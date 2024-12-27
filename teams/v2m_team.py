import os
from typing import List, Dict, Any
from phi.agent import Agent
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat

load_dotenv()


class V2MTeam:
    def __init__(self, instructions: List[str], team: List[Agent]):
        self.instructions = instructions
        self.team = Agent(
            name="V2MTeam",
            team=team,
            model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY')),
            instructions=self.instructions,
            show_tool_calls=True,
            markdown=True,
        )
        
    def ask(self, prompt: str):
        streaming_response = self.team.run(
            prompt,
            stream=True
        )

        for text in streaming_response:
            yield text.content
        
    # def ask(self, prompt: str):
    #     print("EmailTeam received prompt:", prompt)  # 調試日誌

    #     # 通過 LLM 解析用戶需求
    #     parsed_data = self.parse_prompt_with_llm(prompt)
    #     stocks = parsed_data.get("stocks", [])
    #     single_email = parsed_data.get("single_email", True)
    #     print(f"Parsed stocks: {stocks}, Single email: {single_email}")

    #     # 獲取股票數據（通過 YfinanceAgent）
    #     stock_data = self.fetch_stock_data(stocks)

    #     # 決定郵件寄送方式（通過 EmailAgent）
    #     if single_email:
    #         email_result = self.send_single_email(stock_data)
    #     else:
    #         email_result = self.send_multiple_emails(stock_data)

    #     # 返回整合結果
    #     return f"Stocks: {stock_data}\nEmail Result: {email_result}"

    # def parse_prompt_with_llm(self, prompt: str) -> Dict[str, Any]:
    #     """
    #     使用 LLM 解析用戶指令，提取股票列表和郵件寄送方式。
    #     """
    #     llm_prompt = f"""
    #     You are a smart assistant. Your job is to analyze the following user request and extract:
    #     1. A list of stock symbols the user wants to fetch (e.g., AAPL, MSFT).
    #     2. Whether the user wants the result in a single email or multiple emails.
    #     Return your answer in JSON format with the following keys:
    #     - stocks: A list of stock symbols (strings).
    #     - single_email: A boolean value indicating if the result should be sent in a single email.

    #     User request:
    #     {prompt}
    #     """
    #     print("Sending to LLM for parsing...")  # 調試日誌
    #     streaming_response = self.team.run(llm_prompt, stream=True)
    #     llm_output = "".join([text.content for text in streaming_response]).strip()
    #     print("LLM parsing output:", llm_output)  # 調試日誌

    #     # 嘗試解析 LLM 輸出為 JSON
    #     try:
    #         import json
    #         parsed_data = json.loads(llm_output)
    #     except json.JSONDecodeError:
    #         print("Error decoding LLM output. Returning default values.")  # 錯誤處理
    #         parsed_data = {"stocks": [], "single_email": True}

    #     return parsed_data

    # def fetch_stock_data(self, stocks: List[str]):
    #     """
    #     通過 YfinanceAgent 獲取股票數據。
    #     """
    #     stock_data = {}
    #     for stock in stocks:
    #         yfinance_prompt = f"Get the current stock price for {stock}."
    #         print(f"Fetching data for {stock} using YfinanceAgent...")  # 調試日誌
    #         streaming_response = self.team.run(yfinance_prompt, stream=True)
    #         stock_data[stock] = "".join([text.content for text in streaming_response]).strip()
    #     return stock_data

    # def send_single_email(self, stock_data: dict):
    #     """
    #     通過 EmailAgent 發送單封郵件。
    #     """
    #     email_content = "\n".join([f"{stock}: {price}" for stock, price in stock_data.items()])
    #     email_prompt = f"Send the following stock prices in a single email:\n{email_content}"
    #     print("Sending single email using EmailAgent...")  # 調試日誌
    #     streaming_response = self.team.run(email_prompt, stream=True)
    #     return "".join([text.content for text in streaming_response]).strip()

    # def send_multiple_emails(self, stock_data: dict):
    #     """
    #     通過 EmailAgent 為每支股票分別發送郵件。
    #     """
    #     results = []
    #     for stock, price in stock_data.items():
    #         email_prompt = f"Send the stock price for {stock} ({price}) in a separate email."
    #         print(f"Sending email for {stock} using EmailAgent...")  # 調試日誌
    #         streaming_response = self.team.run(email_prompt, stream=True)
    #         results.append("".join([text.content for text in streaming_response]).strip())
    #     return results
