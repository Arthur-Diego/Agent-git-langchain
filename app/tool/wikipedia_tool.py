from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


def get_wikipedia_tool(lang: str = "pt"):
    """
    Tool de consulta ao Wikipedia.
    """
    api_wrapper = WikipediaAPIWrapper(lang=lang)
    return WikipediaQueryRun(api_wrapper=api_wrapper)
