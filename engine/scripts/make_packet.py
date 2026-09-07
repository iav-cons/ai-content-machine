#!/usr/bin/env python3
"""Job packet generator (workflow spec §10, §11, §13, §16, §19).

Every packet is assembled by this script from the canonical files — never by hand,
never from chat memory (spec §23.8). The script refuses to generate a packet the
state machine forbids (spec §19).

Usage:
  python engine/scripts/make_packet.py --project <project-id> --stage entity_research
  python engine/scripts/make_packet.py --project X --stage brief --page-id PG-004
  Revision (spec §13):
  python engine/scripts/make_packet.py --project X --stage content_cluster \
      --revision-of projects/X/cluster/content-cluster-v1.md \
      --failures projects/X/qc/hard-qc-report.md --attempt 2
Options: --stdout (print instead of writing to projects/<id>/jobs/)
"""
import argparse
import datetime as dt
import os
import re
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

STAGES = {
    "entity_research": {
        "out": "research/entity-research-v{v}.md",
        "instructions": "entity-research.md",
        "inputs": ["sources_seed"],
    },
    "content_cluster": {
        "out": "cluster/content-cluster-v{v}.md",
        "instructions": "content-cluster.md",
        "inputs": ["canonical:entity_research"],
    },
    "url_map": {
        "out": "url-map/url-map-v{v}.yml",
        "instructions": "url-map.md",
        "inputs": ["canonical:content_cluster"],
    },
    "serp_research": {
        "out": "pages/{page}/serp-research-v{v}.md",
        "instructions": "serp-research.md",
        "inputs": ["canonical:entity_research", "page_record"],
    },
    "brief": {
        "out": "briefs/{page}/brief-v{v}.md",
        "instructions": "content-brief.md",
        "inputs": ["canonical:entity_research", "canonical:query_triage",
                   "page_record", "page_files"],
    },
    "content": {
        "out": "content/{page}/content-v{v}.md",
        "instructions": "content-generation.md",
        "inputs": ["canonical:brief", "page_record"],
    },
    "page_review": {
        "out": "pages/{page}/page-review-v{v}.md",
        "instructions": "page-review.md",
        "inputs": ["canonical:brief", "canonical:content", "page_record", "perf_files"],
    },
    "query_triage": {
        "out": "pages/{page}/query-triage-v{v}.md",
        "instructions": "query-triage.md",
        "inputs": ["canonical:entity_research", "page_record", "page_files",
                   "optfile:control/query-ownership.md"],
    },
}
STAGES["entity_research"]["inputs"] += ["optfile:control/strategy-hypotheses.md"]
STAGES["content_cluster"]["inputs"] += ["optfile:control/strategy-hypotheses.md"]
STAGES["url_map"]["inputs"] += ["optfile:control/strategy-hypotheses.md"]
STAGES["brief"]["inputs"] += ["optfile:control/audience-icp.md",
                              "optfile:control/voice-tone.md",
                              "optfile:control/query-ownership.md"]
STAGES["content"]["inputs"] += ["optfile:control/writer-persona.md",
                                "optfile:control/audience-icp.md",
                                "optfile:control/voice-tone.md"]
GLOBAL_RULES = ["engine/rules/entity-content-cluster-ruleset.md",
                "engine/rules/mirena-operating-rules.md"]
BASE_INPUTS = (["global:" + p for p in GLOBAL_RULES] +
               ["file:control/project-brief.md", "file:control/source-context.md",
                "file:control/operating-rules.md", "file:control/project-state.md",
                "optfile:control/claims-compliance.md"])


def die(msg):
    print(f"REFUSED: {msg}", file=sys.stderr)
    sys.exit(1)


BINARY_EXT = (".xlsx", ".xls", ".png", ".jpg", ".jpeg", ".pdf", ".zip", ".gif")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_data(path):
    """Data drops may be binary; inline text, stub binaries."""
    if path.lower().endswith(BINARY_EXT):
        return ("[binary data file — not inlined. Provide a .csv or .md export "
                "of this data for the worker; see docs/operator-runbook.md "
                "data-drop conventions.]")
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def next_version(abs_dir, prefix):
    if not os.path.isdir(abs_dir):
        return 1
    vs = [int(m.group(1)) for f in os.listdir(abs_dir) if f.startswith(prefix)
          for m in [re.search(r"-v(\d+)\.", f)] if m]
    return (max(vs) + 1) if vs else 1


