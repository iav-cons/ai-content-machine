#!/usr/bin/env python3
"""MIRENA session tools (one chat per project).

Bootstrap: everything the project chat needs, once, at the start of its life —
session rules, global rulesets, all control files, and current canonical state.
Sync: a short message announcing an approval/correction into the chat so the
chat's working memory matches canonical main (repo is truth).

Usage:
  python engine/scripts/make_session.py bootstrap --project <id> [--stdout]
  python engine/scripts/make_session.py sync --project <id> --artifact <repo-relative path>
"""
import argparse
import datetime as dt
import os
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GLOBAL_RULES = ["engine/rules/entity-content-cluster-ruleset.md",
                "engine/rules/mirena-operating-rules.md"]
CONTROL_ORDER = ["project-brief.md", "source-context.md", "operating-rules.md",
                 "claims-compliance.md", "voice-tone.md", "audience-icp.md",
                 "writer-persona.md", "strategy-hypotheses.md",
                 "quality-checklist.md", "project-state.md",
                 "query-ownership.md"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def block(label, content):
    return (f"----- FILE: {label} -----\n{content.strip()}\n----- END FILE -----")


def bootstrap(proj):
    proj_dir = os.path.join(ROOT, "projects", proj)
    cfg = yaml.safe_load(read(os.path.join(proj_dir, "project.yml")))
    header_path = os.path.join(ROOT, "engine", "templates", "session",
                               "bootstrap-header.md")
    header = read(header_path)
    for k, v in {"{{PROJECT_ID}}": proj, "{{PROJECT_NAME}}": str(cfg.get("name")),
                 "{{DOMAIN}}": str(cfg.get("domain")),
                 "{{NICHE}}": str(cfg.get("niche")),
                 "{{LOCATION}}": str(cfg.get("location")),
                 "{{DATE}}": dt.date.today().isoformat()}.items():
        header = header.replace(k, v)

    parts = [header]
    parts.append("=" * 64 + "\nGLOBAL RULES (highest authority — fixed)\n" + "=" * 64)
    for rel in GLOBAL_RULES:
        path = os.path.join(ROOT, rel)
        if os.path.exists(path):
            content = read(path)
            if "PASTE YOUR" in content:
                print(f"note: {rel} still a placeholder — bootstrap generated "
                      f"without it", file=sys.stderr)
                continue
            parts.append(block(f"{rel}  [GLOBAL RULES]", content))
    parts.append("=" * 64 + "\nPROJECT CONTROL FILES\n" + "=" * 64)
    cdir = os.path.join(proj_dir, "control")
    for fn in CONTROL_ORDER:
        path = os.path.join(cdir, fn)
        if os.path.exists(path):
            parts.append(block(f"projects/{proj}/control/{fn}", read(path)))
    canon = cfg.get("canonical") or {}
    stats = cfg.get("statuses") or {}
    state = ["=" * 64, "CANONICAL STATE ON MAIN (repo is truth)", "=" * 64,
             "Stage statuses:"]
    state += [f"- {k}: {v}" for k, v in sorted(stats.items())]
    state += ["", "Approved canonical artifacts (use these versions, no others):"]
    state += [f"- {k}: {v}" for k, v in sorted(canon.items())] or ["- none yet"]
    parts.append("\n".join(state))
    parts.append(
        "=" * 64 + "\nEND OF BOOTSTRAP\n" + "=" * 64 + "\n\n"
        "Confirm setup by replying with: the current workflow stage, the next\n"
        "allowed step, and any conflicts or missing inputs you detect. Do not\n"
        "start any stage work until a job packet arrives.")
    return "\n\n".join(parts)


def sync(proj, artifact):
    proj_dir = os.path.join(ROOT, "projects", proj)
    cfg = yaml.safe_load(read(os.path.join(proj_dir, "project.yml")))
    canon = cfg.get("canonical") or {}
    key = next((k for k, v in canon.items() if v == artifact), None)
    status = "APPROVED CANONICAL" if key else "recorded"
    body = read(os.path.join(ROOT, artifact)) if os.path.exists(
        os.path.join(ROOT, artifact)) else "(file not found on disk)"
    return (f"SYNC — repo state update ({dt.date.today().isoformat()})\n\n"
            f"The following artifact is now {status} on main"
            f"{f' as {key}' if key else ''}:\n{artifact}\n\n"
            "If your in-chat version of this artifact differs in ANY way from the\n"
            "text below, discard yours: the version below is authoritative from\n"
            "now on. Any earlier drafts of it in this chat are void.\n\n"
            + block(artifact + ("  [APPROVED CANONICAL]" if key else ""), body))


def emit_parts(text, a):
    blocks, cur = [], []
    for chunk in text.split("\n\n"):
        if sum(len(c) + 2 for c in cur) + len(chunk) > a.max_chars and cur:
            blocks.append("\n\n".join(cur))
            cur = []
        cur.append(chunk)
    if cur:
        blocks.append("\n\n".join(cur))
    n = len(blocks)
    ts = f"{dt.datetime.now():%Y%m%d-%H%M%S}"
    outdir = os.path.join(ROOT, "projects", a.project, "jobs")
    for i, body in enumerate(blocks, 1):
        head = (f"BOOTSTRAP PART {i}/{n} — hold. Do NOT act, analyze, or "
                f"summarize yet.\nReply with exactly: READY {i}/{n} — and "
                f"nothing else.\n"
                + ("FINAL PART: after reading this part, follow the "
                   "confirmation instruction at its end.\n" if i == n else "")
                + "=" * 64 + "\n\n")
        part = head + body
        if a.stdout:
            print(part)
            print("\n" + "8" * 8 + f" END PART {i}/{n} " + "8" * 8 + "\n")
        else:
            fn = f"BOOTSTRAP-{ts}-part{i}of{n}.md"
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, fn), "w", encoding="utf-8") as f:
                f.write(part)
            print(f"written: projects/{a.project}/jobs/{fn}")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["bootstrap", "sync"])
    ap.add_argument("--project", required=True)
    ap.add_argument("--artifact", help="repo-relative path (sync mode)")
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--max-chars", type=int, default=30000,
                    help="split the bootstrap into pasteable parts of at most "
                         "this many characters (0 = never split)")
    a = ap.parse_args()
    if a.mode == "bootstrap":
        text = bootstrap(a.project)
        name = f"BOOTSTRAP-{dt.datetime.now():%Y%m%d-%H%M%S}.md"
        if a.max_chars and len(text) > a.max_chars:
            return emit_parts(text, a)
    else:
        if not a.artifact:
            sys.exit("sync mode requires --artifact")
        text = sync(a.project, a.artifact)
        name = f"SYNC-{dt.datetime.now():%Y%m%d-%H%M%S}.md"
    if a.stdout:
        print(text)
    else:
        out = os.path.join(ROOT, "projects", a.project, "jobs", name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"written: projects/{a.project}/jobs/{name}")


if __name__ == "__main__":
    main()
