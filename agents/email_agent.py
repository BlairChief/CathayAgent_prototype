from phi.agent import Agent
from tools.emailv2 import EmailV2Tools
from phi.model.openai import OpenAIChat
import os

class EmailAgent:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_name = os.getenv("SENDER_NAME")
        self.sender_passkey = os.getenv("SENDER_PASSKEY")
        self.agent = Agent(
            name="Email Agent",
            role="Send data to an email address",
            instructions=[
                "You are responsible for sending emails.",
                "When you receive a message:",
                "1. Look for email addresses in the message",
                "2. Make the format of email addresses correct(like 'at' to '@','dot' to '.')",
                "3. If you find an email, use it as the receiver_email",
                "4. When calling email_user, include the found email in receiver_email parameter",
                "5. If emailing is required, maintain a gentle and polite tone, and follow proper formatting guidelines."
                "6. Please the format of the email",
                "Use zh_tw as the language for all communications."
            ],
            tools=[
                EmailV2Tools(
                    sender_email=self.sender_email,
                    sender_name=self.sender_name,
                    sender_passkey=self.sender_passkey,
                )
            ]
        )