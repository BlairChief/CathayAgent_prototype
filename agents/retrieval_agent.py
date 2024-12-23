import os
from dotenv import load_dotenv
from phi.agent import Agent, AgentMemory
from phi.memory.db.postgres import PgMemoryDb
from phi.storage.agent.postgres import PgAgentStorage

load_dotenv()

class RetrievalAgent:
    def __init__(self, knowledge_base, search_knowledge=True):
        self.agent = Agent(
            name='Retrieval Agent',
            role='Retrieves related sources based on a given topic',
            knowledge_base=knowledge_base,
            search_knowledge=search_knowledge,
            add_chat_history_to_messages= True,
            num_history_responses= 3,
            memory=AgentMemory(
                db=PgMemoryDb(
                    table_name='retrieval_agent_memory',
                    db_url=os.getenv('DB_URL')
                ),
                create_user_memories=True,
                create_session_summary=True,
            ),
            storage=PgAgentStorage(
                table_name='personalized_agent_sessions',
                db_url=os.getenv('DB_URL'),
            ),
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