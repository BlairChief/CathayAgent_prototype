from typing import List
from phi.agent import Agent
from textwrap import dedent
from datetime import datetime

class PresentationAgent:
    def __init__(self, instructions: List[str], expected_output: str, save_location: str):
        self.instructions = instructions
        self.expected_output = expected_output
        
        self.agent = Agent(
            name="Presentation Maker",
            role="Makes easy-to-understand and engaging presentation slides for technical and non-technical audiences.",
            instructions=self.instructions,
            expected_output=self.expected_output,
            save_response_to_file=f"{save_location}/presentation_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.md",
        )
