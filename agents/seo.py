from tools.llm import ask_llm


def optimize_seo(topic: str, draft: str) -> dict:
    """SEO agent: adds SEO metadata and improves headings and keywords
    without changing any facts. Returns {"meta": str, "article": str}."""
    prompt = f"""You are an SEO specialist. For the article below, produce:

TITLE: an SEO-friendly title under 60 characters
META_DESCRIPTION: a meta description under 155 characters
KEYWORDS: 5-8 comma-separated target keywords
ARTICLE:
the full article rewritten with the primary keyword in the title and first
paragraph, clear H2/H3 headings, and natural keyword use.
Do NOT add, remove or change any facts.

Topic: {topic}

Article:
{draft}"""
    raw = ask_llm(prompt)
    meta, _, article = raw.partition("ARTICLE:")
    return {"meta": meta.strip(), "article": article.strip() or draft}