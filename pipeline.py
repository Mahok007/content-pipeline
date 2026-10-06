import os
import re
from agents.researcher import research
from agents.writer import write_draft, revise_draft
from agents.fact_checker import check_facts
from agents.seo import optimize_seo
from agents.visual import describe_visuals
from agents.editor import final_polish
from tools.image_gen import image_url

MAX_REVISIONS = 2


def insert_images(markdown: str, visuals: list) -> str:
    """Put the hero image after the main title and one image after each H2 heading."""
    if not visuals:
        return markdown

    def block(v):
        alt = v["alt"].replace("[", "").replace("]", "")
        return f"\n![{alt}]({image_url(v['prompt'])})\n*{alt}*\n"

    out, hero_done, idx = [], False, 1
    for line in markdown.split("\n"):
        out.append(line)
        if not hero_done and line.startswith("# "):
            out.append(block(visuals[0]))
            hero_done = True
        elif line.startswith("## ") and idx < len(visuals):
            out.append(block(visuals[idx]))
            idx += 1
    if not hero_done:
        out.insert(0, block(visuals[0]))
    return "\n".join(out)


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

    print("[5/6] Generating visuals...")
    visuals = describe_visuals(seo["article"])

    print("[6/6] Final editing...")
    final = final_polish(seo["meta"], seo["article"])
    final = insert_images(final, visuals)

    os.makedirs("outputs", exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    with open(f"outputs/{slug}.md", "w", encoding="utf-8") as f:
        f.write(final)
    with open(f"outputs/{slug}-factcheck.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Done. Saved to outputs/{slug}.md")
    return final