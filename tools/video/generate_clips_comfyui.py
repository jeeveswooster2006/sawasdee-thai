"""Make short animated clips of Nong Chang for TikTok / Reels / Shorts with your local ComfyUI.

Two steps for every clip in tools/video/clips_th.json:
  1. a tall still picture of Nong Chang in a new place (Flux, the same set-up as the unit pictures)
  2. that picture brought to life as a 5-second video (Wan 2.2 5B image-to-video)
Claude then adds the Thai word, the voice, "Your turn!" and the end card (tools/social/make_short.py).

Run from the repository folder while ComfyUI is running:
    py -3.12 tools\\video\\generate_clips_comfyui.py --test           (first time: one short, small clip to check it works)
    py -3.12 tools\\video\\generate_clips_comfyui.py                  (all clips that aren't made yet)
    py -3.12 tools\\video\\generate_clips_comfyui.py --clips hello-temple,hot-beach
    py -3.12 tools\\video\\generate_clips_comfyui.py --stills-only    (just the pictures, to check them first)
    py -3.12 tools\\video\\generate_clips_comfyui.py --set intro      (the 4-clip family intro video for TikTok)

Set up for an AMD RX 7800 XT (16 GB): the Wan 2.2 5B model in normal .safetensors files (GGUF versions run very
slowly on that card), a tiled video decoder to save memory, and models unloaded between the picture and video steps.
The first run offers to download the three Wan files (about 18 GB) into ComfyUI's models folders.

Output: tools/video/out/stills/{id}.png and tools/video/out/clips/{id}.mp4
Delete a still or clip and run again to remake just that one.
"""
import argparse
import json
import shutil
import sys
import time
import types
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools" / "art"))
import generate_unit_art_comfyui as art  # noqa: E402  (shared ComfyUI helpers: Comfy, models, Flux workflow)

OUT = HERE / "out"
UPLOAD_URL = "https://github.com/jeeveswooster2006/sawasdee-thai/upload/main/social/clips"

WAN_FILES = {
    # kind: (ComfyUI folder keys to try, file name, download URL, size in GB)
    "model": (("diffusion_models", "unet"), "wan2.2_ti2v_5B_fp16.safetensors",
              "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors", 10.0),
    "text": (("text_encoders", "clip"), "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
             "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", 6.7),
    "vae": (("vae",), "wan2.2_vae.safetensors",
            "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan2.2_vae.safetensors", 1.4),
}

STILL_STYLE = (
    "Soft, polished children's picture-book illustration with gentle painterly shading, clean rounded shapes and warm "
    "friendly lighting. A colourful, detailed Thai setting fills the whole background. Tall vertical 9:16 composition "
    "with the character's whole body clearly visible in the lower middle of the picture and space around it to move. "
    "Correct, simple elephant anatomy: one elephant with exactly four legs, one trunk, two ears and one tail. "
    "No lettering or writing anywhere."
)
MOTION_STYLE = ("Smooth, gentle children's cartoon animation, keep the character exactly the same as in the picture, "
                "same face, scarf and gold ornament, natural movement, steady camera.")
NEGATIVE = ("extra legs, extra limbs, six legs, arms, hands, fingers, deformed, distorted face, blurry, flicker, "
            "text, subtitles, watermark, logo, still image, frozen, ugly, low quality, jpeg artifacts")


def find_folder(comfy, keys):
    try:
        paths = comfy.get_json("/internal/folder_paths")
    except (urllib.error.URLError, OSError, ValueError):
        return None
    for k in keys:
        if paths.get(k):
            return Path(paths[k][0][0] if isinstance(paths[k][0], list) else paths[k][0])
    return None


def download(url, target, size_gb):
    """Resumable download, like the picture script's Flux download."""
    part = target.with_name(target.name + ".part")
    free_gb = shutil.disk_usage(target.parent).free / 1024 ** 3
    if free_gb < size_gb + 1:
        print(f"Not enough disk space in {target.parent} ({free_gb:.0f} GB free, about {size_gb + 1:.0f} GB needed).")
        return False
    print(f"Downloading {target.name} (about {size_gb:.0f} GB) to\n  {target.parent}")
    for attempt in range(1, 8):
        have = part.stat().st_size if part.exists() else 0
        req = urllib.request.Request(url, headers={"Range": f"bytes={have}-"} if have else {})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resumed = have and r.status == 206
                total = (have if resumed else 0) + int(r.headers.get("Content-Length", 0))
                got, last = (have if resumed else 0), 0.0
                with part.open("ab" if resumed else "wb") as f:
                    while chunk := r.read(8 * 1024 * 1024):
                        f.write(chunk)
                        got += len(chunk)
                        if time.time() - last > 5:
                            last = time.time()
                            print(f"  {got / 1024 ** 3:.1f} GB" + (f" ({100 * got / total:.0f}%)" if total else ""), flush=True)
            if total and part.stat().st_size < total:
                raise OSError("download ended early")
            part.replace(target)
            return True
        except urllib.error.HTTPError as e:
            if e.code == 416 and part.exists():
                part.replace(target)
                return True
            print(f"  download problem ({e}); retrying ({attempt}/7)...")
        except (urllib.error.URLError, OSError) as e:
            print(f"  download problem ({e}); retrying ({attempt}/7)...")
        time.sleep(5 * attempt)
    print("The download kept failing. Run this again later and it carries on where it left off.")
    return False


