import os
from typing import List
from phi.agent import Agent
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat

load_dotenv()

class PresentationTeam:
    def __init__(self, instructions: List[str], team: List[Agent]):
        self.team=team
        self.instructions=instructions

        self.team = Agent(
            name="Presentation Maker Team",
            team=self.team,
            model=OpenAIChat(id="gpt-4o", api_key=os.getenv('OPENAI_API_KEY')),
            instructions=self.instructions,
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