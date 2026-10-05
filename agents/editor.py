from tools.llm import ask_llm


def final_polish(seo_meta: str, article: str, visuals: str) -> str:
    """Editor agent: merges everything into the final polished content."""
    prompt = f"""You are a senior editor. Produce the final publication-ready
article in Markdown:
1. Start with the SEO metadata (title, meta description, keywords) as a short block.
2. Then the article, with grammar, typos and flow fixed. Do not add new facts.
3. Insert each image from the visuals list at its position as:
   ![alt text](image-placeholder) followed by an italic caption line.
Return only the final Markdown.

SEO metadata:
{seo_meta}

Article:
{article}

Visuals:
{visuals}"""
    return ask_llm(prompt)