#!/usr/bin/env python3
"""Ingestion tool: convert a markdown URL/content map (13-column tables, the
MIRENA output format) into a schema-v2 url-map yml artifact for any project.

  python engine/scripts/convert_urlmap.py --src <map.md> --project <id> \
      [--version 1] [--status proposed|approved] [--created YYYY-MM-DD] \
      [--job-id JOB-XXXX]

Niche/location come from the project's project.yml. Handles the 9-column FAQ
table variant. Location-type pages whose `owns` text does not mention their
own location entity get it prefixed (keeps sibling locations from claiming
identical territory — hard QC would fail them otherwise).
"""
import argparse
import datetime as dt
import os
import re

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TYPE_MAP = {"homepage": "homepage", "service": "service",
            "trust / service": "trust", "conversion": "conversion",
            "commercial": "commercial", "location": "location",
            "support": "support", "educational": "educational",
            "comparison": "comparison", "informational": "informational",
            "faq hub": "faq", "faq": "faq", "trust": "trust"}


def parse_parent(raw, known_prefix_ids):
    raw = raw.strip()
    if raw.lower() in ("root", "", "none", "null"):
        return None
    m = re.match(r"(?i)child of\s+([A-Z0-9-]+)", raw)
    tok = m.group(1) if m else raw
    if re.match(r"^[A-Z]+-\d+$", tok):
        return tok
    # bare prefix like "HOME" → HOME-001
    return f"{tok}-001"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--status", default="proposed",
                    choices=["proposed", "approved"])
    ap.add_argument("--created", default=dt.date.today().isoformat())
    ap.add_argument("--job-id", default="INGEST")
    a = ap.parse_args()

    proj_yml = os.path.join(ROOT, "projects", a.project, "project.yml")
    cfg = yaml.safe_load(open(proj_yml, encoding="utf-8"))

    pages = []
    for line in open(a.src, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|") or set(line) <= {"|", "-", " ", ":"}:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not re.match(r"^[A-Z]+-\d+$", cells[0]):
            continue
        if len(cells) == 13:
            (pid, cluster, name, url, ptype, pri, sec, ents, owns, mno,
             parent, prio, status) = cells
        elif len(cells) == 9:  # FAQ-style reduced table
            pid, cluster, name, url, ptype, pri, sec, prio, status = cells
            ents, owns = name, f"{pri} questions for the {cluster} cluster"
            mno = "Topics owned by dedicated pages — route with links"
            parent = "Child of HOME" if pid.endswith("-001") else \
                f"Child of {pid.split('-')[0]}-001"
        else:
            continue
        ent_list = [e.strip() for e in ents.split(",") if e.strip()]
        norm_type = TYPE_MAP.get(ptype.lower(), ptype.lower())
        if norm_type == "location" and ent_list and \
                ent_list[0].lower() not in owns.lower():
            owns = f"{ent_list[0]} {owns[0].lower()}{owns[1:]}"
        pages.append({"id": pid, "cluster": cluster, "name": name, "url": url,
                      "type": norm_type, "primary_intent": pri,
                      "secondary_intent": sec, "core_entities": ent_list,
                      "owns": owns, "must_not_own": mno,
                      "parent": parse_parent(parent, None),
                      "priority": prio, "status": "not_started"})

    ids = {p["id"] for p in pages}
    missing = [p["id"] for p in pages if p["parent"] and p["parent"] not in ids]
    doc = {"meta": {"project_id": a.project, "stage": "url_map",
                    "version": a.version, "status": a.status,
                    "niche": cfg.get("niche"), "location": cfg.get("location"),
                    "created": a.created, "job_id": a.job_id, "attempt": 1},
           "pages": pages}
    out = os.path.join(ROOT, "projects", a.project, "url-map",
                       f"url-map-v{a.version}.yml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Converted {dt.date.today().isoformat()} from "
                f"{os.path.basename(a.src)} by convert_urlmap.py.\n"
                "# Location-page 'owns' are prefixed with their location "
                "entity where the\n# source text was generic (sibling "
                "disambiguation).\n")
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True, width=90)
    print(f"{len(pages)} pages → {os.path.relpath(out, ROOT)}")
    if missing:
        print(f"WARNING missing parents: {missing}")


if __name__ == "__main__":
    main()
