from tools.llm import ask_llm


def check_facts(draft: str, research_notes: str):
    """Fact-checker agent: verifies the draft against the research notes.
    Returns (passed: bool, report: str)."""
    prompt = f"""You are a strict fact-checker. Compare the article against the
research notes. List every factual claim in the article (numbers, rankings,
dates, statements) that is NOT supported by the research notes.

Reply in this exact format:
VERDICT: PASS   (if every claim is supported)
or
VERDICT: FAIL   (if any claim is unsupported)
ISSUES:
- one bullet per unsupported claim, with a short explanation

Research notes:
{research_notes}

Article:
{draft}"""
    report = ask_llm(prompt)
    passed = "VERDICT: PASS" in report.upper()
    return passed, report