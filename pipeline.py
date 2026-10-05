import os
import re
from agents.researcher import research
from agents.writer import write_draft, revise_draft
from agents.fact_checker import check_facts
from agents.seo import optimize_seo
from agents.visual import describe_visuals
from agents.editor import final_polish

MAX_REVISIONS = 2


def run_pipeline(topic: str) -> str:
    print("[1/6] Researching...")
    notes = research(topic)

    print("[2/6] Writing draft...")
    draft = write_draft(topic, notes)

    report = ""
    for round_no in range(MAX_REVISIONS + 1):
        print(f"[3/6] Fact-checking (round {round_no + 1})...")
        passed, report = check_facts(draft, notes)
        if passed or round_no == MAX_REVISIONS:
            break
        print("      Issues found, sending back to writer...")
        draft = revise_draft(topic, notes, draft, report)

    print("[4/6] Optimizing for SEO...")
    seo = optimize_seo(topic, draft)

    print("[5/6] Generating visual descriptions...")
    visuals = describe_visuals(seo["article"])

    print("[6/6] Final editing...")
    final = final_polish(seo["meta"], seo["article"], visuals)

    os.makedirs("outputs", exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    with open(f"outputs/{slug}.md", "w", encoding="utf-8") as f:
        f.write(final)
    with open(f"outputs/{slug}-factcheck.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Done. Saved to outputs/{slug}.md")
    return final