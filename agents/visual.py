from tools.llm import ask_llm


def describe_visuals(article: str) -> list:
    """Visual agent: returns a list of {"alt": ..., "prompt": ...} dicts."""
    prompt = f"""You are a visual content designer. Read the article and propose
4 images: one hero image for the whole article, then one for each of the first
3 main sections.

Return EXACTLY 4 lines and nothing else, each in this format:
IMAGE: <one-sentence alt text> || <detailed image generation prompt>

Article:
{article}"""
    raw = ask_llm(prompt)
    visuals = []
    for line in raw.splitlines():
        line = line.strip().lstrip("-*• ").strip()
        if line.upper().startswith("IMAGE:") and "||" in line:
            alt, _, img_prompt = line[6:].partition("||")
            visuals.append({"alt": alt.strip(), "prompt": img_prompt.strip()})
    return visuals