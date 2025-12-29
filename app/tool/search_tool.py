from langchain_community.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """
    Realiza uma busca na web usando DuckDuckGo (ddgs).
    Retorna os principais resultados em texto.
    """
    results_text = []

    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=5
        )

        for r in results:
            title = r.get("title", "")
            url = r.get("href", "")
            body = r.get("body", "")
            results_text.append(
                f"Título: {title}\nResumo: {body}\nLink: {url}"
            )

    return "\n\n".join(results_text)

