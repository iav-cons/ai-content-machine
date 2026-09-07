#!/usr/bin/env python3
"""Hard QC — deterministic checks (workflow spec §12, §15, §17, §18, §19, §23).

Usage:
  CI (pull request):   python engine/scripts/hard_qc.py --ci --base origin/main
  Local (full scan):   python engine/scripts/hard_qc.py --local projects/<project-id>
  Save failure list:   add --report projects/<id>/qc/hard-qc-report.md

Exit code 0 = PASS, 1 = FAIL. The numbered failure list is the exact input for a
revision packet (spec §13).
"""
import argparse
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CFG_PATH = os.path.join(ROOT, "engine", "qc-config.yml")

ARTIFACT_DIRS = ("research/", "cluster/", "url-map/", "briefs/", "content/", "pages/")
PAGE_ARTIFACT_RE = re.compile(r"^(serp-research|page-review|query-triage)-v\d+\.md$")
PAGE_STATUSES = [
    "not_started", "researching", "research_complete", "brief_pending",
    "brief_qc", "awaiting_approval", "approved", "drafting", "draft_qc",
    "revision", "complete",
]
SLUG_SEG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRIAGE_VERDICTS = {"include_in_section", "include_in_faq", "mention_briefly",
                   "link_elsewhere", "exclude", "separate_page_idea",
                   "answer_with_correction"}
SECRET_PATTERNS = [
    re.compile(p) for p in [
        r"sk-[A-Za-z0-9_-]{20,}",
        r"AKIA[0-9A-Z]{16}",
        r"AIza[0-9A-Za-z_-]{35}",
        r"ghp_[A-Za-z0-9]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}",
        r"xox[baprs]-[A-Za-z0-9-]{10,}",
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    ]
]


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT)


def git_show(ref, path):
    r = sh(f"git show {ref}:{path}")
    return r.stdout if r.returncode == 0 else None


def load_yaml_text(text, where, qc):
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as e:
        qc.fail(f"{where}: invalid YAML — {e}")
        return None


