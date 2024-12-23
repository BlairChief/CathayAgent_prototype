import os
from typing import List
from textwrap import dedent
from dotenv import load_dotenv
from phi.agent import Agent

load_dotenv()

class CustomAgent:
    def __init__(
        self,
        name: str = None,
        role: str = None,
        instructions: List[str] = None,
        expected_output: str = None,
        memory = None,
        storage = None,
    ):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.expected_output = expected_output
        self.memory = memory
        self.storage = storage

        self.agent = Agent(
            
        )
        