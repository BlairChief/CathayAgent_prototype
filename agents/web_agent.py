from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo

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