def parse_frontmatter(text):
    """Return (frontmatter_dict_or_None, body). Frontmatter = leading --- block."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None, text[end + 4:]
    body = text[end + 4:]
    return (fm if isinstance(fm, dict) else None), body


class QC:
    def __init__(self):
        self.failures = []
        self.warnings = []

    def fail(self, msg):
        self.failures.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


def stage_of_path(rel):
    """Map an artifact path to its stage key."""
    parts = rel.split("/")
    if len(parts) < 3:
        return None
    sub = parts[2]
    if sub == "research":
        return "entity_research"
    if sub == "cluster":
        return "content_cluster"
    if sub == "url-map":
        return "url_map"
    if sub == "briefs":
        return "brief"
    if sub == "content":
        return "content"
    if sub == "pages":
        base = parts[-1]
        if base.startswith("serp-research-"):
            return "serp_research"
        if base.startswith("page-review-"):
            return "page_review"
        if base.startswith("query-triage-"):
            return "query_triage"
        return None
    return None


def canonical_key(stage, fm, rel, qc):
    if stage in ("brief", "content", "page_review", "query_triage"):
        pid = (fm or {}).get("page_id")
        if not pid:
            qc.fail(f"{rel}: {stage} artifact missing page_id in frontmatter")
            return None
        return f"{stage}:{pid}"
    return stage


def is_page_data(rel):
    """A file under pages/ that is not a versioned artifact = a data drop
    (SERP exports, PAA dumps, performance/ files). Scanned for contamination
    and secrets, but carries no frontmatter requirements."""
    parts = rel.split("/")
    return (len(parts) > 3 and parts[2] == "pages"
            and not PAGE_ARTIFACT_RE.match(parts[-1]))


def contamination_scan(rel, text, proj_id, proj_cfg, other_ids, qc):
    hay = norm(text)
    for oid in other_ids:
        if oid != proj_id and norm(oid) in hay:
            qc.fail(f"{rel}: contains other project's id '{oid}' (spec §18)")
    for term in (proj_cfg.get("contamination_terms") or []):
        if norm(term) and norm(term) in hay:
            qc.fail(f"{rel}: contains contamination term '{term}' (spec §3 source mismatch)")


def all_project_ids():
    pdir = os.path.join(ROOT, "projects")
    if not os.path.isdir(pdir):
        return []
    return [d for d in os.listdir(pdir)
            if os.path.isdir(os.path.join(pdir, d)) and not d.startswith("_")]


# ---------------------------------------------------------------- checks

def check_artifact_md(rel, text, proj_cfg, cfg, qc, other_ids, head_cfg):
    fm, body = parse_frontmatter(text)
    if fm is None:
        qc.fail(f"{rel}: missing or invalid YAML frontmatter")
        return None
    for field in cfg.get("frontmatter_required", []):
        if field not in fm:
            qc.fail(f"{rel}: frontmatter missing required field '{field}'")
    proj_id = rel.split("/")[1]
    if fm.get("project_id") != proj_id:
        qc.fail(f"{rel}: frontmatter project_id '{fm.get('project_id')}' does not match "
                f"folder '{proj_id}' (spec §18 project isolation)")
    if norm(fm.get("niche")) != norm(proj_cfg.get("niche")):
        qc.fail(f"{rel}: niche '{fm.get('niche')}' does not match project niche "
                f"'{proj_cfg.get('niche')}'")
    if norm(fm.get("location")) != norm(proj_cfg.get("location")):
        qc.fail(f"{rel}: location '{fm.get('location')}' does not match project location "
                f"'{proj_cfg.get('location')}'")
    status = fm.get("status")
    if status not in cfg.get("allowed_statuses", ["proposed", "approved"]):
        qc.fail(f"{rel}: status '{status}' not in allowed statuses")
    v = fm.get("version")
    if not (isinstance(v, int) and v >= 1):
        qc.fail(f"{rel}: version must be an integer >= 1")
    elif f"-v{v}." not in os.path.basename(rel):
        qc.fail(f"{rel}: filename must contain '-v{v}.' matching frontmatter version "
                f"(spec §15 versioning)")
    att = fm.get("attempt")
    if att is not None and isinstance(att, int) and att > cfg.get("max_attempts", 3):
        qc.fail(f"{rel}: attempt {att} exceeds max {cfg.get('max_attempts', 3)} — "
                f"human_review_required (spec §13)")
    stage = stage_of_path(rel)
    if fm.get("stage") not in (stage, None) and stage is not None:
        if fm.get("stage") != stage:
            qc.fail(f"{rel}: frontmatter stage '{fm.get('stage')}' does not match "
                    f"folder stage '{stage}'")
    for pat in cfg.get("required_headings", {}).get(stage, []):
        if not re.search(pat, body, re.M):
            qc.fail(f"{rel}: required heading pattern '{pat}' not found (spec §12)")
    created = fm.get("created")
    if created is not None and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(created)):
        qc.fail(f"{rel}: created must be a YYYY-MM-DD date")
    # contamination (spec §3, §18)
    contamination_scan(rel, text, proj_id, proj_cfg, other_ids, qc)
    # approved coherence (spec §14/§15): approved only inside an approval PR shape
    if status == "approved":
        if re.search(r"\[(REQUIRES CONFIRMATION|OPEN QUESTION)\]", text, re.I):
            qc.fail(f"{rel}: approved artifact still contains unresolved "
                    f"[REQUIRES CONFIRMATION]/[OPEN QUESTION] markers — resolve "
                    f"before approval (no unconfirmed facts become canonical)")
        key = canonical_key(stage, fm, rel, qc)
        if key and (head_cfg.get("canonical") or {}).get(key) != rel:
            qc.fail(f"{rel}: status approved but project.yml canonical['{key}'] does not "
                    f"point to this file — approval must update the canonical map (spec §16)")
    return fm


def check_url_map_yml(rel, text, proj_cfg, cfg, qc):
    data = load_yaml_text(text, rel, qc)
    if data is None:
        return
    meta = data.get("meta") or {}
    pages = data.get("pages")
    proj_id = rel.split("/")[1]
    if meta.get("project_id") != proj_id:
        qc.fail(f"{rel}: meta.project_id does not match folder '{proj_id}'")
    if norm(meta.get("niche")) != norm(proj_cfg.get("niche")):
        qc.fail(f"{rel}: meta.niche does not match project niche")
    if norm(meta.get("location")) != norm(proj_cfg.get("location")):
        qc.fail(f"{rel}: meta.location does not match project location")
    if meta.get("status") not in cfg.get("allowed_statuses"):
        qc.fail(f"{rel}: meta.status '{meta.get('status')}' invalid")
    if meta.get("status") == "approved" and re.search(
            r"\[(REQUIRES CONFIRMATION|OPEN QUESTION)\]", text, re.I):
        qc.fail(f"{rel}: approved url map still contains unresolved "
                f"[REQUIRES CONFIRMATION]/[OPEN QUESTION] markers")
    v = meta.get("version")
    if not (isinstance(v, int) and v >= 1):
        qc.fail(f"{rel}: meta.version must be an integer >= 1")
    elif f"-v{v}." not in os.path.basename(rel):
        qc.fail(f"{rel}: filename must contain '-v{v}.' matching meta.version")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(meta.get("created") or "")):
        qc.fail(f"{rel}: meta.created missing or not a YYYY-MM-DD date")
    if not isinstance(pages, list) or not pages:
        qc.fail(f"{rel}: 'pages' must be a non-empty list")
        return
    ids, urls, queries = {}, {}, {}
    required = ["id", "cluster", "name", "url", "type", "primary_intent",
                "secondary_intent", "core_entities", "owns", "must_not_own",
                "parent", "priority", "status"]
    for i, p in enumerate(pages):
        where = f"{rel} pages[{i}]"
        if not isinstance(p, dict):
            qc.fail(f"{where}: not a mapping")
            continue
        for fld in required:
            if fld not in p:
                qc.fail(f"{where}: missing field '{fld}' (spec §7)")
        pid, url = p.get("id"), p.get("url")
        if pid in ids:
            qc.fail(f"{where}: duplicate page ID '{pid}' (spec §7)")
        ids[pid] = p
        if url in urls:
            qc.fail(f"{where}: duplicate URL '{url}' (spec §7)")
        urls[url] = pid
        if isinstance(url, str):
            if url != "/":
                if not url.startswith("/"):
                    qc.fail(f"{where}: malformed slug '{url}' — must start with '/'")
                else:
                    for seg in url.strip("/").split("/"):
                        if not SLUG_SEG.match(seg):
                            qc.fail(f"{where}: malformed slug segment '{seg}' in '{url}'")
        else:
            qc.fail(f"{where}: url must be a string")
        # cannibalization guard: same primary_intent + same owns text = duplicate page
        q = norm(str(p.get("primary_intent", "")) + "|" + str(p.get("owns", "")))
        if q and q != "|":
            if q in queries:
                qc.fail(f"{where}: primary_intent + owns duplicates {queries[q]} — "
                        f"two pages claiming the same territory (spec §7)")
            queries[q] = pid
        if not str(p.get("owns", "")).strip():
            qc.fail(f"{where}: 'owns' is empty — every page needs declared "
                    f"ownership (cannibalization control)")
        if p.get("priority") not in cfg.get("allowed_priorities"):
            qc.fail(f"{where}: priority '{p.get('priority')}' invalid (spec §8)")
        if p.get("type") not in cfg.get("allowed_page_types"):
            qc.fail(f"{where}: type '{p.get('type')}' not in allowed page types")
        if p.get("status") not in PAGE_STATUSES:
            qc.fail(f"{where}: page status '{p.get('status')}' not a spec §8 status")
    # hierarchy: parents exist, no orphans among non-root, no cycles (spec §7)
    for pid, p in ids.items():
        parent = p.get("parent")
        if parent is not None and parent not in ids:
            qc.fail(f"{rel}: page '{pid}' has missing parent '{parent}' — orphan/broken "
                    f"hierarchy (spec §7)")
        seen, cur = set(), pid
        while cur is not None:
            if cur in seen:
                qc.fail(f"{rel}: hierarchy cycle involving '{pid}' (spec §7)")
                break
            seen.add(cur)
            cur = ids.get(cur, {}).get("parent") if cur in ids else None


def gate_for_stage(stage, fm):
    """Which predecessor must be approved before this stage may produce artifacts."""
    if stage == "content_cluster":
        return [("statuses", "entity_research")]
    if stage == "url_map":
        return [("statuses", "content_cluster")]
    if stage in ("brief", "serp_research"):
        return [("statuses", "url_map")]
    if stage == "content":
        pid = (fm or {}).get("page_id")
        return [("canonical", f"brief:{pid}")] if pid else [("statuses", "url_map")]
    if stage == "page_review":
        pid = (fm or {}).get("page_id")
        return [("canonical", f"content:{pid}")] if pid else [("statuses", "url_map")]
    if stage == "query_triage":
        return [("statuses", "url_map")]
    return []


def check_stage_gate(rel, stage, fm, base_cfg, qc):
    for kind, key in gate_for_stage(stage, fm):
        if kind == "statuses":
            if (base_cfg.get("statuses") or {}).get(key) != "approved":
                qc.fail(f"{rel}: {stage} work while '{key}' is not approved on main "
                        f"(spec §19 state machine, §23.12)")
        else:
            if key not in (base_cfg.get("canonical") or {}):
                qc.fail(f"{rel}: {stage} work while '{key}' has no approved canonical "
                        f"on main (spec §19, §23.12)")


def check_project_yml_transition(proj, base_cfg, head_cfg, changed, qc):
    order_ok = {"not_started": 0, "in_progress": 1, "approved": 2}
    for st, new in (head_cfg.get("statuses") or {}).items():
        old = (base_cfg.get("statuses") or {}).get(st, "not_started")
        if order_ok.get(new, -1) < order_ok.get(old, 0):
            qc.fail(f"projects/{proj}/project.yml: status '{st}' moved backwards "
                    f"{old} → {new} — not allowed (spec §19)")
        if new == "approved" and old != "approved":
            canon = (head_cfg.get("canonical") or {}).get(st)
            if not canon:
                qc.fail(f"projects/{proj}/project.yml: '{st}' set to approved without a "
                        f"canonical path (spec §16)")
            elif not os.path.exists(os.path.join(ROOT, canon)):
                qc.fail(f"projects/{proj}/project.yml: canonical['{st}'] = '{canon}' "
                        f"does not exist")
            if f"projects/{proj}/control/change-log.md" not in changed:
                qc.fail(f"projects/{proj}: approval of '{st}' has no change-log entry in "
                        f"this PR (spec §17, §23.15)")
    for key, path in (head_cfg.get("canonical") or {}).items():
        old = (base_cfg.get("canonical") or {}).get(key)
        if old and old != path and old in {}:  # placeholder, replacement handled below
            pass


def check_protected(proj, base_cfg, changed_status, qc):
    protected = set((base_cfg.get("canonical") or {}).values())
    for path, st in changed_status.items():
        if path in protected and st in ("M", "D"):
            qc.fail(f"{path}: modifies an APPROVED canonical artifact — approved files are "
                    f"immutable; propose a new version instead (spec §15, §23.3)")
        if path.endswith("control/change-log.md") and st == "D":
            qc.fail(f"{path}: change log deleted (spec §23.10)")


def check_changelog_append_only(proj, base_ref, qc):
    rel = f"projects/{proj}/control/change-log.md"
    head_path = os.path.join(ROOT, rel)
    if not os.path.exists(head_path):
        return
    old = git_show(base_ref, rel)
    if old is None:
        return
    new = open(head_path, encoding="utf-8").read()
    if not new.startswith(old.rstrip("\n")):
        qc.fail(f"{rel}: existing change-log lines were modified or removed — the log is "
                f"append-only (spec §17, §23.10)")


def scan_patterns_from(path, heading_re):
    """Collect '- pattern' lines under any heading matching heading_re."""
    if not os.path.isfile(path):
        return []
    pats, active = [], False
    for line in open(path, encoding="utf-8", errors="ignore").read().splitlines():
        if line.startswith("#"):
            active = bool(re.search(heading_re, line, re.I))
            continue
        if active and line.strip().startswith("- "):
            pat = line.strip()[2:].strip().strip("`")
            if pat:
                pats.append(pat)
    return pats


def check_claims_and_phrases(rel, text, proj_dir, qc):
    """Deterministic never-claim / banned-phrase scan (compliance + voice files)."""
    hay = norm(text)
    sources = [
        (os.path.join(proj_dir, "control", "claims-compliance.md"),
         r"machine.?scanned", "never-claim pattern (claims-compliance.md)"),
        (os.path.join(proj_dir, "control", "voice-tone.md"),
         r"machine.?scanned", "banned phrase (voice-tone.md)"),
    ]
    for path, head_re, label in sources:
        for pat in scan_patterns_from(path, head_re):
            if norm(pat) in hay:
                qc.fail(f"{rel}: contains {label}: '{pat}'")


def check_query_triage(rel, text, base_cfg, head_cfg, qc):
    """Every triage row: known verdict; link_elsewhere targets exist in the
    approved URL map; separate_page_idea rows carry a note."""
    canon = (base_cfg.get("canonical") or head_cfg.get("canonical") or {})
    page_ids = set()
    um = canon.get("url_map")
    if um and os.path.exists(os.path.join(ROOT, um)):
        try:
            data = yaml.safe_load(open(os.path.join(ROOT, um), encoding="utf-8"))
            page_ids = {p.get("id") for p in (data.get("pages") or [])}
        except yaml.YAMLError:
            pass
    rows = [l for l in text.splitlines()
            if l.strip().startswith("|") and not set(l.strip()) <= {"|", "-", " ", ":"}]
    if len(rows) < 2:
        qc.fail(f"{rel}: no triage table found — every collected query needs a row")
        return
    seen = set()
    for i, row in enumerate(rows[1:], 1):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 4:
            qc.fail(f"{rel} row {i}: needs columns query | source | verdict | destination/note")
            continue
        query, source, verdict, dest = cells[0], cells[1], cells[2], cells[3]
        nq = norm(query)
        if nq in seen:
            qc.fail(f"{rel} row {i}: duplicate query '{query}'")
        seen.add(nq)
        if norm(source) not in ("paa", "fanout-chatgpt", "fanout-gemini", "serp",
                                "related-search", "manual"):
            qc.fail(f"{rel} row {i}: unknown source '{source}' — label provenance "
                    f"(paa | fanout-chatgpt | fanout-gemini | serp | related-search | manual)")
        v = norm(verdict).replace(" ", "_")
        if v not in TRIAGE_VERDICTS:
            qc.fail(f"{rel} row {i}: verdict '{verdict}' not in allowed set "
                    f"{sorted(TRIAGE_VERDICTS)}")
        if v == "link_elsewhere" and page_ids and dest not in page_ids:
            qc.fail(f"{rel} row {i}: link_elsewhere target '{dest}' is not a page ID "
                    f"in the approved URL map")


def check_ownership_ledger(proj, qc):
    path = os.path.join(ROOT, "projects", proj, "control", "query-ownership.md")
    if not os.path.isfile(path):
        return
    seen = {}
    for i, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        if not line.strip().startswith("|") or set(line.strip()) <= {"|", "-", " ", ":"}:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or norm(cells[0]) in ("query", ""):
            continue
        nq = norm(cells[0])
        if nq in seen and seen[nq] != cells[1]:
            qc.fail(f"control/query-ownership.md line {i}: query '{cells[0]}' has two "
                    f"owners ({seen[nq]} and {cells[1]}) — one question, one owner")
        seen[nq] = cells[1]


def check_secrets(paths, qc):
    for rel in paths:
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            text = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                qc.fail(f"{rel}: possible secret/API key detected (spec §23.11)")
                break


# ---------------------------------------------------------------- drivers

def load_cfg():
    with open(CFG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_ci(base_ref):
    cfg = load_cfg()
    qc = QC()
    mb = sh(f"git merge-base {base_ref} HEAD").stdout.strip()
    if not mb:
        print(f"Cannot find merge-base with {base_ref}", file=sys.stderr)
        sys.exit(2)
    diff = sh(f"git diff --name-status --no-renames {mb} HEAD").stdout.strip()
    changed_status = {}
    for line in diff.splitlines():
        st, path = line.split("\t", 1)
        changed_status[path] = st[0]
    changed = [p for p, s in changed_status.items() if s != "D"]
    if cfg.get("secret_scan", True):
        check_secrets(changed, qc)
    projs = sorted({p.split("/")[1] for p in changed_status
                    if p.startswith("projects/") and len(p.split("/")) > 2})
    other_ids = all_project_ids()
    for proj in projs:
        cfg_rel = f"projects/{proj}/project.yml"
        head_txt = (open(os.path.join(ROOT, cfg_rel), encoding="utf-8").read()
                    if os.path.exists(os.path.join(ROOT, cfg_rel)) else None)
        if head_txt is None:
            qc.fail(f"{cfg_rel}: missing — every project must have project.yml (spec §20)")
            continue
        head_cfg = load_yaml_text(head_txt, cfg_rel, qc) or {}
        if head_cfg.get("project_id") != proj:
            qc.fail(f"{cfg_rel}: project_id does not match folder name (spec §18)")
        base_txt = git_show(mb, cfg_rel)
        base_cfg = (yaml.safe_load(base_txt) or {}) if base_txt else {}
        check_protected(proj, base_cfg, changed_status, qc)
        check_ownership_ledger(proj, qc)
        check_changelog_append_only(proj, mb, qc)
        check_project_yml_transition(proj, base_cfg, head_cfg, set(changed_status), qc)
        for rel, st in changed_status.items():
            if st == "D" or not rel.startswith(f"projects/{proj}/"):
                continue
            sub = rel.split("/", 2)[2] if len(rel.split("/")) > 2 else ""
            in_artifact_dir = any(sub.startswith(d) for d in ARTIFACT_DIRS)
            text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read()
            if in_artifact_dir and is_page_data(rel):
                contamination_scan(rel, text, proj, head_cfg, other_ids, qc)
            elif in_artifact_dir and rel.endswith(".md"):
                fm = check_artifact_md(rel, text, head_cfg, cfg, qc, other_ids, head_cfg)
                st = stage_of_path(rel)
                check_stage_gate(rel, st, fm, base_cfg, qc)
                if st in ("brief", "content", "page_review"):
                    check_claims_and_phrases(
                        rel, text, os.path.join(ROOT, "projects", proj), qc)
                if st == "query_triage":
                    check_query_triage(rel, text, base_cfg, head_cfg, qc)
            elif in_artifact_dir and rel.endswith((".yml", ".yaml")) and "url-map/" in rel:
                check_url_map_yml(rel, text, head_cfg, cfg, qc)
                check_stage_gate(rel, "url_map", None, base_cfg, qc)
    return qc


def run_local(target):
    cfg = load_cfg()
    qc = QC()
    other_ids = all_project_ids()
    targets = other_ids if target in ("all", "projects") else [os.path.basename(target.rstrip("/"))]
    for proj in targets:
        base = os.path.join(ROOT, "projects", proj)
        cfg_path = os.path.join(base, "project.yml")
        if not os.path.exists(cfg_path):
            qc.fail(f"projects/{proj}/project.yml: missing")
            continue
        head_cfg = load_yaml_text(open(cfg_path, encoding="utf-8").read(),
                                  cfg_path, qc) or {}
        if head_cfg.get("project_id") != proj:
            qc.fail(f"projects/{proj}/project.yml: project_id does not match folder name")
        check_ownership_ledger(proj, qc)
        for dirpath, _, files in os.walk(base):
            for fn in files:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT)
                sub = rel.split("/", 2)[2] if len(rel.split("/")) > 2 else ""
                if not any(sub.startswith(d) for d in ARTIFACT_DIRS):
                    continue
                text = open(full, encoding="utf-8", errors="ignore").read()
                if is_page_data(rel):
                    contamination_scan(rel, text, proj, head_cfg, other_ids, qc)
                elif rel.endswith(".md"):
                    fm = check_artifact_md(rel, text, head_cfg, cfg, qc, other_ids, head_cfg)
                    st = stage_of_path(rel)
                    if fm and fm.get("status") == "proposed":
                        check_stage_gate(rel, st, fm, head_cfg, qc)
                    if st in ("brief", "content", "page_review"):
                        check_claims_and_phrases(rel, text, base, qc)
                    if st == "query_triage":
                        check_query_triage(rel, text, head_cfg, head_cfg, qc)
                elif rel.endswith((".yml", ".yaml")) and "url-map/" in rel:
                    check_url_map_yml(rel, text, head_cfg, cfg, qc)
        if cfg.get("secret_scan", True):
            allf = [os.path.relpath(os.path.join(dp, f), ROOT)
                    for dp, _, fs in os.walk(base) for f in fs]
            check_secrets(allf, qc)
    return qc


def report(qc, out_path=None):
    lines = []
    if qc.failures:
        lines.append(f"HARD QC: FAIL — {len(qc.failures)} failure(s)")
        lines.append("")
        lines.append("Failures:")
        for i, f in enumerate(qc.failures, 1):
            lines.append(f"{i}. {f}")
    else:
        lines.append("HARD QC: PASS")
    if qc.warnings:
        lines.append("")
        lines.append("Warnings:")
        for w in qc.warnings:
            lines.append(f"- {w}")
    text = "\n".join(lines)
    print(text)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("```\n" + text + "\n```\n")
    return 1 if qc.failures else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ci", action="store_true", help="diff-driven mode for pull requests")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--local", help="project dir (or 'all') for a full local scan")
    ap.add_argument("--report", help="write the PASS/FAIL report to this file")
    a = ap.parse_args()
    if a.ci:
        qc = run_ci(a.base)
    elif a.local:
        qc = run_local(a.local)
    else:
        ap.error("use --ci or --local <project-dir|all>")
    sys.exit(report(qc, a.report))


if __name__ == "__main__":
    main()