def artifact_meta(text):
    """Frontmatter (md) or meta block (yml) of an artifact, as a dict."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            try:
                fm = yaml.safe_load(text[4:end])
                return fm if isinstance(fm, dict) else {}
            except yaml.YAMLError:
                return {}
    try:
        d = yaml.safe_load(text)
        if isinstance(d, dict) and isinstance(d.get("meta"), dict):
            return d["meta"]
    except yaml.YAMLError:
        pass
    return {}


def staleness_violations(inputs, rules):
    """Inputs whose research data is older than allowed (data decays — SERP most)."""
    today = dt.date.today()
    bad = []
    for label, content in inputs:
        meta = artifact_meta(content)
        stage = meta.get("stage")
        if stage not in rules:
            continue
        created = str(meta.get("created") or "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", created):
            m = re.search(r"JOB-(\d{4})(\d{2})(\d{2})-", str(meta.get("job_id") or ""))
            if not m:
                continue
            created = "-".join(m.groups())
        age = (today - dt.date.fromisoformat(created)).days
        if age > rules[stage]:
            bad.append(f"{label}: {stage} data is {age} days old "
                       f"(max {rules[stage]} in engine/qc-config.yml)")
    return bad


def gate(stage, cfg, page_id):
    st = cfg.get("statuses") or {}
    canon = cfg.get("canonical") or {}
    if stage == "entity_research":
        return
    if stage == "content_cluster" and st.get("entity_research") != "approved":
        die("entity_research is not approved — Content Cluster cannot start (spec §19)")
    if stage == "url_map" and st.get("content_cluster") != "approved":
        die("content_cluster is not approved — URL Map cannot start (spec §19)")
    if stage in ("serp_research", "brief", "content", "page_review", "query_triage"):
        if st.get("url_map") != "approved":
            die("url_map is not approved — page production cannot start (spec §19)")
        if not page_id:
            die(f"--page-id is required for stage '{stage}'")
    if stage == "content" and f"brief:{page_id}" not in canon:
        die(f"no approved canonical brief for {page_id} — content cannot start "
            f"(spec §14, §23.12)")
    if stage == "page_review" and f"content:{page_id}" not in canon:
        die(f"no approved canonical content for {page_id} — page review needs the "
            f"live content (spec §16)")


def source_validation_gate(proj_dir):
    p = os.path.join(proj_dir, "control", "source-context.md")
    if not os.path.exists(p):
        die("control/source-context.md missing — source validation not done (spec §3)")
    if "- [ ]" in read(p):
        die("source validation checklist in control/source-context.md has unchecked "
            "items — complete it before issuing AI jobs (spec §3)")


def page_record(cfg, proj_dir, page_id):
    canon = (cfg.get("canonical") or {}).get("url_map")
    if not canon:
        die("no approved canonical url_map in project.yml (spec §16)")
    data = yaml.safe_load(read(os.path.join(ROOT, canon)))
    for p in data.get("pages", []):
        if p.get("id") == page_id:
            return canon, yaml.safe_dump(p, sort_keys=False, allow_unicode=True)
    die(f"page '{page_id}' not found in approved url map {canon}")


def gather_inputs(stage, cfg, proj, proj_dir, page_id):
    """Return list of (label, content)."""
    out = []
    canon = cfg.get("canonical") or {}
    specs = BASE_INPUTS + STAGES[stage]["inputs"]
    for spec in specs:
        if spec.startswith("global:"):
            rel = spec[7:]
            path = os.path.join(ROOT, rel)
            if os.path.exists(path):
                content = read(path)
                if "PASTE YOUR" in content:
                    print(f"note: {rel} is still a placeholder — global rules NOT "
                          f"inlined into this packet", file=sys.stderr)
                else:
                    out.append((f"{rel}  [GLOBAL RULES — HIGHEST AUTHORITY]", content))
        elif spec.startswith("optfile:"):
            rel = spec[8:]
            path = os.path.join(proj_dir, rel)
            if os.path.exists(path):
                out.append((f"projects/{proj}/{rel}", read(path)))
        elif spec.startswith("file:"):
            rel = spec[5:]
            path = os.path.join(proj_dir, rel)
            if not os.path.exists(path):
                die(f"required input missing: projects/{proj}/{rel} (spec §12)")
            out.append((f"projects/{proj}/{rel}", read(path)))
        elif spec.startswith("canonical:"):
            key = spec[10:]
            key = f"{key}:{page_id}" if key in ("brief", "content", "query_triage") else key
            rel = canon.get(key)
            if not rel:
                if key.startswith("query_triage:") and key in canon:
                    out.append((f"{key}  [SKIPPED — operator chose --skip-triage]",
                                "No approved query-triage exists for this page. "
                                "Derive coverage from the raw query files below; "
                                "flag this in the Document Usage Check."))
                    continue
                die(f"no approved canonical '{key}' in project.yml — downstream work "
                    f"cannot use unapproved inputs (spec §16, §23.12)")
            out.append((f"{rel}  [APPROVED CANONICAL]", read(os.path.join(ROOT, rel))))
        elif spec == "page_record":
            src, rec = page_record(cfg, proj_dir, page_id)
            out.append((f"page record {page_id} from {src}  [APPROVED CANONICAL]", rec))
        elif spec == "sources_seed":
            sdir = os.path.join(proj_dir, "sources")
            if os.path.isdir(sdir):
                for fn in sorted(os.listdir(sdir)):
                    fp = os.path.join(sdir, fn)
                    if not os.path.isfile(fp) or fn == ".gitkeep":
                        continue
                    if fn.startswith(("entity-analysis", "serp--", "paa--",
                                      "fanout--")):
                        out.append((f"projects/{proj}/sources/{fn}  "
                                    f"[PRE-PROJECT SEED — high authority]",
                                    read_data(fp)))
        elif spec == "page_files":
            pdir = os.path.join(proj_dir, "pages", page_id)
            if os.path.isdir(pdir):
                for fn in sorted(os.listdir(pdir)):
                    fp = os.path.join(pdir, fn)
                    if os.path.isfile(fp):
                        out.append((f"projects/{proj}/pages/{page_id}/{fn}", read_data(fp)))
        elif spec == "perf_files":
            pdir = os.path.join(proj_dir, "pages", page_id, "performance")
            files = ([f for f in sorted(os.listdir(pdir))
                      if os.path.isfile(os.path.join(pdir, f)) and f != ".gitkeep"]
                     if os.path.isdir(pdir) else [])
            if not files:
                die(f"no performance data in projects/{proj}/pages/{page_id}/performance/"
                    f" — drop GSC/analytics exports there before a page review")
            for fn in files:
                out.append((f"projects/{proj}/pages/{page_id}/performance/{fn}",
                            read_data(os.path.join(pdir, fn))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--stage", required=True, choices=sorted(STAGES))
    ap.add_argument("--page-id")
    ap.add_argument("--attempt", type=int, default=1)
    ap.add_argument("--revision-of", help="path to the previous output being revised")
    ap.add_argument("--failures", help="path to the exact QC failure report")
    ap.add_argument("--allow-stale", action="store_true",
                    help="consciously accept inputs older than the staleness limits")
    ap.add_argument("--skip-triage", action="store_true",
                    help="consciously generate a brief without an approved "
                         "query-triage for this page")
    ap.add_argument("--slim", action="store_true",
                    help="session-mode packet: omit global rules and control files "
                         "already loaded in the project chat via the bootstrap")
    ap.add_argument("--stdout", action="store_true")
    a = ap.parse_args()

    proj_dir = os.path.join(ROOT, "projects", a.project)
    cfg_path = os.path.join(proj_dir, "project.yml")
    if not os.path.exists(cfg_path):
        die(f"projects/{a.project}/project.yml not found")
    cfg = yaml.safe_load(read(cfg_path))
    if cfg.get("project_id") != a.project:
        die("project.yml project_id does not match folder (spec §18)")

    qc_cfg_path = os.path.join(ROOT, "engine", "qc-config.yml")
    qc_cfg = (yaml.safe_load(read(qc_cfg_path)) or {}) if os.path.exists(qc_cfg_path) else {}
    max_attempts = qc_cfg.get("max_attempts", 3)
    if a.attempt > max_attempts:
        die(f"attempt {a.attempt} exceeds max {max_attempts} — human_review_required, "
            f"the system stops (spec §13)")
    if a.revision_of and not a.failures:
        die("revision packets require --failures with the exact QC failure list (spec §13)")

    source_validation_gate(proj_dir)
    gate(a.stage, cfg, a.page_id)

    out_rel = STAGES[a.stage]["out"].replace("{page}", a.page_id or "")
    out_dir = os.path.join(proj_dir, os.path.dirname(out_rel))
    prefix = os.path.basename(STAGES[a.stage]["out"]).split("-v{v}")[0]
    version = next_version(out_dir, prefix)
    out_rel = out_rel.replace("{v}", str(version))
    output_file = f"projects/{a.project}/{out_rel}"
    today = dt.date.today().isoformat()

    instr_path = os.path.join(proj_dir, "control", "instructions",
                              STAGES[a.stage]["instructions"])
    if not os.path.exists(instr_path):
        die(f"stage instructions missing: {instr_path}")
    instructions = read(instr_path)
    if "PASTE YOUR TESTED" in instructions:
        die(f"{instr_path} still contains the placeholder — paste your tested prompt "
            f"before issuing this job")

    job_id = dt.datetime.now().strftime(f"JOB-%Y%m%d-%H%M%S-{a.stage}")
    fm_lines = [
        "---",
        f'project_id: "{a.project}"',
        f"stage: {a.stage}",
    ]
    if a.page_id:
        fm_lines.append(f"page_id: {a.page_id}")
    fm_lines += [
        f"version: {version}",
        "status: proposed",
        f'niche: "{cfg.get("niche")}"',
        f'location: "{cfg.get("location")}"',
        f"created: {today}",
        f"job_id: {job_id}",
        f"attempt: {a.attempt}",
        "---",
    ]
    frontmatter = "\n".join(fm_lines)
    if out_rel.endswith((".yml", ".yaml")):
        frontmatter = ("meta:\n"
                       f"  project_id: {a.project}\n"
                       f"  stage: {a.stage}\n"
                       f"  version: {version}\n"
                       f"  status: proposed\n"
                       f'  niche: "{cfg.get("niche")}"\n'
                       f'  location: "{cfg.get("location")}"\n'
                       f"  created: {today}\n"
                       f"  job_id: {job_id}\n"
                       f"  attempt: {a.attempt}")

    revision_block = ""
    if a.revision_of:
        revision_block = (
            "================================================================\n"
            f"REVISION JOB (attempt {a.attempt} of {max_attempts} — spec §13)\n"
            "================================================================\n\n"
            "This is a revision, not a rewrite. Fix ONLY the exact QC failures listed\n"
            "below. Keep everything else in the previous output unchanged (spec §23.13).\n\n"
            "----- EXACT QC FAILURES -----\n"
            f"{read(os.path.join(ROOT, a.failures)).strip()}\n"
            "----- END QC FAILURES -----\n\n"
            "----- PREVIOUS OUTPUT (being revised) -----\n"
            f"{read(os.path.join(ROOT, a.revision_of)).strip()}\n"
            "----- END PREVIOUS OUTPUT -----\n"
        )

    if a.stage == "brief" and not a.skip_triage:
        if not (cfg.get("canonical") or {}).get(f"query_triage:{a.page_id}"):
            die(f"no approved query-triage for {a.page_id} — run the "
                f"query_triage stage first (PAA/fan-out verdicts are the "
                f"brief's coverage obligations), or pass --skip-triage to "
                f"consciously proceed without one")
    if a.stage == "brief" and a.skip_triage:
        cfg.setdefault("canonical", {}).setdefault(
            f"query_triage:{a.page_id}", None)
    inputs = gather_inputs(a.stage, cfg, a.project, proj_dir, a.page_id)
    if a.slim:
        keep_prefixes = (f"projects/{a.project}/pages/",
                         f"projects/{a.project}/control/query-ownership.md")
        slim = []
        for label, content in inputs:
            path = label.split("  [")[0]
            if (path.startswith(keep_prefixes)
                    or "[APPROVED CANONICAL]" in label
                    or "[SKIPPED" in label
                    or "[PRE-PROJECT SEED" in label
                    or "page record" in label):
                slim.append((label, content))
        canon_state = "\n".join(
            [f"- {k}: {v}" for k, v in sorted((cfg.get("canonical") or {}).items())])
        stat_state = "\n".join(
            [f"- {k}: {v}" for k, v in sorted((cfg.get("statuses") or {}).items())])
        slim.insert(0, ("CANONICAL STATE on main (repo is truth; if this chat "
                        "remembers different versions, THESE win)",
                        f"Stage statuses:\n{stat_state}\n\nApproved canonical "
                        f"artifacts:\n{canon_state}"))
        inputs = slim

    stale = staleness_violations(inputs, qc_cfg.get("staleness_max_age_days") or {})
    if stale and not a.allow_stale:
        die("stale inputs — refresh the research first, or pass --allow-stale to "
            "accept consciously:\n  " + "\n  ".join(stale))
    if stale:
        revision_block = ("STALE INPUTS ACCEPTED BY OPERATOR:\n"
                          + "\n".join(f"- {s}" for s in stale)
                          + "\n\n" + revision_block)

    golden_block = ""
    gname = "url_map.yml" if a.stage == "url_map" else f"{a.stage}.md"
    gpath = os.path.join(proj_dir, "control", "golden", gname)
    if os.path.exists(gpath):
        golden_block = (
            "================================================================\n"
            f"GOLDEN EXAMPLE — an approved, best-in-class {a.stage} output.\n"
            "Match its structure, depth and quality. Do NOT copy its content,\n"
            "entities or niche facts — your output is for the PROJECT above.\n"
            "================================================================\n\n"
            f"{read(gpath).strip()}\n\n")

    inputs_txt = "\n\n".join(
        f"----- FILE: {label} -----\n{content.strip()}\n----- END FILE -----"
        for label, content in inputs
    )

    tpl = read(os.path.join(ROOT, "engine", "templates", "packets",
                            "packet-template.md"))
    packet = (tpl
              .replace("{{JOB_ID}}", job_id)
              .replace("{{PROJECT_ID}}", a.project)
              .replace("{{PROJECT_NAME}}", str(cfg.get("name", "")))
              .replace("{{NICHE}}", str(cfg.get("niche", "")))
              .replace("{{LOCATION}}", str(cfg.get("location", "")))
              .replace("{{STAGE}}", a.stage)
              .replace("{{PAGE_LINE}}", f"PAGE: {a.page_id}\n" if a.page_id else "")
              .replace("{{ATTEMPT}}", f"{a.attempt} of {max_attempts}")
              .replace("{{OUTPUT_FILE}}", output_file)
              .replace("{{OUTPUT_FRONTMATTER}}", frontmatter)
              .replace("{{REVISION_BLOCK}}", revision_block)
              .replace("{{GOLDEN_BLOCK}}", golden_block)
              .replace("{{INSTRUCTIONS}}", instructions.strip())
              .replace("{{INPUTS}}", inputs_txt))

    if a.stdout:
        print(packet)
    else:
        jobs_dir = os.path.join(proj_dir, "jobs")
        os.makedirs(jobs_dir, exist_ok=True)
        out_path = os.path.join(jobs_dir, f"{job_id}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(packet)
        print(f"Packet written: projects/{a.project}/jobs/{job_id}.md")
        print(f"Expected worker output: {output_file}")


if __name__ == "__main__":
    main()
