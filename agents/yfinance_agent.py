from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools
from phi.model.openai import OpenAIChat

class YfinanceAgent:
    def __init__(self):
        self.agent = Agent(
            name="YFinance Agent",
            role="get stock data from Yahoo Finance according to the query",
            model=OpenAIChat(id="gpt-4o-mini"),
            instructions=[
                "You are responsible for getting stock data from Yahoo Finance according to the query.",
                "plese pay attention to the user's requirements of the correct date.",
            ],
            tools=[YFinanceTools(stock_price=True, 
                                 analyst_recommendations=True, 
                                 stock_fundamentals=True,
                                 historical_prices=True,
                                 )],
        )

    def ask(self, prompt: str):
        streaming_response = self.agent.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content