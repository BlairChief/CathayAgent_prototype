from phi.agent import Agent
from phi.tools.email import EmailTools
import concurrent.futures
import os
import asyncio

class EmailAgent:
    def __init__(self):
        self.receiver_email = os.getenv("RECEIVER_EMAIL")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_name = os.getenv("SENDER_NAME")
        self.sender_passkey = os.getenv("SENDER_PASSKEY")
        print(f"Initializing EmailAgent with receiver_email={self.receiver_email}")  # Debug log
        self.agent = Agent(
            name="Email Agent",
            role="Send stock data from Yahoo Finance to an email address",
            tools=[
                EmailTools(
                    receiver_email=self.receiver_email,
                    sender_email=self.sender_email,
                    sender_name=self.sender_name,
                    sender_passkey=self.sender_passkey,
                )
            ]
        )

        self.executor = concurrent.futures.ThreadPoolExecutor()

    async def ask(self, prompt: str) -> str:
        """
        處理電子郵件相關的請求。
        
        參數:
            prompt (str): 用戶的請求文字。
        
        返回:
            str: 處理結果或錯誤訊息。
        """
        print("EmailAgent: Received prompt for email processing")
        
        # 定義一個非阻塞的處理函數
        def process_email():
            streaming_response = self.agent.run(prompt, stream=True)
            response_content = ""
            for text in streaming_response:
                response_content += text.content
            return response_content.strip()
        
        # 使用 asyncio 的 run_in_executor 來避免阻塞
        loop = asyncio.get_event_loop()
        try:
            response_content = await loop.run_in_executor(None, process_email)
            return response_content
        except Exception as e:
            print(f"EmailAgent: Email processing failed: {e}")
            return f"錯誤: 電子郵件處理失敗 - {e}"
    