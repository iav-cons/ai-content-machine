#!/usr/bin/env python3
"""Qualitative QC via the Anthropic API (used inline by engine_ops after Hard QC).
Prints 'QUALITATIVE QC: PASS' or 'QUALITATIVE QC: FAIL' + numbered failures.
Never approves — a human still comments /approve."""
import argparse, json, os, sys, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
R = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, p)) else ""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--project", required=True); ap.add_argument("--artifact", required=True)
    a = ap.parse_args()
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("QUALITATIVE QC: SKIPPED — ANTHROPIC_API_KEY not set. Review manually against control/quality-checklist.md, then /approve."); return
    c = f"projects/{a.project}/control/"
    ctx = "\n\n".join(f"===== {n} =====\n{R(c + n)}" for n in
                      ["quality-checklist.md", "claims-compliance.md", "voice-tone.md", "source-context.md"])
    prompt = (f"You are the qualitative QC reviewer for a content-production engine. Judge the ARTIFACT "
              f"strictly against the checklist and rails. Output EXACTLY:\nQUALITATIVE QC: PASS\nor\n"
              f"QUALITATIVE QC: FAIL\n1. <exact, minimal, evidence-backed failure>\n2. ...\n"
              f"Then one short paragraph of rationale. Never rewrite the artifact. Never approve.\n\n"
              f"PROJECT CONTROL FILES:\n{ctx[:60000]}\n\nARTIFACT ({a.artifact}):\n{R(a.artifact)[:60000]}")
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        data=json.dumps({"model": os.environ.get("QC_MODEL", "claude-sonnet-4-6"), "max_tokens": 2000,
                         "messages": [{"role": "user", "content": prompt}]}).encode())
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            out = json.load(r)
        print("".join(b.get("text", "") for b in out.get("content", [])))
    except Exception as e:  # noqa: BLE001
        print(f"QUALITATIVE QC: UNAVAILABLE ({str(e)[:200]}). Review manually, then /approve.")

if __name__ == "__main__":
    main()
