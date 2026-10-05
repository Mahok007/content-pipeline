from tools.llm import ask_llm
from tools.search import web_search


def research(topic: str) -> str:
       """Research agent: searches the web, then summarizes the findings."""
       search_results = web_search(topic)
       prompt = f"""You are a research agent. Using ONLY the search results
   below, write 8-10 concise bullet points of accurate, useful facts about the topic.
   After each fact, add the source URL in brackets.

   Topic: {topic}

   Search results:
   {search_results}"""
       return ask_llm(prompt)