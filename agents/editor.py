from tools.llm import ask_llm


def final_polish(seo_meta: str, article: str) -> str:
    """Editor agent: produces the final polished article in Markdown."""
    prompt = f"""You are a senior editor. Produce the final publication-ready
article in Markdown:
1. Start with the SEO metadata as three bold lines: **Title:**, **Meta description:**,
   **Keywords:** (plain Markdown, not a code block).
2. Then the article, starting with a single "# " title heading and using "## "
   headings for the main sections. Fix grammar, typos and flow. Do not add new facts.
3. Do NOT include any images or image syntax.
Return only the final Markdown.

SEO metadata:
{seo_meta}

Article:
{article}"""
    return ask_llm(prompt)