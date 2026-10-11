"""Check every recorded word in audio/ against data/curriculum.json using local Whisper.

Run from the repository folder:
    py -3.12 tools\\audio\\check_pronunciation.py            (Windows)
    python3 tools/audio/check_pronunciation.py              (Mac/Linux)

Options:
    --model small|medium|large-v3   bigger = more accurate Thai, slower (default: small)
    --device cpu|cuda               use cuda only if you have an NVIDIA GPU set up for it

Writes tools/audio/pronunciation_report.csv and prints a summary to paste back.
The first run downloads the Whisper model (small is about 460 MB).
"""
import argparse
import csv
import difflib
import json
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
PASS = 0.75
REVIEW = 0.5


def load_audio(path):
    """Decode to 16 kHz mono float32 ourselves; faster-whisper's own decoder breaks on some PyAV versions."""
    import av
    import numpy as np
    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
    chunks = []
    with av.open(str(path)) as container:
        for frame in container.decode(audio=0):
            chunks.extend(f.to_ndarray().reshape(-1) for f in resampler.resample(frame))
    chunks.extend(f.to_ndarray().reshape(-1) for f in resampler.resample(None))
    return np.concatenate(chunks).astype(np.float32) / 32768.0


def normalize(text):
    text = text.replace("555", "ห้าห้าห้า").replace("...", "").replace("…", "")
    return re.sub(r"[\sๆ.,!?\"'()\-]", "", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="small")
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    curriculum = json.loads((ROOT / "data" / "curriculum.json").read_text(encoding="utf-8"))
    groups = json.loads((ROOT / "tools" / "audio" / "audio_groups.json").read_text(encoding="utf-8"))
    already_verified = {wid for g in groups[:5] for wid in g["ids"]}
    words = [w for lvl in curriculum for u in lvl["units"] for ls in u["lessons"] for w in ls["words"]]

    from faster_whisper import WhisperModel
    print(f"Loading Whisper '{args.model}' on {args.device} (first run downloads it)...")
    model = WhisperModel(args.model, device=args.device, compute_type="int8" if args.device == "cpu" else "float16")

    rows = []
    started = time.time()
    for i, w in enumerate(words, 1):
        path = ROOT / "audio" / f"{w['id']}.mp3"
        if not path.exists():
            rows.append({**w, "heard": "", "similarity": 0.0, "status": "MISSING FILE"})
            continue
        segments, _ = model.transcribe(load_audio(path), language="th", beam_size=5,
                                       condition_on_previous_text=False, vad_filter=False)
        heard = "".join(s.text for s in segments).strip()
        sim = difflib.SequenceMatcher(None, normalize(w["thai"]), normalize(heard)).ratio()
        status = "pass" if sim >= PASS else ("listen" if sim >= REVIEW else "LISTEN FIRST")
        rows.append({**w, "heard": heard, "similarity": round(sim, 2), "status": status})
        if i % 25 == 0 or i == len(words):
            print(f"  {i}/{len(words)} checked ({time.time() - started:.0f}s)")

    out = ROOT / "tools" / "audio" / "pronunciation_report.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["word_id", "thai", "english", "heard_by_whisper", "similarity", "status",
                     "already_verified_by_elevenlabs", "audio_file"])
        for r in rows:
            wr.writerow([r["id"], r["thai"], r["en"], r["heard"], r["similarity"], r["status"],
                         "yes" if r["id"] in already_verified else "no", f"audio/{r['id']}.mp3"])

    def summarize(subset, label):
        n = len(subset)
        p = sum(r["status"] == "pass" for r in subset)
        print(f"{label}: {p}/{n} pass ({100 * p / max(n, 1):.0f}%)")

    print("\n===== SUMMARY (paste everything below back to Claude) =====")
    print(f"model={args.model}")
    summarize([r for r in rows if r["id"] in already_verified], "Known-good calibration words")
    summarize([r for r in rows if r["id"] not in already_verified], "Words being checked")
    flagged = sorted((r for r in rows if r["id"] not in already_verified and r["status"] != "pass"),
                     key=lambda r: r["similarity"])
    print(f"Flagged for a listen: {len(flagged)}")
    for r in flagged:
        print(f"  {r['id']:10s} {r['similarity']:.2f}  expected={r['thai']}  heard={r['heard']}")
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
