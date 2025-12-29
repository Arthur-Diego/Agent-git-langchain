from app.llm.openain_llm import get_llm
from app.memory.conversation_memory import get_memory

from app.chain.agent_chain import build_agent_chain
from app.agent.tool_calling_executor import ToolCallingExecutor
from app.tool.search_tool import web_search
from app.tool.wikipedia_tool import get_wikipedia_tool


def main():
    llm = get_llm()
    memory = get_memory()

    tools = [
        web_search,
        get_wikipedia_tool(lang="pt"),
    ]

    agent_chain = build_agent_chain(llm, tools)
    agent_executor = ToolCallingExecutor(agent_chain, tools, memory)

    result = agent_executor.run("Quais foram as principais notícias sobre OpenAI nos últimos 7 dias?")
    print(result)


if __name__ == "__main__":
    main()