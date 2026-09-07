#!/usr/bin/env python3
"""Project initializer (workflow spec §2 — PROJECT INITIALIZATION).

Usage:
  python engine/scripts/new_project.py --id drain-cleaning-phoenix \
      --name "Drain Cleaning Phoenix" --domain draincleaningphoenix.com \
      --niche "Drain Cleaning" --location "Phoenix, AZ"

Creates projects/<id>/ from engine/templates/project with placeholders filled and
the spec §21 folder tree. Then: add source documents to sources/, complete the
source-validation checklist in control/source-context.md (spec §3), and paste your
tested prompts into control/instructions/ if the templates were still placeholders.
"""
import argparse
import datetime as dt
import os
import re
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TPL = os.path.join(ROOT, "engine", "templates", "project")
SUBDIRS = ["control", "control/instructions", "sources", "research", "cluster",
           "url-map", "briefs", "content", "pages", "qc", "jobs"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True, help="slug, e.g. my-service-my-city")
    ap.add_argument("--name", required=True)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--niche", required=True)
    ap.add_argument("--location", required=True)
    a = ap.parse_args()

    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", a.id):
        sys.exit("REFUSED: --id must be a lowercase slug (a-z, 0-9, hyphens)")
    dest = os.path.join(ROOT, "projects", a.id)
    if os.path.exists(dest):
        sys.exit(f"REFUSED: projects/{a.id} already exists — never overwrite (spec §23.3)")

    repl = {
        "{{PROJECT_ID}}": a.id,
        "{{PROJECT_NAME}}": a.name,
        "{{DOMAIN}}": a.domain,
        "{{NICHE}}": a.niche,
        "{{LOCATION}}": a.location,
        "{{DATE}}": dt.date.today().isoformat(),
    }

    for sub in SUBDIRS:
        os.makedirs(os.path.join(dest, sub), exist_ok=True)
        keep = os.path.join(dest, sub, ".gitkeep")
        if sub not in ("control", "control/instructions"):
            open(keep, "w").close()

    for dirpath, _, files in os.walk(TPL):
        rel = os.path.relpath(dirpath, TPL)
        for fn in files:
            src = os.path.join(dirpath, fn)
            out_dir = os.path.join(dest, rel) if rel != "." else dest
            os.makedirs(out_dir, exist_ok=True)
            with open(src, encoding="utf-8") as f:
                text = f.read()
            for k, v in repl.items():
                text = text.replace(k, v)
            with open(os.path.join(out_dir, fn), "w", encoding="utf-8") as f:
                f.write(text)

    print(f"Project initialized: projects/{a.id}")
    print("Next (spec §2/§3):")
    print(f"  1. Add source documents to projects/{a.id}/sources/")
    print(f"  2. Complete the checklist in projects/{a.id}/control/source-context.md")
    print(f"  3. Confirm tested prompts exist in projects/{a.id}/control/instructions/")
    print(f"  4. Fill contamination_terms in projects/{a.id}/project.yml")
    print("  5. Commit on a branch, open the project-initialization PR")


if __name__ == "__main__":
    main()
