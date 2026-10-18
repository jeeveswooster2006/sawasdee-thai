"""Generate the Sawasdee Thai unit illustrations with your local ComfyUI + Flux.

Run from the repository folder while ComfyUI is running:
    py -3.12 tools\\art\\generate_unit_art_comfyui.py --list-models        (see what it found)
    py -3.12 tools\\art\\generate_unit_art_comfyui.py --units basics1,food  (quick test: 2 images)
    py -3.12 tools\\art\\generate_unit_art_comfyui.py                       (the 39 units without art)
    py -3.12 tools\\art\\generate_unit_art_comfyui.py --all                 (all 43, one consistent style)

It asks ComfyUI which models are installed and picks Flux automatically: either a single
Flux checkpoint, or separate diffusion model + T5/CLIP-L text encoders + VAE (ae.safetensors).
GGUF Flux models work too if the ComfyUI-GGUF custom nodes are installed. Override any
choice with --checkpoint / --unet / --t5 / --clip-l / --vae.

Character consistency: every prompt carries a detailed description of Nong Chang. If Flux
Redux is installed (flux1-redux-dev + sigclip_vision_patch14_384) and tools/art/mascot.png
exists, the mascot image is also used as a reference at a gentle strength.

Output: art/units/{unit_id}.png (and a small .webp copy for the app if Pillow is installed).
Finished units are skipped on re-run; each unit has a fixed seed so results are repeatable.
"""
import argparse
import hashlib
import json
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "tools" / "art" / "unit_illustrations.json"
OUT = ROOT / "art" / "units"

CHARACTER = (
    "Nong Chang, an adorable baby elephant mascot with soft warm grey skin and gentle shading, "
    "large round glossy dark eyes with small white highlights, rosy pink cheeks, big rounded ears "
    "with pink insides, a short curled trunk, a chubby round body standing on exactly four short "
    "sturdy elephant legs (two front legs and two back legs, no arms and no hands - it holds and "
    "picks things up with its trunk), a small ornate "
    "gold Thai flame-shaped ornament on top of the head, wearing a deep teal scarf with an ornate "
    "gold Thai temple-pattern border"
)
STYLE = (
    "Soft, polished children's picture-book illustration with gentle painterly shading, clean "
    "rounded shapes and warm friendly lighting. Simple uncluttered warm ivory background with "
    "subtle teal and gold accents. Landscape composition, Nong Chang is the clear focus. "
    "Correct, simple elephant anatomy: one elephant with exactly four legs, one trunk, two ears and one tail. "
    "No lettering or writing anywhere."
)

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# The single-file fp8 Flux dev from the ComfyUI team: model + fp8 T5 + CLIP-L + VAE, about 17 GB.
# It fits a 16 GB graphics card and a 32 GB PC, where the full-size 23 GB file runs out of memory.
SMALL_FLUX_NAME = "flux1-dev-fp8.safetensors"
SMALL_FLUX_URL = "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors"


class ComfyGone(RuntimeError):
    """ComfyUI stopped answering in the middle of an image (usually a crash from running out of memory)."""


