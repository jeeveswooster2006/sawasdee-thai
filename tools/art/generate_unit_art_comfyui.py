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
    "with pink insides, a short curled trunk, a chubby round body and short legs, a small ornate "
    "gold Thai flame-shaped ornament on top of the head, wearing a deep teal scarf with an ornate "
    "gold Thai temple-pattern border"
)
STYLE = (
    "Soft, polished children's picture-book illustration with gentle painterly shading, clean "
    "rounded shapes and warm friendly lighting. Simple uncluttered warm ivory background with "
    "subtle teal and gold accents. Landscape composition, Nong Chang is the clear focus. "
    "No lettering or writing anywhere."
)

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


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
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            raise SystemExit(f"ComfyUI rejected the request ({e.code}):\n{format_comfy_error(body)}")

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
        u = pick(unets, ("flux", "dev"), ("flux", "schnell"), ("flux",))
        g = pick(ggufs, ("flux", "dev"), ("flux", "schnell"), ("flux",))
        c = pick(ckpts, ("flux", "dev"), ("flux", "schnell"), ("flux",))
        if u:
            m.update(kind="unet", unet=u)
        elif g:
            m.update(kind="gguf", unet=g)
        elif c:
            m.update(kind="checkpoint", checkpoint=c)
        else:
            raise SystemExit("Couldn't find a Flux model in ComfyUI. Run with --list-models to see what's "
                             "installed, then pass --checkpoint or --unet with the exact file name.")
    if m["kind"] in ("unet", "gguf"):
        encoders = options(info, "DualCLIPLoader", "clip_name1")
        gguf_encoders = options(info, "DualCLIPLoaderGGUF", "clip_name1")
        m["t5"] = args.t5 or pick(encoders, ("t5xxl", "fp16"), ("t5xxl", "fp8"), ("t5",)) or pick(gguf_encoders, ("t5",))
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


def build_workflow(models, redux, ref_name, prompt, seed, args):
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
    w["9"] = {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": vae}}
    w["10"] = {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "sawasdee/unit"}}
    return w


def unit_seed(unit_id, variant, offset):
    return (int(hashlib.md5(unit_id.encode()).hexdigest()[:8], 16) + 1009 * variant + offset) % (2 ** 32)


def wait_for_image(comfy, prompt_id, timeout):
    started = time.time()
    while time.time() - started < timeout:
        hist = comfy.get_json(f"/history/{prompt_id}")
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
        time.sleep(2)
    raise RuntimeError(f"timed out after {timeout}s (raise --timeout if your GPU is slow)")


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
    ap.add_argument("--weight-dtype", default="default", help="UNETLoader weight dtype, e.g. fp8_e4m3fn to save VRAM")
    ap.add_argument("--steps", type=int, help="default 28 for Flux dev, 4 for schnell")
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--width", type=int, default=1216); ap.add_argument("--height", type=int, default=832)
    ap.add_argument("--reference", default=str(ROOT / "tools" / "art" / "mascot.png"))
    ap.add_argument("--no-redux", action="store_true")
    ap.add_argument("--redux-strength", type=float, default=0.35)
    ap.add_argument("--timeout", type=int, default=900, help="seconds to wait per image")
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
        raise SystemExit(f"Can't reach ComfyUI at {' or '.join(urls)}. Start ComfyUI first "
                         "(or pass --url if it uses a different address).")
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

    models = resolve_models(info, args)
    redux, redux_note = resolve_redux(info, args)
    print("Using:", ", ".join(f"{k}={v}" for k, v in models.items() if k not in ("kind",) and v not in (None, False)))
    print(f"Mascot reference (Flux Redux): {redux_note}")

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

    ref_name = comfy.upload_image(redux["reference"]) if redux and not args.dry_run else (redux and redux["reference"].name)
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(u, v) for u in units for v in range(args.variants)]
    print(f"{len(jobs)} image(s) to make for {len(units)} unit(s) -> {OUT}")
    webp_warned = False
    done = skipped = failed = 0
    for n, (u, v) in enumerate(jobs, 1):
        name = u["unit_id"] + ("" if v == 0 else f"-v{v + 1}")
        target = OUT / f"{name}.png"
        if target.exists() and not args.force:
            skipped += 1
            continue
        prompt = f"{CHARACTER}. Scene: Nong Chang {u['scene']}. {STYLE}"
        workflow = build_workflow(models, redux, ref_name, prompt, unit_seed(u["unit_id"], v, args.seed_offset), args)
        if args.dry_run:
            print(json.dumps(workflow, ensure_ascii=False, indent=1))
            return
        started = time.time()
        try:
            resp = comfy.post_json("/prompt", {"prompt": workflow, "client_id": "sawasdee-art"})
            target.write_bytes(wait_for_image(comfy, resp["prompt_id"], args.timeout))
        except RuntimeError as e:
            failed += 1
            print(f"[{n}/{len(jobs)}] {name}: FAILED - {e}")
            continue
        made_webp = save_web_copy(target)
        if not made_webp and not webp_warned:
            print("  (tip: `py -3.12 -m pip install pillow` to also get small .webp copies for the app)")
            webp_warned = True
        done += 1
        print(f"[{n}/{len(jobs)}] {name}: saved ({time.time() - started:.0f}s) - {u['title']}")
    print(f"\nDone: {done} made, {skipped} already existed, {failed} failed. Images are in {OUT}")


if __name__ == "__main__":
    main()
