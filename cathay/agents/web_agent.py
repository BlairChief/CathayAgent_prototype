from phi.agent import Agent
from cathay.tools import Searxng

class WebAgent:
    def __init__(self):
        self.agent = Agent(
            name="Web Searcher",
            role="Get seach queries on a topic",
            tools=[Searxng()],
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content