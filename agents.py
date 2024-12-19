import os
from textwrap import dedent
from datetime import datetime
from dotenv import load_dotenv
from phi.agent import Agent, AgentMemory
from phi.tools.duckduckgo import DuckDuckGo
from phi.memory.db.postgres import PgMemoryDb
from phi.storage.agent.postgres import PgAgentStorage

load_dotenv()

class WebAgent:
    def __init__(self):
        self.agent = Agent(
            name="Web Searcher",
            role="Get seach queries on a topic",
            tools=[DuckDuckGo()],
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content


class PresentationAgent:
    def __init__(self):
        self.agent = Agent(
            name="Presentation Maker",
            role="Makes easy-to-understand and engaging presentation slides.",
            instructions=[
                "You are going to make a presentation using Marp (Visual Studio Code) in Markdown.",
                "You are going to use the sources you got from the internet and the sources we have in the database",
                "When making the presentation, please include the source, as well as the references.",
                "Include mathematical equations and Python code if possible.",
                "When creating the presentation, you are going to follow the format provided.",
            ],
            expected_output=dedent("""
            ---
            marp: true
            title: Marp
            paginate: true
            theme: uncover
            ---

            # My Presentation

            ---

            ## Slides 1

            Something interesting happens in the first day

            ---

            ## Slides 2

            ![w:300](https://marp.app/assets/marp-logo.svg)

            ---

            ## Slides 3

            ```python
            def foo(self):
                pass
            ```
                     
            ---

            ## Slides 4

            $$
            \beta = \alpha + \beta
            $$
            """),
            save_response_to_file=f"presentations/presentation-{datetime.now}.md",
        )


class RetrievalAgent:
    def __init__(self, knowledge_base, search_knowledge=True):
        self.agent = Agent(
            name="Retrieval Agent",
            role="Retrieves related sources based on a given topic",
            knowledge_base=knowledge_base,
            search_knowledge=search_knowledge,
            add_chat_history_to_messages= True,
            num_history_responses= 3,
            memory=AgentMemory(
                db=PgMemoryDb(
                    table_name="retrieval_agent_memory",
                    db_url=os.getenv('DB_URL')
                ),
                create_user_memories=True,
                create_session_summary=True
            ),
            storage=PgAgentStorage(
                table_name='personalized_agent_sessions',
                db_url=os.getenv('DB_URL')
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