#!/usr/bin/env python3
"""ChatOps for the content engine. Every human action is a comment on a GitHub
issue; this script does the repo mechanics. Invoked by .github/workflows/
engine-ops.yml with the event payload. Pure file operations are separated
from GitHub calls so they can be tested locally (`--dry`).

Commands (first line of an issue comment):
  /bootstrap            post the project-chat bootstrap (parts) in this issue
  /packet <stage>       post a slim job packet for this page/stage
  /ingest  + ``` ... ``` place MIRENA's artifact → PR → Hard QC → Claude review
  /approve              approve the open PR for this issue: bookkeeping, merge,
                        SYNC message, next packet
  /sync <path>          post a SYNC message for any repo file
  /pages [P0|P1|P2|P3]  create one page issue per not_started page in the map
  /factor               (intake issue) derive the control stack from sources/
  /help                 list commands
Issue forms handled on open: new-project intake, truth update.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from make_packet import STAGES  # noqa: E402

NEXT = {"entity_research": "content_cluster", "content_cluster": "url_map",
        "url_map": None, "query_triage": "brief", "brief": "content",
        "content": None, "page_review": None, "serp_research": "query_triage"}
PHASE1 = ("entity_research", "content_cluster", "url_map")
PAGE_ID_RE = re.compile(r"\b([A-Z]{2,6}-\d{3})\b")
TODAY = dt.date.today().isoformat()


# ----------------------------------------------------------------- helpers
def sh(cmd, check=True, inp=None):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True,
                       text=True, input=inp, cwd=ROOT)
    if check and r.returncode:
        raise RuntimeError(f"{cmd}\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, text):
    fp = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(text)


def project_cfg(pid):
    return yaml.safe_load(read(f"projects/{pid}/project.yml"))


def save_cfg(pid, cfg):
    write(f"projects/{pid}/project.yml",
          yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True, width=100))


def fenced(body):
    """Text inside the outermost code fence; whole body (minus command) if none."""
    lines = body.splitlines()
    fences = [i for i, l in enumerate(lines) if l.strip().startswith("```")]
    if len(fences) >= 2:
        return "\n".join(lines[fences[0] + 1:fences[-1]]).strip()
    return "\n".join(l for l in lines[1:]).strip()


def frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            return yaml.safe_load(text[3:end]) or {}
    doc = yaml.safe_load(text) if text.lstrip().startswith("meta:") else None
    return (doc or {}).get("meta", {}) if doc else {}


def detect_project(issue_body, issue_title):
    m = re.search(r"(?im)^(?:###\s*)?project(?: id)?:?\s*\n?\s*`?([a-z0-9][a-z0-9-]+)`?", issue_body or "")
    if m and os.path.isdir(os.path.join(ROOT, "projects", m.group(1))):
        return m.group(1)
    projs = [d for d in os.listdir(os.path.join(ROOT, "projects"))
             if os.path.isdir(os.path.join(ROOT, "projects", d)) and not d.startswith(".")]
    if len(projs) == 1:
        return projs[0]
    raise RuntimeError("cannot tell which project — add a line `project: <id>` to the issue")


def detect_page(issue_title, issue_body):
    m = PAGE_ID_RE.search(issue_title or "") or PAGE_ID_RE.search(issue_body or "")
    return m.group(1) if m else None


# ------------------------------------------------------- pure file operations
def place_artifact(pid, text):
    fm = frontmatter(text)
    stage, ver = fm.get("stage"), fm.get("version")
    if stage not in STAGES or not ver:
        raise RuntimeError("artifact frontmatter needs `stage` (known) and `version`")
    if fm.get("status") != "proposed":
        raise RuntimeError("ingested artifacts must carry `status: proposed`")
    if int(fm.get("attempt", 1)) > 3:
        raise RuntimeError("attempt 4 does not exist — human_review_required (spec §13)")
    page = fm.get("page_id")
    out = STAGES[stage]["out"].format(page=page or "", v=ver)
    rel = f"projects/{pid}/{out}"
    write(rel, text.rstrip() + "\n")
    return rel, stage, page, int(fm.get("attempt", 1))


def approve_artifact(pid, rel, issue):
    text = read(rel)
    stage = frontmatter(text).get("stage")
    page = frontmatter(text).get("page_id")
    if "status: proposed" not in text:
        raise RuntimeError(f"{rel} is not a proposed artifact")
    write(rel, text.replace("status: proposed", "status: approved", 1))
    cfg = project_cfg(pid)
    key = f"{stage}:{page}" if page else stage
    cfg.setdefault("canonical", {})[key] = rel
    if stage in PHASE1:
        cfg.setdefault("statuses", {})[stage] = "approved"
    save_cfg(pid, cfg)
    log = f"projects/{pid}/control/change-log.md"
    write(log, read(log).rstrip() + f"\n{TODAY} | {stage} | User | Approved {rel} "
          f"via /approve (issue #{issue}). Canonical {key}.\n")
    if stage == "query_triage":
        add_ledger_rows(pid, text, page)
    return stage, page, key


def add_ledger_rows(pid, triage_text, page):
    m = re.search(r"(?is)ledger updates.*?\n((?:\s*[-*].*\n?)+)", triage_text)
    if not m:
        return
    ledger = f"projects/{pid}/control/query-ownership.md"
    existing = read(ledger)
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip().lstrip("-* ").strip()
        if not line:
            continue
        parts = re.split(r"\s*(?:→|->)\s*", line, maxsplit=1)
        q = parts[0].strip(" `")
        owner = parts[1].strip(" `") if len(parts) > 1 else page
        if owner.lower() in ("this page", ""):
            owner = page
        if q and q.lower() not in existing.lower():
            rows.append(f"| {q} | {owner} | include | {TODAY} |")
    if rows:
        write(ledger, existing.rstrip() + "\n" + "\n".join(rows) + "\n")


def apply_truth(pid, fields):
    """fields: {form label: value}. Replaces [REQUIRES CONFIRMATION] on the
    matching Operations-truth line of source-context.md."""
    rel = f"projects/{pid}/control/source-context.md"
    lines = read(rel).splitlines()
    changed = []
    for label, value in fields.items():
        value = (value or "").strip()
        if not value or value.lower() in ("_no response_", "unknown", "skip"):
            continue
        for i, l in enumerate(lines):
            if l.lstrip("- ").lower().startswith(label.lower()):
                j = i
                while "[REQUIRES CONFIRMATION]" not in lines[j] and j + 1 < len(lines) \
                        and lines[j + 1].startswith("  "):
                    j += 1  # marker may sit on a wrapped continuation line
                if "[REQUIRES CONFIRMATION]" in lines[j]:
                    lines[j] = lines[j].replace("[REQUIRES CONFIRMATION]", value)
                else:
                    lines[i] = l.rsplit(": ", 1)[0] + ": " + value
                changed.append(label)
                break
        num = re.search(r"(?:#|no\.?|number|licen[cs]e|ROC|DBPR|DOPL)\s*#?\s*([A-Z]{0,3}\d{4,9})", value, re.I)
        if num and label.lower().startswith("fulfillment partner"):
            cc = f"projects/{pid}/control/claims-compliance.md"
            if os.path.exists(os.path.join(ROOT, cc)):
                write(cc, read(cc).replace("#[number]", f"#{num.group(1)}"))
    write(rel, "\n".join(lines) + "\n")
    if changed:
        log = f"projects/{pid}/control/change-log.md"
        write(log, read(log).rstrip() + f"\n{TODAY} | Source context | User | "
              f"Truth update via form: {', '.join(changed)}.\n")
    return changed


def form_fields(body):
    """Issue-form body → {label: value}."""
    out = {}
    for m in re.finditer(r"###\s*(.+?)\s*\n+(.*?)(?=\n###\s|\Z)", body or "", re.S):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


# ------------------------------------------------------------- github side
class GH:
    def __init__(self, event):
        self.ev = event
        self.repo = os.environ.get("GITHUB_REPOSITORY", "")
        self.issue = (event.get("issue") or {}).get("number")
        self.title = (event.get("issue") or {}).get("title", "")
        self.body = (event.get("issue") or {}).get("body", "") or ""
        self.comment = ((event.get("comment") or {}).get("body") or "").strip()

    def say(self, text):
        sh(["gh", "issue", "comment", str(self.issue), "--repo", self.repo,
            "--body-file", "-"], inp=text)

    def post_blocks(self, text, header):
        for i, part in enumerate(chunk(text), 1):
            self.say(f"{header} (part {i})\n\n``````\n{part}\n``````")

    def branch_pr(self, branch, title, body):
        sh("git config user.name engine-bot && git config user.email engine-bot@users.noreply.github.com")
        sh(f"git checkout -B {branch}")
        sh("git add -A")
        sh(f'git commit -m "{title}"', check=False)
        sh(f"git push -u origin {branch} -f")
        existing = sh(["gh", "pr", "list", "--repo", self.repo, "--head", branch,
                       "--state", "open", "--json", "number", "--jq", ".[0].number"], check=False)
        if not existing:
            sh(["gh", "pr", "create", "--repo", self.repo, "--head", branch,
                "--base", "main", "--title", title, "--body", body])
            existing = sh(["gh", "pr", "list", "--repo", self.repo, "--head", branch,
                           "--json", "number", "--jq", ".[0].number"])
        return int(existing)

    def hard_qc_and_report(self):
        r = subprocess.run([sys.executable, "engine/scripts/hard_qc.py", "--ci",
                            "--base", "origin/main"], capture_output=True, text=True, cwd=ROOT)
        ok = r.returncode == 0
        sha = sh("git rev-parse HEAD")
        name = sh(["gh", "api", f"repos/{self.repo}/branches/main/protection/required_status_checks",
                   "--jq", ".contexts[0]"], check=False) or "hard-qc"
        sh(["gh", "api", f"repos/{self.repo}/check-runs", "-f", f"name={name}",
            "-f", f"head_sha={sha}", "-f", "status=completed",
            "-f", f"conclusion={'success' if ok else 'failure'}",
            "-f", "output[title]=Hard QC", "-f", f"output[summary]={r.stdout[:6000]}"],
           check=False)
        return ok, r.stdout

    def open_pr_for(self, branch_prefix):
        num = sh(["gh", "pr", "list", "--repo", self.repo, "--state", "open", "--json",
                  "number,headRefName", "--jq",
                  f'[.[]|select(.headRefName|startswith("{branch_prefix}"))][0].number'], check=False)
        return int(num) if num else None


def chunk(text, n=60000):
    return [text[i:i + n] for i in range(0, len(text), n)] or [""]


# ------------------------------------------------------------------ commands
def cmd_bootstrap(gh, pid):
    out = sh([sys.executable, "engine/scripts/make_session.py", "bootstrap",
              "--project", pid, "--stdout"])
    parts = [p.strip() for p in re.split(r"\n8{8}.*\n", out) if p.strip()]
    for i, p in enumerate(parts, 1):
        gh.say(f"**Bootstrap part {i}/{len(parts)}** — paste as one message into the "
               f"project chat; wait for MIRENA's READY reply before the next part.\n\n"
               f"``````\n{p}\n``````")


def post_packet(gh, pid, stage, page, extra=()):
    args = [sys.executable, "engine/scripts/make_packet.py", "--project", pid,
            "--stage", stage, "--slim", "--stdout", *extra]
    if page and stage not in PHASE1:
        args += ["--page-id", page]
    r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        gh.say(f"Packet for `{stage}` not generated:\n\n```\n{(r.stdout + r.stderr)[-3000:]}\n```")
        return False
    gh.post_blocks(r.stdout, f"**Job packet — {stage}{' ' + page if page else ''}** — "
                              f"paste into the project chat, then `/ingest` MIRENA's answer here")
    return True


def cmd_ingest(gh, pid):
    text = fenced(gh.comment)
    rel, stage, page, attempt = place_artifact(pid, text)
    branch = f"ingest/issue-{gh.issue}-{stage}"
    pr = gh.branch_pr(branch, f"{stage} {page or ''} v-artifact (issue #{gh.issue})",
                      f"Ingested from issue #{gh.issue} via /ingest. Attempt {attempt}.")
    ok, report = gh.hard_qc_and_report()
    if not ok:
        gh.say(f"**HARD QC: FAIL** on `{rel}` (PR #{pr})\n\n```\n{report[-5000:]}\n```")
        rev = subprocess.run([sys.executable, "engine/scripts/make_packet.py", "--project", pid,
                              "--stage", stage, "--slim", "--stdout", "--revision-of", rel,
                              "--failures", "-", "--attempt", str(attempt + 1)]
                             + (["--page-id", page] if page else []),
                             capture_output=True, text=True, cwd=ROOT, input=report)
        if rev.returncode == 0:
            gh.post_blocks(rev.stdout, "**Revision packet** — paste into the chat, then `/ingest` the fixed artifact")
        return
    verdict = subprocess.run([sys.executable, "engine/scripts/qual_review.py", "--project", pid,
                              "--artifact", rel], capture_output=True, text=True, cwd=ROOT)
    v = (verdict.stdout or verdict.stderr).strip()
    gh.say(f"**HARD QC: PASS** on `{rel}` (PR #{pr})\n\n{v}\n\n"
           f"If this is good: comment `/approve`. If not: fix in the chat and `/ingest` again "
           f"(attempt {attempt + 1} of 3).")


def cmd_approve(gh, pid):
    pr = gh.open_pr_for(f"ingest/issue-{gh.issue}-")
    if not pr:
        gh.say("No open ingest PR for this issue — `/ingest` an artifact first."); return
    branch = sh(["gh", "pr", "view", str(pr), "--repo", gh.repo, "--json", "headRefName",
                 "--jq", ".headRefName"])
    sh(f"git fetch origin {branch} && git checkout -B {branch} origin/{branch}")
    changed = sh("git diff --name-only origin/main...HEAD").splitlines()
    arts = [c for c in changed if re.search(r"-v\d+\.(md|yml)$", c)]
    if len(arts) != 1:
        gh.say(f"Expected exactly one artifact in PR #{pr}, found {arts}"); return
    stage, page, key = approve_artifact(pid, arts[0], gh.issue)
    sh("git config user.name engine-bot && git config user.email engine-bot@users.noreply.github.com")
    sh('git add -A && git commit -m "Approve: bookkeeping (status, canonical, change-log, ledger)"')
    sh(f"git push origin {branch}")
    ok, report = gh.hard_qc_and_report()
    if not ok:
        gh.say(f"Approval blocked by Hard QC:\n\n```\n{report[-4000:]}\n```"); return
    sh(["gh", "pr", "merge", str(pr), "--repo", gh.repo, "--squash", "--delete-branch"])
    sh("git checkout main && git pull origin main")
    sync = sh([sys.executable, "engine/scripts/make_session.py", "sync", "--project", pid,
               "--artifact", arts[0], "--stdout"])
    gh.post_blocks(sync, f"**APPROVED — {key}.** Paste this SYNC into the project chat")
    nxt = NEXT.get(stage)
    if nxt:
        post_packet(gh, pid, nxt, page)
    elif stage == "url_map":
        gh.say("Phase 1 complete. Comment `/pages P0` (or P1, all) to create the page issues.")
    elif stage == "content":
        sh(["gh", "issue", "edit", str(gh.issue), "--repo", gh.repo, "--add-label",
            "status:complete"], check=False)
        gh.say("Page complete. Content is canonical; publish hook fires if Make is wired.")


def cmd_pages(gh, pid, arg):
    cfg = project_cfg(pid)
    um = cfg.get("canonical", {}).get("url_map")
    if not um:
        gh.say("No approved URL map yet."); return
    pages = yaml.safe_load(read(um)).get("pages", [])
    want = arg.upper() if arg and arg.upper() != "ALL" else None
    made = 0
    for p in pages:
        if p.get("status") != "not_started" or (want and p.get("priority") != want):
            continue
        exists = sh(["gh", "issue", "list", "--repo", gh.repo, "--search",
                     f'"{p["id"]}" in:title', "--state", "all", "--json", "number",
                     "--jq", "length"], check=False)
        if exists and exists != "0":
            continue
        sh(["gh", "issue", "create", "--repo", gh.repo, "--title",
            f"[PAGE] {p['id']} — {p['name']} ({p.get('priority')})",
            "--body", f"project: {pid}\npage: {p['id']}\nurl: {p['url']}\n\n"
                      f"Owns: {p.get('owns')}\nMust not own: {p.get('must_not_own')}\n\n"
                      f"1. Upload SERP/PAA/fan-out files to `projects/{pid}/pages/{p['id']}/`\n"
                      f"2. Comment `/packet query_triage` here\n3. Paste into chat → `/ingest` the answer → `/approve`\n"
                      f"The next packets post themselves."], check=False)
        made += 1
    gh.say(f"Created {made} page issue(s).")


def cmd_factor(gh, pid):
    r = subprocess.run([sys.executable, "engine/scripts/factor_project.py", "--project", pid],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        gh.say(f"Factoring failed:\n\n```\n{(r.stdout + r.stderr)[-3000:]}\n```"); return
    pr = gh.branch_pr(f"factor/{pid}", f"Control stack for {pid} (derived from sources/)",
                      f"Derived by Claude from projects/{pid}/sources/. Review, edit if needed, merge.")
    ok, report = gh.hard_qc_and_report()
    gh.say(f"Control stack drafted → PR #{pr} ({'Hard QC PASS' if ok else 'Hard QC FAIL — see PR'}).\n\n"
           f"Read it on the PR's *Files changed* tab; merge when it reads true. "
           f"Then comment `/bootstrap` here to open the project chat.")


def on_issue_opened(gh):
    f = form_fields(gh.body)
    if "[NEW PROJECT]" in gh.title.upper():
        pid = re.sub(r"[^a-z0-9-]+", "-", f.get("Project id", "").lower()).strip("-")
        sh([sys.executable, "engine/scripts/new_project.py", "--id", pid, "--name",
            f.get("Project name", pid), "--domain", f.get("Domain", ""),
            "--niche", f.get("Niche", ""), "--location", f.get("Location / market", "")])
        write(f"projects/{pid}/sources/README.md",
              "Upload here: the filled source-context questionnaire, the entity analysis "
              "(file name starting `entity-analysis`), the ICP, and the writer master "
              "prompt (file name containing `persona` or `master-prompt`). Then comment "
              "`/factor` on the intake issue.\n")
        brief = f"projects/{pid}/control/project-brief.md"
        write(brief, read(brief).rstrip() + "\n\n## Starter block\n" +
              "\n".join(f"- {k}: {v}" for k, v in f.items()) + "\n")
        pr = gh.branch_pr(f"init/{pid}", f"Initialize project {pid}", f"From intake issue #{gh.issue}")
        gh.hard_qc_and_report()
        sh(["gh", "pr", "merge", str(pr), "--repo", gh.repo, "--squash", "--delete-branch"], check=False)
        gh.say(f"Project `{pid}` initialized. Now upload your four documents into "
               f"`projects/{pid}/sources/` (Add file → Upload files), then comment `/factor` here.")
    elif "[TRUTH]" in gh.title.upper():
        pid = detect_project(gh.body, gh.title)
        changed = apply_truth(pid, f)
        if not changed:
            gh.say("Nothing to apply — every field was empty/unknown."); return
        pr = gh.branch_pr(f"truth/issue-{gh.issue}", f"Truth update ({', '.join(changed)})",
                          f"From truth form issue #{gh.issue}")
        ok, report = gh.hard_qc_and_report()
        if ok:
            sh(["gh", "pr", "merge", str(pr), "--repo", gh.repo, "--squash", "--delete-branch"])
            sync = sh([sys.executable, "engine/scripts/make_session.py", "sync", "--project", pid,
                       "--artifact", f"projects/{pid}/control/source-context.md", "--stdout"])
            gh.post_blocks(sync, f"Applied: {', '.join(changed)}. Merged. Paste this SYNC into the chat if it is open")
        else:
            gh.say(f"Truth update blocked by Hard QC (PR #{pr}):\n\n```\n{report[-3000:]}\n```")


def route(event):
    gh = GH(event)
    if "comment" not in event:
        return on_issue_opened(gh)
    first = gh.comment.splitlines()[0].strip() if gh.comment else ""
    if not first.startswith("/"):
        return
    cmd, *rest = first.split()
    arg = rest[0] if rest else ""
    pid = detect_project(gh.body, gh.title)
    page = detect_page(gh.title, gh.body)
    try:
        if cmd == "/help":
            gh.say(__doc__)
        elif cmd == "/bootstrap":
            cmd_bootstrap(gh, pid)
        elif cmd == "/packet":
            post_packet(gh, pid, arg or "query_triage", page)
        elif cmd == "/ingest":
            cmd_ingest(gh, pid)
        elif cmd == "/approve":
            cmd_approve(gh, pid)
        elif cmd == "/sync":
            gh.post_blocks(sh([sys.executable, "engine/scripts/make_session.py", "sync",
                               "--project", pid, "--artifact", arg, "--stdout"]), "**SYNC** — paste into the chat")
        elif cmd == "/pages":
            cmd_pages(gh, pid, arg)
        elif cmd == "/factor":
            cmd_factor(gh, pid)
    except Exception as e:  # noqa: BLE001
        gh.say(f"`{cmd}` failed:\n\n```\n{str(e)[-3000:]}\n```")
        raise


if __name__ == "__main__":
    if "--dry" in sys.argv:  # local test hook: python engine_ops.py --dry <fn> args...
        fn = sys.argv[sys.argv.index("--dry") + 1]
        print(globals()[fn](*sys.argv[sys.argv.index("--dry") + 2:]))
    else:
        route(json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8")))
