from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools

class YfinanceAgent:
    def __init__(self):
        self.agent = Agent(
            name="YFinance Agent",
            role="get stock data from Yahoo Finance according to the query",
            tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content