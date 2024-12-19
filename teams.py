from phi.agent import Agent
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat
import os

load_dotenv()

class PresentationTeam:
    def __init__(self, web_agent, retrieval_agent, presentation_agent):
        self.team = Agent(
            name="Presentation Maker Team",
            team=[web_agent, retrieval_agent, presentation_agent],
            model=OpenAIChat(id="gpt-4o", api_key=os.getenv('OPENAI_API_KEY')),
            instructions=[
                "First, you go on the internet, search for the query keywords, and gather the query results."
                "Then, you would go on the database and look for relevant sources.",
                "Important: you are going to make a Marp presentation with the result that you got from the internet and the database",
                "Finally, generate an insightful presentation for technical and non-technical audience.",
            ],
            show_tool_calls=True,
            markdown=True,
        )

    def ask(self, prompt: str):
        streaming_response = self.team.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content