class Comfy:
    def __init__(self, url):
        self.url = url.rstrip("/")

    def get(self, path):
        with opener.open(self.url + path, timeout=60) as r:
            return r.read()

    def get_json(self, path):
        return json.loads(self.get(path))

    def post_json(self, path, payload):
        req = urllib.request.Request(self.url + path, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with opener.open(req, timeout=60) as r:
                body = r.read()
                return json.loads(body) if body.strip() else {}  # /free and /interrupt reply with an empty body
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            raise SystemExit(f"ComfyUI rejected the request ({e.code}):\n{format_comfy_error(body)}")
        except urllib.error.URLError as e:
            if isinstance(e.reason, ConnectionRefusedError):
                raise ComfyGone("ComfyUI isn't running (it may have crashed)")
            raise

    def upload_image(self, path):
        boundary = uuid.uuid4().hex
        data = path.read_bytes()
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{path.name}\"\r\n"
                f"Content-Type: image/png\r\n\r\n").encode() + data + \
               (f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue"
                f"\r\n--{boundary}--\r\n").encode()
        req = urllib.request.Request(self.url + "/upload/image", data=body,
                                     headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        with opener.open(req, timeout=60) as r:
            return json.loads(r.read())["name"]


def format_comfy_error(body):
    try:
        err = json.loads(body)
    except ValueError:
        return body
    lines = [str(err.get("error", {}).get("message", err.get("error")))]
    for node, info in (err.get("node_errors") or {}).items():
        for e in info.get("errors", []):
            lines.append(f"  node {node} ({info.get('class_type')}): {e.get('message')} {e.get('details', '')}")
    return "\n".join(lines)


def options(info, node, field):
    """Choices for a combo input, handling both old ([list, cfg]) and new ("COMBO", {options}) formats."""
    spec = info.get(node, {}).get("input", {})
    entry = spec.get("required", {}).get(field) or spec.get("optional", {}).get(field)
    if not entry:
        return []
    if isinstance(entry[0], list):
        return entry[0]
    if entry[0] == "COMBO" and len(entry) > 1:
        return entry[1].get("options", [])
    return []


def has_input(info, node, field):
    spec = info.get(node, {}).get("input", {})
    return field in spec.get("required", {}) or field in spec.get("optional", {})


def pick(choices, *needles, avoid=("redux", "fill", "canny", "depth", "kontext", "lora")):
    usable = [c for c in choices if not any(a in c.lower() for a in avoid)]
    for needle_set in needles:
        for c in usable:
            if all(n in c.lower() for n in needle_set):
                return c
    return None


def is_small(name):
    n = name.lower()
    return n.endswith(".gguf") or any(t in n for t in ("fp8", "int8", "nf4"))


def resolve_models(info, args):
    m = {"kind": None}
    if args.checkpoint:
        m.update(kind="checkpoint", checkpoint=args.checkpoint)
    elif args.unet:
        m.update(kind="gguf" if args.unet.lower().endswith(".gguf") else "unet", unet=args.unet)
    else:
        unets = options(info, "UNETLoader", "unet_name")
        ggufs = options(info, "UnetLoaderGGUF", "unet_name")
        ckpts = options(info, "CheckpointLoaderSimple", "ckpt_name")
        prefs = (("flux", "dev"), ("flux", "schnell"), ("flux",))
        u, g, c = pick(unets, *prefs), pick(ggufs, *prefs), pick(ckpts, *prefs)
        order = [("unet", u), ("gguf", g), ("checkpoint", c)]
        if args.low_memory == "on":
            # Prefer files that are already small (fp8/GGUF) over a full-size model.
            order = [("unet", pick([x for x in unets if is_small(x)], *prefs)), ("gguf", g),
                     ("checkpoint", pick([x for x in ckpts if is_small(x)], *prefs))] + order
        chosen = next(((kind, name) for kind, name in order if name), None)
        if chosen:
            m.update(kind=chosen[0], **{"checkpoint" if chosen[0] == "checkpoint" else "unet": chosen[1]})
        else:
            raise SystemExit("Couldn't find a Flux model in ComfyUI. Run with --list-models to see what's "
                             "installed, then pass --checkpoint or --unet with the exact file name.")
    if m["kind"] in ("unet", "gguf"):
        encoders = options(info, "DualCLIPLoader", "clip_name1")
        gguf_encoders = options(info, "DualCLIPLoaderGGUF", "clip_name1")
        t5_prefs = (("t5xxl", "fp8"), ("t5xxl", "fp16")) if args.low_memory == "on" else (("t5xxl", "fp16"), ("t5xxl", "fp8"))
        m["t5"] = args.t5 or pick(encoders, *t5_prefs, ("t5",)) or pick(gguf_encoders, ("t5",))
        m["clip_l"] = args.clip_l or pick(encoders, ("clip_l",)) or pick(gguf_encoders, ("clip_l",))
        m["vae"] = args.vae or pick(options(info, "VAELoader", "vae_name"), ("ae.",), ("flux",), ("ae",))
        missing = [k for k in ("t5", "clip_l", "vae") if not m[k]]
        if missing:
            raise SystemExit(f"Found Flux model {m['unet']} but not its {', '.join(missing)} file(s). "
                             "Pass them with --t5 / --clip-l / --vae (see --list-models).")
        m["clip_loader"] = "DualCLIPLoaderGGUF" if m["t5"].lower().endswith(".gguf") else "DualCLIPLoader"
    name = (m.get("unet") or m.get("checkpoint")).lower()
    m["schnell"] = "schnell" in name
    return m


def resolve_redux(info, args):
    if args.no_redux:
        return None, "turned off with --no-redux"
    ref = Path(args.reference)
    if not ref.exists():
        return None, f"no reference image at {ref}"
    sig = pick(options(info, "CLIPVisionLoader", "clip_name"), ("sigclip",), ("siglip",), avoid=())
    redux = pick(options(info, "StyleModelLoader", "style_model_name"), ("redux",), avoid=())
    if not (sig and redux):
        return None, "Flux Redux models not installed (needs flux1-redux-dev + sigclip_vision_patch14_384)"
    if not has_input(info, "StyleModelApply", "strength"):
        return None, "your ComfyUI is too old for Redux strength control (update ComfyUI to use it)"
    return {"clip_vision": sig, "style_model": redux, "reference": ref}, "on"


def build_workflow(models, redux, ref_name, prompt, seed, args, info=None):
    info = info or {}
    low = args.low_memory == "on"
    w = {}
    if models["kind"] == "checkpoint":
        w["1"] = {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": models["checkpoint"]}}
        model, clip, vae = ["1", 0], ["1", 1], ["1", 2]
    else:
        if models["kind"] == "gguf":
            w["1"] = {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": models["unet"]}}
        else:
            w["1"] = {"class_type": "UNETLoader", "inputs": {"unet_name": models["unet"], "weight_dtype": args.weight_dtype}}
        w["2"] = {"class_type": models["clip_loader"],
                  "inputs": {"clip_name1": models["t5"], "clip_name2": models["clip_l"], "type": "flux"}}
        if low and has_input(info, models["clip_loader"], "device"):
            w["2"]["inputs"]["device"] = "cpu"  # keep the 9 GB T5 text encoder off the graphics card
        w["3"] = {"class_type": "VAELoader", "inputs": {"vae_name": models["vae"]}}
        model, clip, vae = ["1", 0], ["2", 0], ["3", 0]
    w["4"] = {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": clip}}
    w["5"] = {"class_type": "FluxGuidance", "inputs": {"conditioning": ["4", 0], "guidance": args.guidance}}
    positive = ["5", 0]
    if redux:
        w["20"] = {"class_type": "LoadImage", "inputs": {"image": ref_name}}
        w["21"] = {"class_type": "CLIPVisionLoader", "inputs": {"clip_name": redux["clip_vision"]}}
        w["22"] = {"class_type": "CLIPVisionEncode", "inputs": {"clip_vision": ["21", 0], "image": ["20", 0], "crop": "center"}}
        w["23"] = {"class_type": "StyleModelLoader", "inputs": {"style_model_name": redux["style_model"]}}
        w["24"] = {"class_type": "StyleModelApply", "inputs": {"conditioning": positive, "style_model": ["23", 0],
                   "clip_vision_output": ["22", 0], "strength": args.redux_strength, "strength_type": "multiply"}}
        positive = ["24", 0]
    w["6"] = {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": clip}}
    w["7"] = {"class_type": "EmptySD3LatentImage", "inputs": {"width": args.width, "height": args.height, "batch_size": 1}}
    w["8"] = {"class_type": "KSampler", "inputs": {
        "model": model, "seed": seed, "steps": args.steps or (4 if models["schnell"] else 28), "cfg": 1.0,
        "sampler_name": "euler", "scheduler": "simple", "positive": positive, "negative": ["6", 0],
        "latent_image": ["7", 0], "denoise": 1.0}}
    if low and "VAEDecodeTiled" in info:
        tiled = {"tile_size": 512, "overlap": 64, "temporal_size": 64, "temporal_overlap": 8}
        w["9"] = {"class_type": "VAEDecodeTiled", "inputs": dict({"samples": ["8", 0], "vae": vae},
                  **{k: v for k, v in tiled.items() if has_input(info, "VAEDecodeTiled", k)})}
    else:
        w["9"] = {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": vae}}
    w["10"] = {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "sawasdee/unit"}}
    return w


def unit_seed(unit_id, variant, offset):
    return (int(hashlib.md5(unit_id.encode()).hexdigest()[:8], 16) + 1009 * variant + offset) % (2 ** 32)


def queue_state(comfy, prompt_id):
    try:
        q = comfy.get_json("/queue")
    except (urllib.error.URLError, OSError, ValueError):
        return "unknown"
    if any(item[1] == prompt_id for item in q.get("queue_running", [])):
        return "running"
    if any(item[1] == prompt_id for item in q.get("queue_pending", [])):
        return "waiting in ComfyUI's queue"
    return "unknown"


def cancel(comfy, prompt_id):
    """Take a timed-out job out of ComfyUI so it doesn't block every image after it."""
    try:
        if queue_state(comfy, prompt_id) == "running":
            comfy.post_json("/interrupt", {})
        comfy.post_json("/queue", {"delete": [prompt_id]})
    except (urllib.error.URLError, OSError, ValueError, SystemExit, RuntimeError):
        pass


def download_small_flux(comfy, info):
    """Download the fp8 Flux dev checkpoint into ComfyUI's checkpoints folder, resuming if interrupted."""
    try:
        folder = Path(comfy.get_json("/internal/folder_paths")["checkpoints"][0])
    except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError, TypeError):
        print(f"Couldn't ask ComfyUI where its models folder is. Download this file in your browser:\n  {SMALL_FLUX_URL}\n"
              "and put it in ComfyUI's models\\checkpoints folder, then run this again.")
        return False
    target, part = folder / SMALL_FLUX_NAME, folder / (SMALL_FLUX_NAME + ".part")
    if not target.exists():
        free_gb = shutil.disk_usage(folder).free / 1024 ** 3
        have = part.stat().st_size if part.exists() else 0
        if free_gb < 18 - have / 1024 ** 3:
            print(f"Not enough free disk space in {folder} ({free_gb:.0f} GB free, about 18 GB needed).")
            return False
        print(f"Downloading {SMALL_FLUX_NAME} (about 17 GB) to\n  {folder}\nThis takes a while; you can stop and "
              "restart it, and it carries on where it left off.")
        for attempt in range(1, 8):
            have = part.stat().st_size if part.exists() else 0
            req = urllib.request.Request(SMALL_FLUX_URL, headers={"Range": f"bytes={have}-"} if have else {})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    resumed = have and r.status == 206
                    size = int(r.headers.get("Content-Length", 0))
                    total = have + size if resumed else size
                    got, last = (have if resumed else 0), 0.0
                    with part.open("ab" if resumed else "wb") as f:
                        while True:
                            chunk = r.read(8 * 1024 * 1024)
                            if not chunk:
                                break
                            f.write(chunk)
                            got += len(chunk)
                            if time.time() - last > 5:
                                last = time.time()
                                pct = f" ({100 * got / total:.0f}%)" if total else ""
                                print(f"  {got / 1024 ** 3:.1f} GB{pct}", flush=True)
                if total and part.stat().st_size < total:
                    raise OSError("download ended early")
                break
            except urllib.error.HTTPError as e:
                if e.code == 416:  # nothing left to download
                    break
                print(f"  download problem ({e}); retrying ({attempt}/7)...")
                time.sleep(5 * attempt)
            except (urllib.error.URLError, OSError) as e:
                print(f"  download problem ({e}); retrying ({attempt}/7)...")
                time.sleep(5 * attempt)
        else:
            print("The download kept failing. Check your internet connection and run this again to resume.")
            return False
        part.replace(target)
        print("Download finished.")
    for _ in range(30):  # ComfyUI notices new model files on its own; give it a moment
        if SMALL_FLUX_NAME in options(comfy.get_json("/object_info"), "CheckpointLoaderSimple", "ckpt_name"):
            return True
        time.sleep(2)
    print("The file is downloaded but ComfyUI doesn't list it yet. Restart ComfyUI and run this again.")
    return False


def free_memory(comfy, unload=False):
    try:
        comfy.post_json("/free", {"unload_models": unload, "free_memory": True})
    except (urllib.error.URLError, OSError, ValueError, SystemExit, RuntimeError):
        pass


def ask_yes(question):
    if not sys.stdin.isatty():
        return False
    try:
        return input(f"{question} [Y/N] ").strip().lower().startswith("y")
    except EOFError:
        return False


def wait_for_comfy(comfy):
    input("\nComfyUI has stopped. Open ComfyUI again, wait until it has finished loading, then press Enter here... ")
    while True:
        try:
            comfy.get_json("/system_stats")
            return
        except (urllib.error.URLError, OSError, ValueError):
            print("  ComfyUI isn't answering yet - waiting...")
            time.sleep(5)


def check_gpu(comfy):
    """Return (name, vram_gb, looks_integrated) for the device ComfyUI renders on, or None if unknown."""
    try:
        stats = comfy.get_json("/system_stats")
        dev = stats["devices"][0]
    except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError, TypeError):
        return None
    name, vram = str(dev.get("name", "")), (dev.get("vram_total") or 0) / 1024 ** 3
    check_gpu.ram_gb = ((stats.get("system") or {}).get("ram_total") or 0) / 1024 ** 3
    low = name.lower()
    integrated = dev.get("type") != "cpu" and (
        ("radeon" in low and "graphics" in low and " rx " not in f" {low} ") or "intel" in low or 0 < vram < 6)
    return name, vram, integrated


def wait_for_image(comfy, prompt_id, timeout):
    started = last_note = time.time()
    unreachable_since = None
    while time.time() - started < timeout:
        try:
            hist = comfy.get_json(f"/history/{prompt_id}")
            unreachable_since = None
        except urllib.error.URLError as e:
            if isinstance(getattr(e, "reason", None), ConnectionRefusedError) or "refused" in str(e).lower():
                unreachable_since = unreachable_since or time.time()
                if time.time() - unreachable_since > 20:
                    raise ComfyGone("ComfyUI stopped (it crashed - usually from running out of memory)")
            hist = {}  # ComfyUI can be slow to answer while it loads a big model; just ask again
        except (OSError, ValueError):
            hist = {}
        if prompt_id in hist:
            entry = hist[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                msgs = [m[1].get("exception_message", "") for m in status.get("messages", []) if m[0] == "execution_error"]
                raise RuntimeError("ComfyUI failed: " + "; ".join(msgs))
            for out in entry.get("outputs", {}).values():
                for img in out.get("images", []):
                    q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img.get("subfolder", ""),
                                                "type": img.get("type", "output")})
                    return comfy.get(f"/view?{q}")
            if status.get("completed"):
                raise RuntimeError("ComfyUI finished but returned no image")
        if time.time() - last_note >= 60:
            last_note = time.time()
            print(f"    ...still working ({last_note - started:.0f}s, {queue_state(comfy, prompt_id)})", flush=True)
        time.sleep(2)
    cancel(comfy, prompt_id)
    raise TimeoutError(f"timed out after {timeout}s")


def save_web_copy(png_path):
    try:
        from PIL import Image
    except ImportError:
        return False
    with Image.open(png_path) as im:
        im = im.convert("RGB")
        w = 960
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(png_path.with_suffix(".webp"), "WEBP", quality=82, method=6)
    return True


SPEC_URL = "https://raw.githubusercontent.com/jeeveswooster2006/sawasdee-thai/main/tools/art/unit_illustrations.json"


def refresh_spec():
    """Fetch the latest picture descriptions, so scene fixes reach this PC without a new download."""
    try:
        with urllib.request.urlopen(SPEC_URL, timeout=20) as r:
            data = r.read()
        if json.loads(data.decode("utf-8")).get("units"):
            SPEC.write_bytes(data)
            print("Picture list: up to date")
    except (urllib.error.URLError, OSError, ValueError):
        print("Picture list: couldn't check for updates - using the copy already here")


def ask_redo(units):
    """All pictures exist: ask which ones to make again (e.g. ones with extra legs)."""
    ids = [u["unit_id"] for u in units]
    print("\nAll the pictures are made (they're in art\\units).")
    print("If any look wrong (extra legs, odd faces), you can make new versions of them.")
    print("Picture names: " + ", ".join(ids))
    while True:
        answer = input("\nType the names to redo, separated by commas (e.g. emergency,weather), "
                       "or just press Enter to finish: ").strip().lower()
        if not answer:
            return set()
        picked = {a.strip().removesuffix(".png").removesuffix(".webp") for a in answer.split(",") if a.strip()}
        unknown = picked - set(ids)
        if not unknown:
            print(f"OK - making 3 new versions of: {', '.join(sorted(picked))}")
            return picked
        print(f"I don't know: {', '.join(sorted(unknown))}. Check the spelling against the list above.")


def choose_options(units, variants):
    """Show where the new versions are and let the person pick one to use."""
    letters = "abcdefghij"[:variants]
    print(f"\nThe new versions are in {OUT / 'options'}")
    print("Open that folder, look at each picture, then choose here.")
    for u in units:
        uid = u["unit_id"]
        have = [x for x in letters if (OUT / "options" / f"{uid}-{x}.png").exists()]
        if not have:
            continue
        while True:
            answer = input(f"\n{uid}: which one do you want? Type {', '.join(have)} "
                           f"(or press Enter to keep the old picture): ").strip().lower()
            if not answer:
                print(f"  Kept the old {uid} picture.")
                break
            if answer in have:
                chosen = OUT / f"{uid}.png"
                shutil.copyfile(OUT / "options" / f"{uid}-{answer}.png", chosen)
                save_web_copy(chosen)
                print(f"  Done - {uid}-{answer} is now the {uid} picture.")
                break
            print(f"  Please type one of: {', '.join(have)}")
    print("\nFinished. Upload the .webp files from art\\units to GitHub when you're happy with them.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="ComfyUI address (default: tries 127.0.0.1:8188, then Desktop's 127.0.0.1:8000)")
    ap.add_argument("--units", help="comma-separated unit ids to generate (e.g. basics1,food)")
    ap.add_argument("--all", action="store_true", help="all 43 units, including the 4 that have Canva art")
    ap.add_argument("--force", action="store_true", help="regenerate even if the image already exists")
    ap.add_argument("--variants", type=int, default=1, help="images per unit, to pick the best (default 1)")
    ap.add_argument("--seed-offset", type=int, default=0, help="change to get different images")
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print the first workflow instead of running it")
    ap.add_argument("--checkpoint"); ap.add_argument("--unet"); ap.add_argument("--t5")
    ap.add_argument("--clip-l"); ap.add_argument("--vae")
    ap.add_argument("--weight-dtype", default="auto",
                    help="UNETLoader weight dtype: auto (fp8 for full-size Flux files, to fit 16 GB cards), default, fp8_e4m3fn")
    ap.add_argument("--steps", type=int, help="default 28 for Flux dev, 4 for schnell")
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--width", type=int, default=1216); ap.add_argument("--height", type=int, default=832)
    ap.add_argument("--reference", default=str(ROOT / "tools" / "art" / "mascot.png"))
    ap.add_argument("--no-redux", action="store_true")
    ap.add_argument("--redux-strength", type=float, default=0.35)
    ap.add_argument("--low-memory", choices=["auto", "on", "off"], default="auto",
                    help="text encoders on the CPU + tiled decoding; auto = on for cards with 16 GB or less")
    ap.add_argument("--download-small", action="store_true",
                    help=f"download {SMALL_FLUX_NAME} (17 GB, fits 16 GB cards / 32 GB PCs) into ComfyUI and exit")
    ap.add_argument("--allow-full-size", action="store_true",
                    help="use a full-size Flux file even on a 16 GB card with less than 48 GB of memory")
    ap.add_argument("--any-gpu", action="store_true", help="don't stop when ComfyUI is on a built-in graphics chip")
    ap.add_argument("--stall-after", type=int, default=600,
                    help="retry an image fresh if it takes this long and 5x the fastest one so far (default 600 s)")
    ap.add_argument("--timeout", type=int, default=3600, help="seconds to wait per image (default 3600)")
    args = ap.parse_args()

    # ComfyUI Desktop listens on 8000, a command-line/portable install on 8188; use whichever has Flux.
    urls = [args.url] if args.url else ["http://127.0.0.1:8188", "http://127.0.0.1:8000"]
    reachable = []
    for url in urls:
        try:
            reachable.append((Comfy(url), Comfy(url).get_json("/object_info")))
        except (urllib.error.URLError, OSError, ValueError):
            pass
    if not reachable:
        print(f"Can't reach ComfyUI at {' or '.join(urls)}. Start ComfyUI first "
              "(or pass --url if it uses a different address).")
        sys.exit(2)
    comfy, info = reachable[0]
    if len(reachable) > 1 and not args.list_models:
        for c, i in reachable:
            try:
                resolve_models(i, args)
                comfy, info = c, i
                break
            except SystemExit:
                continue
    print(f"ComfyUI: {comfy.url}")

    if args.list_models:
        for c, i in reachable:
            print(f"\n=== {c.url} ===")
            for label, node, field in [("Checkpoints", "CheckpointLoaderSimple", "ckpt_name"),
                                       ("Diffusion models", "UNETLoader", "unet_name"),
                                       ("GGUF models", "UnetLoaderGGUF", "unet_name"),
                                       ("Text encoders", "DualCLIPLoader", "clip_name1"),
                                       ("VAEs", "VAELoader", "vae_name"),
                                       ("CLIP vision", "CLIPVisionLoader", "clip_name"),
                                       ("Style models (Redux)", "StyleModelLoader", "style_model_name")]:
                print(f"{label}: {', '.join(options(i, node, field)) or '(none)'}")
        return

    gpu = check_gpu(comfy)
    if gpu:
        print(f"Graphics: {gpu[0]} ({gpu[1]:.1f} GB)")
        if gpu[2] and not args.any_gpu and not args.dry_run:
            print("\nComfyUI is using the processor's built-in graphics chip, which is far too slow for Flux.\n"
                  "Point it at your graphics card (e.g. start ComfyUI with --cuda-device 1), restart it, and run this again.")
            sys.exit(3)
    if args.low_memory == "auto":
        args.low_memory = "on" if gpu and gpu[1] <= 17 else "off"
    if args.low_memory == "on":
        print("Low-memory mode: lighter settings for graphics cards with 16 GB or less")
    if args.download_small:
        sys.exit(0 if download_small_flux(comfy, info) else 1)
    models = resolve_models(info, args)
    ram_gb = getattr(check_gpu, "ram_gb", 0)
    if (args.low_memory == "on" and models["kind"] == "unet" and not is_small(models["unet"]) and 0 < ram_gb < 48
            and not args.allow_full_size and not args.unet and not args.dry_run):
        print(f"\nYour Flux file ({models['unet']}) is the full-size 23 GB version. With a {gpu[1]:.0f} GB graphics card "
              f"and {ram_gb:.0f} GB of memory it runs out of memory and makes ComfyUI crash.\n"
              f"The fix is the smaller fp8 version ({SMALL_FLUX_NAME}, about 17 GB, free). Same pictures, half the memory.")
        if not ask_yes("Download it now?"):
            print("OK - run this again when you're ready (or use --download-small).")
            sys.exit(5)
        if not download_small_flux(comfy, info):
            sys.exit(1)
        info = comfy.get_json("/object_info")
        models = resolve_models(info, args)
    if args.weight_dtype == "auto":
        # A full-size Flux dev file is ~23 GB; loading it as fp8 halves that so it fits a 16 GB card.
        full_size = models["kind"] == "unet" and not any(t in models["unet"].lower() for t in ("fp8", "int8", "nf4"))
        fp8_ok = "fp8_e4m3fn" in options(info, "UNETLoader", "weight_dtype")
        args.weight_dtype = "fp8_e4m3fn" if full_size and fp8_ok else "default"
        if args.weight_dtype != "default":
            print("Loading the diffusion model as fp8 to save graphics memory (--weight-dtype default to turn off)")
    redux, redux_note = resolve_redux(info, args)
    print("Using:", ", ".join(f"{k}={v}" for k, v in models.items() if k not in ("kind",) and v not in (None, False)))
    print(f"Mascot reference (Flux Redux): {redux_note}")

    refresh_spec()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    units = spec["units"]
    if args.units:
        wanted = {u.strip() for u in args.units.split(",")}
        unknown = wanted - {u["unit_id"] for u in units}
        if unknown:
            raise SystemExit(f"Unknown unit id(s): {', '.join(sorted(unknown))}")
        units = [u for u in units if u["unit_id"] in wanted]
    elif not args.all:
        units = [u for u in units if not u.get("canva_media_id")]

    redo = False
    if (not args.units and not args.force and not args.dry_run and sys.stdin.isatty()
            and units and all((OUT / f"{u['unit_id']}.png").exists() for u in units)):
        picked = ask_redo(units)
        if not picked:
            print("Nothing to redo. All done!")
            return
        units = [u for u in units if u["unit_id"] in picked]
        redo = True
        args.variants = max(args.variants, 3)
        args.seed_offset = int(time.time()) % 100000  # fresh pictures each time
    ref_name = comfy.upload_image(redux["reference"]) if redux and not args.dry_run else (redux and redux["reference"].name)
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(u, v) for u in units for v in range(args.variants)]
    print(f"{len(jobs)} image(s) to make for {len(units)} unit(s) -> {OUT}")
    webp_warned = False
    done = skipped = failed = 0
    fastest = 0.0
    for n, (u, v) in enumerate(jobs, 1):
        if redo:
            name = f"{u['unit_id']}-{'abcdefghij'[v]}"
            target = OUT / "options" / f"{name}.png"
            target.parent.mkdir(parents=True, exist_ok=True)
        else:
            name = u["unit_id"] + ("" if v == 0 else f"-v{v + 1}")
            target = OUT / f"{name}.png"
        if target.exists() and not args.force and not redo:
            skipped += 1
            continue
        prompt = f"{CHARACTER}. Scene: Nong Chang {u['scene']}. {STYLE}"
        workflow = build_workflow(models, redux, ref_name, prompt, unit_seed(u["unit_id"], v, args.seed_offset), args, info)
        if args.dry_run:
            print(json.dumps(workflow, ensure_ascii=False, indent=1))
            return
        started = time.time()
        print(f"[{n}/{len(jobs)}] {name}: making..." + (" (the first one also loads the model, so it's slowest)"
                                                        if done == 0 else ""), flush=True)
        # Once we know how fast an image can be, give up early on one that has stalled and retry it fresh.
        limit = min(args.timeout, max(args.stall_after, 5 * fastest)) if fastest else args.timeout
        try:
            try:
                resp = comfy.post_json("/prompt", {"prompt": workflow, "client_id": "sawasdee-art"})
                target.write_bytes(wait_for_image(comfy, resp["prompt_id"], limit))
            except TimeoutError:
                if limit >= args.timeout:
                    raise
                print(f"[{n}/{len(jobs)}] {name}: much slower than usual ({limit:.0f}s) - freeing memory and retrying")
                free_memory(comfy, unload=True)
                time.sleep(5)
                resp = comfy.post_json("/prompt", {"prompt": workflow, "client_id": "sawasdee-art"})
                target.write_bytes(wait_for_image(comfy, resp["prompt_id"], args.timeout))
            except RuntimeError as e:
                if "out of memory" not in str(e).lower():
                    raise
                # Free everything ComfyUI is holding, switch to low-memory mode and try this image once more.
                print(f"[{n}/{len(jobs)}] {name}: ran out of graphics memory - freeing memory and retrying in low-memory mode")
                free_memory(comfy, unload=True)
                time.sleep(5)
                args.low_memory = "on"
                workflow = build_workflow(models, redux, ref_name, prompt,
                                          unit_seed(u["unit_id"], v, args.seed_offset), args, info)
                resp = comfy.post_json("/prompt", {"prompt": workflow, "client_id": "sawasdee-art"})
                target.write_bytes(wait_for_image(comfy, resp["prompt_id"], args.timeout))
        except ComfyGone as e:
            print(f"[{n}/{len(jobs)}] {name}: FAILED - {e}")
            if not sys.stdin.isatty():
                sys.exit(4)
            wait_for_comfy(comfy)
            failed += 1
            print("  Carrying on. Run this again afterwards to retry anything that failed.")
            continue
        except (RuntimeError, OSError) as e:
            failed += 1
            print(f"[{n}/{len(jobs)}] {name}: FAILED - {e}")
            if done == 0 and "out of memory" in str(e).lower():
                raise SystemExit("\nStopping: the graphics card ran out of memory even in low-memory mode.\n"
                                 "Close other programs that use the graphics card (games, browsers with many tabs),\n"
                                 "restart ComfyUI and run this again. If it still happens, paste this window to Claude.")
            if isinstance(e, TimeoutError) and done == 0:
                raise SystemExit("\nStopping: not even one image finished, so the rest would time out too.\n"
                                 "Check the ComfyUI window for errors or an out-of-memory message, then try:\n"
                                 "  py -3.12 tools\\art\\generate_unit_art_comfyui.py --units colors --steps 20\n"
                                 "and paste what both windows say.")
            continue
        made_webp = save_web_copy(target)
        if not made_webp and not webp_warned:
            print("  (tip: `py -3.12 -m pip install pillow` to also get small .webp copies for the app)")
            webp_warned = True
        if args.low_memory == "on":
            # On 16 GB cards leftovers from one image make the next one spill into shared memory and crawl
            # (100 s becomes 15+ min). Unloading after every image costs a model reload but keeps each one fast.
            free_memory(comfy, unload=True)
            time.sleep(3)  # let ComfyUI act on it before the next image is queued
        done += 1
        took = time.time() - started
        fastest = min(fastest, took) if fastest else took
        print(f"[{n}/{len(jobs)}] {name}: saved ({time.time() - started:.0f}s) - {u['title']}")
    print(f"\nDone: {done} made, {skipped} already existed, {failed} failed. Images are in {OUT}")
    if redo:
        choose_options(units, args.variants)


if __name__ == "__main__":
    main()
