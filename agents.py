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
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content