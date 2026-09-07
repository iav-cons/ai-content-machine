#!/usr/bin/env python3
"""Derive a project's control stack from projects/<id>/sources/ (questionnaire,
entity analysis, ICP, writer master prompt) using the Anthropic API — the same
factoring done by hand for the first project. Writes control files; the caller
opens a PR for human review. Writer persona is copied verbatim, never rewritten."""
import argparse, json, os, re, sys, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FILES = ["source-context.md", "claims-compliance.md", "voice-tone.md",
         "audience-icp.md", "strategy-hypotheses.md", "project-brief.md"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--project", required=True); a = ap.parse_args()
    key = os.environ.get("ANTHROPIC_API_KEY") or sys.exit("ANTHROPIC_API_KEY not set")
    pdir = os.path.join(ROOT, "projects", a.project); sdir = os.path.join(pdir, "sources")
    import yaml; cfg = yaml.safe_load(open(os.path.join(pdir, "project.yml")))
    docs, persona = [], None
    for fn in sorted(os.listdir(sdir)):
        fp = os.path.join(sdir, fn)
        if fn == "README.md" or not os.path.isfile(fp) or fn.lower().endswith((".xlsx", ".png", ".pdf")): continue
        txt = open(fp, encoding="utf-8", errors="replace").read()
        if re.search(r"persona|master-prompt", fn, re.I): persona = txt
        docs.append(f"===== SOURCE FILE: {fn} =====\n{txt}")
    if persona:
        fm = (f'---\nproject_id: "{a.project}"\nstage: control\nniche: "{cfg.get("niche")}"\n'
              f'location: "{cfg.get("location")}"\n---\n')
        open(os.path.join(pdir, "control", "writer-persona.md"), "w", encoding="utf-8").write(fm + persona)
    templates = "\n\n".join(f"===== TEMPLATE {f} =====\n" + open(os.path.join(ROOT, "engine/templates/project/control", f), encoding="utf-8").read() for f in FILES)
    prompt = (f"You factor a business questionnaire + audience + entity inputs into a content engine's control files. "
              f"Project: {cfg.get('name')} | id {a.project} | niche {cfg.get('niche')} | location {cfg.get('location')} | domain {cfg.get('domain')}.\n"
              f"RULES: one fact, one home. source-context.md = confirmed business/market TRUTH only (no voice, no audience, no architecture, no claim rules); "
              f"keep its 'Source validation' checklist with all boxes ticked [x]; end with an 'Operations truth' section listing EXACTLY these lines, "
              f"each ending ': [REQUIRES CONFIRMATION]' unless the sources state the fact: 'Fulfillment partner legal name + license number', 'License class / category actually held', 'Equipment or brands the partner actually installs / sells', 'Certifications genuinely held', 'Emergency or after-hours reality', 'Business phone, form destination, service email, hours, who answers calls', 'Google Business Profile', 'Real price ranges', 'Financing lender name + terms language', 'Maintenance / recurring agreement price and terms' (put local specifics such as the licensing body in parentheses AFTER the label). "
              f"claims-compliance.md = ALL never-claim rules; its 'Never-claim patterns (machine-scanned)' list = short literal strings that must never appear. "
              f"voice-tone.md = voice, reading level, terminology table, and 'Banned phrases (machine-scanned)' literal list. audience-icp.md = the WHO (merge ICP + questionnaire audience answers). "
              f"strategy-hypotheses.md = hubs/page wishlists/KPIs/admission checks as validate-don't-obey. project-brief.md = goal, model, priorities. "
              f"Never invent facts; unknown = [REQUIRES CONFIRMATION]. Every file starts with the frontmatter shown in the templates (fill project_id/niche/location). "
              f"OUTPUT FORMAT (nothing else): for each file:\n=====FILE: <name>=====\n<content>\n=====END=====\n\nTEMPLATES:\n{templates}\n\nSOURCES:\n" + "\n\n".join(docs))
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        data=json.dumps({"model": os.environ.get("QC_MODEL", "claude-sonnet-4-6"), "max_tokens": 24000,
                         "messages": [{"role": "user", "content": prompt[:180000]}]}).encode())
    with urllib.request.urlopen(req, timeout=600) as r:
        text = "".join(b.get("text", "") for b in json.load(r).get("content", []))
    n = 0
    for m in re.finditer(r"=====FILE: (.+?)=====\n(.*?)\n=====END=====", text, re.S):
        name = m.group(1).strip()
        if name in FILES:
            open(os.path.join(pdir, "control", name), "w", encoding="utf-8").write(m.group(2).strip() + "\n"); n += 1
    if n < 4: sys.exit(f"factoring produced only {n} files — check sources/ and retry /factor")
    print(f"wrote {n} control files" + (" + writer-persona.md" if persona else ""))

if __name__ == "__main__":
    main()
