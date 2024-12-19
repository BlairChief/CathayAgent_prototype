from phi.agent import Agent
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

load_dotenv()

class WebAgent:
    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[DuckDuckGo()],
            instructions=["Always include sources"],
            show_tool_calls=True,
            markdown=True,
            add_chat_history_to_messages= True,
            num_history_responses= 3
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content


class RetrievalAgent:
    def __init__(self, knowledge_base, search_knowledge=True):
        self.agent = Agent(
            knowledge_base=knowledge_base,
            search_knowledge=search_knowledge,
            add_chat_history_to_messages= True,
            num_history_responses= 3,
            memory=AgentMemory(
                db=PgMemoryDb(
                    table_name="retrieval_agent_memory",
                    db_url=DB_URL
                ),
                create_user_memories=True,
                create_session_summary=True
            ),
            storage=PgAgentStorage(
                table_name='personalized_agent_sessions',
                db_url=DB_URL
            )
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content

    def get_memories(self):
        return self.agent.memory.memories
    
    def get_memory_summary(self):
        return self.agent.memory.summary