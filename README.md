# Project Live Working
https://content-pipeline-sarthak-sarkar.streamlit.app/

# Multi-Agent Content Creation Pipeline

**Course:** CE509 Agentic AI | **PS No.:** 18 | **Domain:** Content, Media & Creativity

A pipeline of six cooperating AI agents that researches a topic, writes a draft,
fact-checks it, optimizes it for SEO, generates visual descriptions, and produces
final polished content.

## Architecture

```mermaid
flowchart LR
    A[Topic] --> B[Researcher]
    B --> C[Writer]
    C --> D[Fact-Checker]
    D -- unsupported claims --> C
    D -- passed --> E[SEO Optimizer]
    E --> F[Visual Describer]
    F --> G[Editor]
    G --> H[Final Markdown in outputs/]
```

| Agent | Role |
|---|---|
| Researcher | Searches the web (DuckDuckGo) and summarizes facts with source URLs |
| Writer | Writes the first draft from the research notes, and revises it when the fact-checker finds problems |
| Fact-Checker | Checks every claim against the research notes and returns PASS or FAIL with issues |
| SEO Optimizer | Adds title, meta description, keywords, and improves headings |
| Visual Describer | Writes alt text and image-generation prompts for each section |
| Editor | Merges everything into the final polished article |

The Writer and Fact-Checker form a feedback loop (up to 2 revision rounds).

## Tech stack
Python, Google Gemini API (`google-genai`), `ddgs` for web search, `python-dotenv`.

## Setup
1. Clone the repo and open the folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your own Gemini API key from aistudio.google.com.
4. Run: `python main.py --topic "Benefits of solar energy in India"`

The API key is read only from `.env`, which is excluded from Git.

## Output
The final article is saved to `outputs/<topic>.md`, with the fact-check report in
`outputs/<topic>-factcheck.txt`. A sample is included in the `outputs/` folder.

## Project structure
```
agents/     researcher, writer, fact_checker, seo, visual, editor
tools/      llm.py (Gemini wrapper with retries), search.py (web search)
pipeline.py orchestration and the fact-check loop
main.py     command-line entry point
outputs/    generated articles
```