def resolve_wan(comfy, info):
    """Find the Wan 2.2 files in ComfyUI, offering to download any that are missing."""
    for node in ("Wan22ImageToVideoLatent", "CreateVideo", "SaveVideo"):
        if node not in info:
            raise SystemExit(f"Your ComfyUI doesn't have the '{node}' node yet. Update ComfyUI (it's built in to recent "
                             "versions), restart it and run this again.")
    lookups = {"model": ("UNETLoader", "unet_name"), "text": ("CLIPLoader", "clip_name"), "vae": ("VAELoader", "vae_name")}
    found, missing = {}, []
    for kind, (node, field) in lookups.items():
        name = WAN_FILES[kind][1]
        have = art.options(info, node, field)
        found[kind] = name if name in have else None
        if not found[kind]:
            missing.append(kind)
    if missing:
        total = sum(WAN_FILES[k][3] for k in missing)
        print("\nThe Wan 2.2 video model isn't installed yet: " + ", ".join(WAN_FILES[k][1] for k in missing)
              + f" (about {total:.0f} GB).")
        if not art.ask_yes("Download it now?"):
            raise SystemExit("OK - run this again when you're ready.")
        for kind in missing:
            keys, name, url, size = WAN_FILES[kind]
            folder = find_folder(comfy, keys)
            if not folder:
                raise SystemExit(f"Couldn't ask ComfyUI where its models folder is. Download\n  {url}\ninto ComfyUI's "
                                 f"models\\{keys[0]} folder, then run this again.")
            if not download(url, folder / name, size):
                raise SystemExit(1)
        print("Downloads finished - waiting for ComfyUI to notice the new files...")
        for _ in range(30):
            info = comfy.get_json("/object_info")
            if all(WAN_FILES[k][1] in art.options(info, *lookups[k]) for k in missing):
                return {k: WAN_FILES[k][1] for k in lookups}, info
            time.sleep(2)
        raise SystemExit("The files are downloaded but ComfyUI doesn't list them yet. Restart ComfyUI and run this again.")
    return found, info


def wan_workflow(info, wan, image_name, prompt, seed, args):
    w = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": wan["model"], "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": wan["text"], "type": "wan"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": wan["vae"]}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["2", 0]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["2", 0]}},
        "6": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "7": {"class_type": "Wan22ImageToVideoLatent", "inputs": {"vae": ["3", 0], "start_image": ["6", 0],
              "width": args.width, "height": args.height, "length": args.frames, "batch_size": 1}},
        "8": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
        "9": {"class_type": "KSampler", "inputs": {"model": ["8", 0], "positive": ["4", 0], "negative": ["5", 0],
              "latent_image": ["7", 0], "seed": seed, "steps": args.steps, "cfg": 5.0, "sampler_name": "uni_pc",
              "scheduler": "simple", "denoise": 1.0}},
        "11": {"class_type": "CreateVideo", "inputs": {"images": ["10", 0], "fps": 24}},
    }
    if art.has_input(info, "CLIPLoader", "device"):
        w["2"]["inputs"]["device"] = "default"
    if "VAEDecodeTiled" in info:  # decodes the frames in pieces so 16 GB is enough
        inputs = {"samples": ["9", 0], "vae": ["3", 0], "tile_size": 512, "overlap": 64}
        if art.has_input(info, "VAEDecodeTiled", "temporal_size"):
            inputs.update(temporal_size=64, temporal_overlap=8)
        w["10"] = {"class_type": "VAEDecodeTiled", "inputs": inputs}
    else:
        w["10"] = {"class_type": "VAEDecode", "inputs": {"samples": ["9", 0], "vae": ["3", 0]}}
    fmt = "mp4" if "mp4" in art.options(info, "SaveVideo", "format") else "auto"
    codec = "h264" if "h264" in art.options(info, "SaveVideo", "codec") else "auto"
    w["12"] = {"class_type": "SaveVideo", "inputs": {"video": ["11", 0], "filename_prefix": "nongchang/clip",
               "format": fmt, "codec": codec}}
    return w


