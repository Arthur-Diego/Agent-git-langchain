from langchain_community.tools import tool

@tool
def calculator(expression: str) -> str:
    """Resolve expressões matemáticas."""
    return str(eval(expression))