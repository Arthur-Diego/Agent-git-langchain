# app/chains/agent_chain.py

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages

from app.prompt.system_prompt import SYSTEM_PROMPT

# MessagesPlaceholder(variable_name="chat_history")
# Insere automaticamente mensagens anteriores
# Mantém contexto da conversa
# Geralmente contém mensagens HumanMessage e AIMessage

# MessagesPlaceholder(variable_name="agent_scratchpad")
# registra pensamentos intermediários
# registra chamadas de função
#observa respostas das ferramentas
# ✳️ Passthrough
# Significa:
# “Passe os dados adiante sem alterar o input original”
# ✳️ Scratchpad
# É o bloco de anotações do agente.
# Ele guarda:
# decisões tomadas
# ferramentas chamadas
# respostas das ferramentas

def build_agent_chain(llm, tools):
    tools_json = [convert_to_openai_function(t) for t in tools]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    passthrough = RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        )
    )

    return (
        passthrough
        | prompt
        | llm.bind(functions=tools_json)
        | OpenAIFunctionsAgentOutputParser()
    )