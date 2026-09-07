#!/usr/bin/env python3
"""Publish pipeline (extension of spec §22): after a merge to main, find content
files that just changed AND are the approved canonical for their page (spec §16
— only canonical content is ever published), and emit one JSON payload per page
for the Make webhook → WordPress.

Payload fields: project_id, project_name, domain, page_id, page_name, page_url,
version, path, created, content_markdown, content_html.

Usage (run from a checkout of main, fetch-depth >= 2):
  python engine/scripts/publish_notify.py            # diff HEAD^..HEAD
  python engine/scripts/publish_notify.py --all      # every canonical content file
Writes payloads/*.json + payloads/manifest.tsv (page_id, json path, name, url).
"""
import argparse
import json
import os
import re
import subprocess
import sys

import yaml

try:
    import markdown as md_lib
except ImportError:
    md_lib = None

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONTENT_RE = re.compile(r"^projects/([^/]+)/content/([^/]+)/content-v(\d+)\.md$")


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT)


def changed_files():
    if sh("git rev-parse HEAD^").returncode != 0:
        return []  # first commit — nothing to diff
    out = sh("git diff --name-only HEAD^ HEAD").stdout
    return [l.strip() for l in out.splitlines() if l.strip()]


def frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            try:
                fm = yaml.safe_load(text[4:end])
                return (fm if isinstance(fm, dict) else {}), text[end + 4:].lstrip("\n")
            except yaml.YAMLError:
                pass
    return {}, text


def page_record(cfg, page_id):
    canon = (cfg.get("canonical") or {}).get("url_map")
    if not canon:
        return {}
    try:
        data = yaml.safe_load(open(os.path.join(ROOT, canon), encoding="utf-8"))
        for p in data.get("pages", []):
            if p.get("id") == page_id:
                return p
    except (OSError, yaml.YAMLError):
        pass
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="emit payloads for every canonical content file")
    a = ap.parse_args()

    candidates = []
    if a.all:
        pdir = os.path.join(ROOT, "projects")
        for proj in (os.listdir(pdir) if os.path.isdir(pdir) else []):
            cfgp = os.path.join(pdir, proj, "project.yml")
            if not os.path.isfile(cfgp):
                continue
            cfg = yaml.safe_load(open(cfgp, encoding="utf-8")) or {}
            for key, rel in (cfg.get("canonical") or {}).items():
                if key.startswith("content:"):
                    candidates.append(rel)
    else:
        candidates = [f for f in changed_files() if CONTENT_RE.match(f)]

    outdir = os.path.join(ROOT, "payloads")
    os.makedirs(outdir, exist_ok=True)
    manifest = []
    for rel in candidates:
        m = CONTENT_RE.match(rel)
        if not m:
            continue
        proj, page_id, version = m.group(1), m.group(2), int(m.group(3))
        cfgp = os.path.join(ROOT, "projects", proj, "project.yml")
        if not os.path.isfile(cfgp):
            continue
        cfg = yaml.safe_load(open(cfgp, encoding="utf-8")) or {}
        if (cfg.get("canonical") or {}).get(f"content:{page_id}") != rel:
            print(f"skip (not canonical): {rel}", file=sys.stderr)
            continue
        full = os.path.join(ROOT, rel)
        if not os.path.isfile(full):
            continue
        fm, body = frontmatter(open(full, encoding="utf-8").read())
        rec = page_record(cfg, page_id)
        html = (md_lib.markdown(body, extensions=["extra"])
                if md_lib else "")
        payload = {
            "project_id": proj,
            "project_name": cfg.get("name"),
            "domain": cfg.get("domain"),
            "page_id": page_id,
            "page_name": rec.get("name"),
            "page_url": rec.get("url"),
            "version": version,
            "path": rel,
            "created": str(fm.get("created") or ""),
            "content_markdown": body,
            "content_html": html,
        }
        jpath = os.path.join(outdir, f"{proj}--{page_id}.json")
        with open(jpath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        manifest.append((page_id, os.path.relpath(jpath, ROOT),
                         str(rec.get("name") or ""), str(rec.get("url") or ""),
                         proj, str(version)))
        print(f"payload: {os.path.relpath(jpath, ROOT)}  ({rel})")

    with open(os.path.join(outdir, "manifest.tsv"), "w", encoding="utf-8") as f:
        for row in manifest:
            f.write("\t".join(row) + "\n")
    print(f"{len(manifest)} payload(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