def flux_args(gpu):
    """The settings the picture script would use, but tall (9:16) instead of wide."""
    return types.SimpleNamespace(checkpoint=None, unet=None, t5=None, clip_l=None, vae=None, weight_dtype="auto",
                                 steps=None, guidance=3.5, width=768, height=1344,
                                 low_memory="on" if gpu and gpu[1] <= 17 else "off",
                                 redux_strength=0.35, no_redux=False, reference=None)


def make_stills(comfy, info, clips, gpu, course, seed_offset):
    fa = flux_args(gpu)
    fa.reference = str(course["reference"])
    models = art.resolve_models(info, fa)
    if fa.weight_dtype == "auto":
        full = models["kind"] == "unet" and not any(t in models["unet"].lower() for t in ("fp8", "int8", "nf4"))
        fa.weight_dtype = "fp8_e4m3fn" if full and "fp8_e4m3fn" in art.options(info, "UNETLoader", "weight_dtype") else "default"
    redux, note = art.resolve_redux(info, fa)
    print(f"Pictures: Flux ({', '.join(str(v) for k, v in models.items() if k != 'kind' and v)}), mascot guide: {note}")
    ref_name = comfy.upload_image(redux["reference"]) if redux else None
    (OUT / "stills").mkdir(parents=True, exist_ok=True)
    made = 0
    for n, c in enumerate(clips, 1):
        target = OUT / "stills" / f"{c['id']}.png"
        if target.exists():
            continue
        prompt = f"{art.CHARACTER}. Scene: {art.NAME} {c['scene']}. {STILL_STYLE}"
        wf = art.build_workflow(models, redux, ref_name, prompt, art.unit_seed(c["id"], 0, seed_offset), fa, info)
        print(f"[picture {n}/{len(clips)}] {c['id']}: making...", flush=True)
        started = time.time()
        resp = comfy.post_json("/prompt", {"prompt": wf, "client_id": "sawasdee-video"})
        target.write_bytes(art.wait_for_image(comfy, resp["prompt_id"], 3600))
        print(f"[picture {n}/{len(clips)}] {c['id']}: saved ({time.time() - started:.0f}s)")
        made += 1
        if fa.low_memory == "on":
            art.free_memory(comfy, unload=True)
            time.sleep(3)
    return made


def make_clips(comfy, info, clips, args):
    wan, info = resolve_wan(comfy, info)
    art.free_memory(comfy, unload=True)  # drop Flux before loading Wan
    time.sleep(3)
    (OUT / "clips").mkdir(parents=True, exist_ok=True)
    print(f"Video: Wan 2.2 5B, {args.width}x{args.height}, {args.frames} frames ({args.frames / 24:.1f}s), {args.steps} steps")
    done = 0
    for n, c in enumerate(clips, 1):
        still = OUT / "stills" / f"{c['id']}.png"
        target = OUT / "clips" / f"{c['id']}{'-test' if args.test else ''}.mp4"
        if target.exists() or not still.exists():
            continue
        image_name = comfy.upload_image(still)
        prompt = f"{c['motion']}. {MOTION_STYLE}"
        wf = wan_workflow(info, wan, image_name, prompt, art.unit_seed(c["id"], 1, args.seed_offset), args)
        print(f"[clip {n}/{len(clips)}] {c['id']}: animating... (expect 10-20+ minutes on an RX 7800 XT)", flush=True)
        started = time.time()
        try:
            resp = comfy.post_json("/prompt", {"prompt": wf, "client_id": "sawasdee-video"})
            target.write_bytes(wait_for_video(comfy, resp["prompt_id"], args.timeout))
        except art.ComfyGone as e:
            print(f"[clip {n}/{len(clips)}] {c['id']}: FAILED - {e}\n  Try --test, or smaller: --width 480 --height 832")
            art.wait_for_comfy(comfy)
            continue
        except (RuntimeError, OSError) as e:
            print(f"[clip {n}/{len(clips)}] {c['id']}: FAILED - {e}")
            if "out of memory" in str(e).lower():
                print("  Out of graphics memory: close games/browsers, or try --width 480 --height 832 --frames 81")
            continue
        done += 1
        print(f"[clip {n}/{len(clips)}] {c['id']}: saved ({(time.time() - started) / 60:.1f} min)")
    return done


