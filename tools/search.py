from ddgs import DDGS


def web_search(query: str, max_results: int = 6) -> str:
       """Search the web and return results as plain text."""
       results = DDGS().text(query, max_results=max_results)
       lines = []
       for r in results:
           lines.append(f"- {r['title']} ({r['href']}): {r['body']}")
       return "\n".join(lines)