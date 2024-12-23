import os
from dotenv import load_dotenv
from phi.agent import Agent
from tools import FirstMillionCalculator

load_dotenv()

agent = Agent(
    tools=[
        FirstMillionCalculator(),
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

agent.print_response(
    "Given my annual return rate is 2 percent, how long would it take for me to save USD 1,000,000 if my monthly saving is USD 5000? ",
    markdown=True
)

