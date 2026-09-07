#!/usr/bin/env python3
"""Canary diff (worker drift alarm — MIRENA or any model update).

Compares two outputs of the SAME frozen canary packet run at different times and
reports structural drift: heading sequence, section count, per-section length,
frontmatter keys. Wording is expected to vary between runs; structure is not —
structural drift means the worker changed under you.

Usage:
  python engine/scripts/canary_diff.py benchmarks/mirena/2026-08.md benchmarks/mirena/2026-09.md
Exit 0 = structurally stable, 1 = drift detected.
"""
import argparse
import re
import sys

H_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)


def parse(path):
    text = open(path, encoding="utf-8").read()
    fm_keys = []
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            fm_keys = [l.split(":")[0].strip() for l in text[4:end].splitlines()
                       if ":" in l and not l.startswith(" ")]
            text = text[end + 4:]
    heads = [(len(m.group(1)), m.group(2).strip()) for m in H_RE.finditer(text)]
    # words per section (text between headings)
    sections = {}
    parts = H_RE.split(text)
    # parts = [pre, hashes, title, body, hashes, title, body, ...]
    for i in range(1, len(parts) - 2, 3):
        title = parts[i + 1].strip()
        body = parts[i + 2]
        sections[title] = len(body.split())
    total = len(text.split())
    return fm_keys, heads, sections, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--section-tolerance", type=float, default=0.35,
                    help="flag sections whose word count shifts more than this fraction")
    a = ap.parse_args()

    fm1, h1, s1, t1 = parse(a.old)
    fm2, h2, s2, t2 = parse(a.new)
    drift = []
    notes = []

    if fm1 != fm2:
        drift.append(f"frontmatter keys changed: {fm1} → {fm2}")

    titles1 = [t for _, t in h1]
    titles2 = [t for _, t in h2]
    missing = [t for t in titles1 if t not in titles2]
    added = [t for t in titles2 if t not in titles1]
    if missing:
        drift.append(f"headings removed: {missing}")
    if added:
        drift.append(f"headings added: {added}")
    common = [t for t in titles1 if t in titles2]
    if not missing and not added and titles1 != titles2:
        drift.append("headings reordered")
    if len(h1) != len(h2):
        notes.append(f"section count {len(h1)} → {len(h2)}")

    if t1:
        delta = (t2 - t1) / t1
        notes.append(f"total length {t1} → {t2} words ({delta:+.0%})")
        if abs(delta) > 0.5:
            drift.append(f"total length shifted {delta:+.0%} (>50%)")

    for title in common:
        w1, w2 = s1.get(title, 0), s2.get(title, 0)
        if w1 >= 30:
            d = (w2 - w1) / w1
            if abs(d) > a.section_tolerance:
                drift.append(f"section '{title}' length {w1} → {w2} words ({d:+.0%})")

    print(f"CANARY DIFF: {a.old}  →  {a.new}")
    for n in notes:
        print(f"  note: {n}")
    if drift:
        print(f"\nSTRUCTURAL DRIFT DETECTED — {len(drift)} signal(s):")
        for i, d in enumerate(drift, 1):
            print(f"{i}. {d}")
        print("\nThe worker likely changed (vendor update / model update). Re-validate "
              "quality on the next few real jobs before trusting output blindly.")
        sys.exit(1)
    print("\nSTRUCTURALLY STABLE — wording variance only, no drift signals.")
    sys.exit(0)


if __name__ == "__main__":
    main()
