import streamlit as st
from textwrap import dedent
from teams import V2MTeam
from knowledge_base import PdfKnowledgeBase
from agents import WebAgent, YfinanceAgent, EmailAgent
from tools import SpeechProcessor
from datetime import datetime

from phi.model.openai import OpenAIChat

web_agent = WebAgent()
yfinance_agent=YfinanceAgent()
email_agent = EmailAgent()
speech_processor = SpeechProcessor()

db = PdfKnowledgeBase()
db.initialize_knowledge_base()
# db.pdf_knowledge_base.load(recreate=True, upsert=True)
#retrieval_agent = RetrievalAgent(db.pdf_knowledge_base)

def initv2m():
    return V2MTeam(
    team=[web_agent.agent, yfinance_agent.agent, email_agent.agent],
    instructions = [
    "You are responsible for interpreting the user’s requests and deciding which Agent to use.",
    "Follow these steps whenever you receive a request:",
    "1. Understand the user’s requirements.",
    "2. Determine which Agent(s) the user needs.",
    "3. Identify the correct email address(es) for sending results.",
    "4. Use the chosen Agent(s) to complete the request.",
    "5. If emailing is required, maintain a gentle and polite tone, and follow proper formatting guidelines.",
    "6. After sending the email, provide a clear confirmation that it has been delivered.",
    "7. Use zh_tw as the language for all communications."
    "8. If there is any information missing, use Agent(s) to get."
    "9. today is date", datetime.now().strftime("%Y-%m-%d"),
    "10. Please the format of the email",
    ]
    )
if __name__ == "__main__":
    audio_file = r"C:\Users\User\Desktop\CathayAgent_prototype\morning3.mp3"
    text_prompt = speech_processor.process_audio(audio_file)
    if text_prompt:
        text_prompt = text_prompt
    else:
        text_prompt = "使用繁體中文寄送午安問候信件給我"

    print(text_prompt)
    v2m_team = initv2m()
    response_text = ""
    for response in v2m_team.ask(text_prompt):
        response_text += response  # 拼接片段
    print(response_text.strip())  # 去除多餘空格

