from tools.llm import ask_llm
def write_draft(topic: str, research_notes: str) -> str:
    """Writer agent: turns research notes into a first draft."""
    prompt = f"""You are a content writer. Write a clear, engaging article
(about 500-700 words) on the topic below, using ONLY the research notes provided.
Include a title, an introduction, 3-4 sections with headings, and a conclusion.

Topic: {topic}

Research notes:
{research_notes}"""
    return ask_llm(prompt)
def revise_draft(topic: str, research_notes: str, draft: str, issues: str) -> str:
    """Writer agent: fixes the problems the fact-checker found."""
    prompt = f"""You are a content writer. Revise the article below to fix the
fact-check issues. Remove or correct any claim not supported by the research notes.
Keep the same structure and tone. Return only the revised article.

Topic: {topic}

Research notes:
{research_notes}

Fact-check issues:
{issues}

Current article:
{draft}"""
    return ask_llm(prompt)