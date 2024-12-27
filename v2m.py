import streamlit as st
from textwrap import dedent
from teams import V2MTeam
from knowledge_base import PdfKnowledgeBase
from agents import WebAgent, RetrievalAgent, YfinanceAgent, EmailAgent

web_agent = WebAgent()
yfinance_agent=YfinanceAgent()
email_agent = EmailAgent()

db = PdfKnowledgeBase()
db.initialize_knowledge_base()
# db.pdf_knowledge_base.load(recreate=True, upsert=True)
retrieval_agent = RetrievalAgent(db.pdf_knowledge_base)

if __name__ == "__main__":
    v2m_team = V2MTeam(
    team=[web_agent.agent, retrieval_agent.agent, yfinance_agent.agent, email_agent.agent],
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
    ]
    )
    response_text = ""
    for response in v2m_team.ask("我想要今天台積電的台幣收盤價，使用繁體中文寄送email給我"):
        response_text += response  # 拼接片段
    print(response_text.strip())  # 去除多餘空格

