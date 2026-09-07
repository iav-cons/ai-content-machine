#!/usr/bin/env python3
"""STATUS BOARD generator (spec §20 — "open it months later and see everything").

Walks every projects/*/project.yml and (optionally, with --with-issues via the
GitHub CLI) the open page issues, and produces one markdown overview: Phase 1
stage statuses, canonical artifacts, the page queue by status label, and stalls
(awaiting_manual_worker older than --stall-days, plus anything in
human_review_required).

Usage:
  python engine/scripts/status_report.py --out status.md
  python engine/scripts/status_report.py --with-issues --out status.md --stalls stalls.json
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STAGES = ["entity_research", "content_cluster", "url_map"]
MARK = {"approved": "approved ✅", "in_progress": "in progress 🟡",
        "not_started": "not started ⚪"}


def load_projects():
    rows = []
    pdir = os.path.join(ROOT, "projects")
    if not os.path.isdir(pdir):
        return rows
    for d in sorted(os.listdir(pdir)):
        cfgp = os.path.join(pdir, d, "project.yml")
        if not os.path.isfile(cfgp):
            continue
        try:
            cfg = yaml.safe_load(open(cfgp, encoding="utf-8")) or {}
        except yaml.YAMLError:
            cfg = {"project_id": d, "_error": "project.yml unparseable"}
        rows.append(cfg)
    return rows


def gh_issues():
    try:
        r = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--limit", "500",
             "--json", "number,title,labels,updatedAt"],
            capture_output=True, text=True, cwd=ROOT, timeout=60)
        if r.returncode != 0:
            return None
        return json.loads(r.stdout)
    except (OSError, json.JSONDecodeError, subprocess.TimeoutExpired):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-issues", action="store_true")
    ap.add_argument("--stall-days", type=int, default=7)
    ap.add_argument("--out", default="status.md")
    ap.add_argument("--stalls", default="stalls.json")
    a = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    lines = [f"# STATUS BOARD — {now.strftime('%Y-%m-%d %H:%M UTC')}",
             "",
             "_Auto-generated. Do not edit — it is overwritten on every run._",
             ""]

    projects = load_projects()
    if not projects:
        lines.append("No projects found.")
    else:
        lines.append("## Phase 1 — stage statuses")
        lines.append("")
        lines.append("| Project | Entity research | Content cluster | URL map | "
                     "Approved artifacts |")
        lines.append("|---|---|---|---|---|")
        for cfg in projects:
            st = cfg.get("statuses") or {}
            canon = cfg.get("canonical") or {}
            cells = [MARK.get(st.get(s, "not_started"), st.get(s, "?"))
                     for s in STAGES]
            lines.append(f"| {cfg.get('project_id', '?')} | {cells[0]} | "
                         f"{cells[1]} | {cells[2]} | {len(canon)} |")
        lines.append("")

    stalls = []
    issues = gh_issues() if a.with_issues else None
    if issues is not None:
        counts = {}
        for it in issues:
            labels = [l["name"] for l in it.get("labels", [])]
            for l in labels:
                if l.startswith("status:"):
                    counts[l] = counts.get(l, 0) + 1
            updated = it.get("updatedAt", "")
            try:
                upd = dt.datetime.fromisoformat(updated.replace("Z", "+00:00"))
                age = (now - upd).days
            except ValueError:
                age = 0
            if "awaiting_manual_worker" in labels and age >= a.stall_days:
                stalls.append({"number": it["number"], "title": it["title"],
                               "label": "awaiting_manual_worker", "days": age})
            if "human_review_required" in labels:
                stalls.append({"number": it["number"], "title": it["title"],
                               "label": "human_review_required", "days": age})
        lines.append("## Page queue (open issues by status)")
        lines.append("")
        if counts:
            for l in sorted(counts):
                lines.append(f"- `{l}`: {counts[l]}")
        else:
            lines.append("No labeled page issues open.")
        lines.append("")
        lines.append(f"## Stalls (manual work waiting ≥ {a.stall_days} days, "
                     "or human review required)")
        lines.append("")
        if stalls:
            for s in stalls:
                lines.append(f"- #{s['number']} — {s['title']} "
                             f"(`{s['label']}`, {s['days']}d)")
        else:
            lines.append("None. 🎉")
        lines.append("")
    elif a.with_issues:
        lines.append("_Issue data unavailable (gh CLI failed) — showing file "
                     "state only._")
        lines.append("")

    text = "\n".join(lines) + "\n"
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)
    with open(a.stalls, "w", encoding="utf-8") as f:
        json.dump(stalls, f, indent=2)
    print(text)
    print(f"[written: {a.out}, {a.stalls} — {len(stalls)} stall(s)]",
          file=sys.stderr)


if __name__ == "__main__":
    main()
