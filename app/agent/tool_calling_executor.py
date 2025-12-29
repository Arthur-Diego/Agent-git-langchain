from langchain.schema.agent import AgentFinish

class ToolCallingExecutor:
    def __init__(self, agent_chain, tools, memory):
        self.agent_chain = agent_chain
        self.tools = {tool.name: tool for tool in tools}
        self.memory = memory

    def run(self, user_input: str):
        intermediate_steps = []

        while True:
            result = self.agent_chain.invoke({
                "input": user_input,
                "chat_history": self.memory.chat_memory.messages,
                "intermediate_steps": intermediate_steps,
            })

            # ✅ Finalizou
            if isinstance(result, AgentFinish):
                self.memory.save_context(
                    {"input": user_input},
                    {"output": result.return_values["output"]}
                )
                return result.return_values["output"]

            print("🧠 Ação:", result.tool)
            print("📥 Entrada:", result.tool_input)
            # 🔧 Chamou tool
            observation = self.tools[result.tool].run(
                result.tool_input
            )
            print("📤 Observation:", observation)

            intermediate_steps.append((result, observation))