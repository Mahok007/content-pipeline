from tools.llm import ask_llm


def describe_visuals(article: str) -> str:
    """Visual agent: writes image descriptions for the article."""
    prompt = f"""You are a visual content designer. Read the article and propose
4 images (one hero image plus one for each main section).
For each image give:
- Position: where it goes in the article
- Alt text: one sentence for accessibility
- Image prompt: a detailed prompt for an AI image generator

Article:
{article}"""
    return ask_llm(prompt)