def wait_for_video(comfy, prompt_id, timeout):
    """Like the picture script's wait, but also accepts video outputs listed under 'videos' or 'gifs'."""
    import urllib.parse
    started = last_note = time.time()
    while time.time() - started < timeout:
        try:
            hist = comfy.get_json(f"/history/{prompt_id}")
        except urllib.error.URLError as e:
            if "refused" in str(e).lower():
                try:
                    comfy.get_json("/system_stats")
                except (urllib.error.URLError, OSError, ValueError):
                    raise art.ComfyGone("ComfyUI stopped (it crashed - usually from running out of memory)")
            hist = {}
        except (OSError, ValueError):
            hist = {}
        entry = hist.get(prompt_id)
        if entry:
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                msgs = [m[1].get("exception_message", "") for m in status.get("messages", []) if m[0] == "execution_error"]
                raise RuntimeError("ComfyUI failed: " + "; ".join(msgs))
            for out in entry.get("outputs", {}).values():
                for key in ("videos", "gifs", "images"):
                    for f in out.get(key, []):
                        if isinstance(f, dict) and f.get("filename"):
                            q = urllib.parse.urlencode({"filename": f["filename"], "subfolder": f.get("subfolder", ""),
                                                        "type": f.get("type", "output")})
                            return comfy.get(f"/view?{q}")
            if status.get("completed"):
                raise RuntimeError("ComfyUI finished but returned no video")
        if time.time() - last_note >= 120:
            last_note = time.time()
            print(f"    ...still working ({(last_note - started) / 60:.0f} min)", flush=True)
        time.sleep(3)
    art.cancel(comfy, prompt_id)
    raise TimeoutError(f"timed out after {timeout}s")


def prepare_upload():
    import os
    import webbrowser
    clips = sorted((OUT / "clips").glob("*.mp4"))
    if not clips:
        return
    dest = OUT / "upload-to-github"
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    for c in clips:
        shutil.copyfile(c, dest / c.name)
    print(f"\n{len(clips)} clip(s) ready to upload in: {dest}\n"
          "Drag them all onto the GitHub page that opens, click 'Commit changes', then tell Claude 'clips uploaded'.")
    try:
        os.startfile(str(dest))  # Windows only
    except (AttributeError, OSError):
        pass
    webbrowser.open(UPLOAD_URL)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="ComfyUI address (default: tries 127.0.0.1:8188, then 127.0.0.1:8000)")
    ap.add_argument("--course", choices=sorted(art.COURSES), default="th", help="th = Nong Chang (default), es = Torito")
    ap.add_argument("--set", help="which clip list to use: intro = the 4-clip family intro video (default: the course list)")
    ap.add_argument("--clips", help="comma-separated clip ids (default: all in the list)")
    ap.add_argument("--test", action="store_true", help="one short, small clip (2 s, 480x832) to check everything works")
    ap.add_argument("--stills-only", action="store_true", help="only make the still pictures")
    ap.add_argument("--width", type=int, default=704); ap.add_argument("--height", type=int, default=1280)
    ap.add_argument("--frames", type=int, default=121, help="121 = 5 seconds at 24 fps (must be 4n+1)")
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--seed-offset", type=int, default=0, help="change to get different results")
    ap.add_argument("--timeout", type=int, default=5400, help="seconds to wait per clip (default 90 minutes)")
    args = ap.parse_args()
    if args.test:
        args.width, args.height, args.frames = 480, 832, 49
    args.frames = (args.frames - 1) // 4 * 4 + 1

    course = art.use_course(args.course)
    spec = json.loads((HERE / f"clips_{args.set or args.course}.json").read_text(encoding="utf-8"))
    clips = spec["clips"]
    if args.clips:
        wanted = {x.strip() for x in args.clips.split(",")}
        clips = [c for c in clips if c["id"] in wanted]
        if not clips:
            raise SystemExit("None of those clip ids are in the list.")
    if args.test:
        clips = clips[:1]

    urls = [args.url] if args.url else ["http://127.0.0.1:8188", "http://127.0.0.1:8000"]
    for url in urls:
        try:
            comfy = art.Comfy(url)
            info = comfy.get_json("/object_info")
            break
        except (urllib.error.URLError, OSError, ValueError):
            continue
    else:
        raise SystemExit(f"Can't reach ComfyUI at {' or '.join(urls)}. Start ComfyUI first.")
    gpu = art.check_gpu(comfy)
    print(f"ComfyUI: {comfy.url}" + (f" - {gpu[0]} ({gpu[1]:.0f} GB)" if gpu else ""))

    made = make_stills(comfy, info, clips, gpu, course, args.seed_offset)
    print(f"\nPictures are in {OUT / 'stills'}" + (f" ({made} new)" if made else ""))
    if args.stills_only:
        print("Look through them, delete any you don't like and run again to remake those.")
        return
    if made and sys.stdin.isatty() and not art.ask_yes("Have a look at the pictures first. Carry on and animate them?"):
        print("OK - delete any you don't like, then run this again.")
        return
    done = make_clips(comfy, info, clips, args)
    print(f"\nDone: {done} clip(s) made. They're in {OUT / 'clips'}")
    if done and not args.test:
        prepare_upload()
    elif done:
        print("Test clip made - send it to Claude (or play it) to check the quality before doing the rest.")


if __name__ == "__main__":
    main()
