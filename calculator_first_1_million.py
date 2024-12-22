from phi.agent import Agent
from phi.tools.python import PythonTools

# 定義自訂儲蓄目標計算工具
class SavingsGoalCalculator:

    def __call__(self, target_amount: float, monthly_saving: float, annual_return_rate: float):
        """
        計算達成目標金額所需的時間（以年為單位）。
        :param target_amount: 目標金額
        :param monthly_saving: 每月儲蓄金額
        :param annual_return_rate: 年預期報酬率（百分比）
        :return: 達成目標所需的時間（年）
        """
        import math
        if annual_return_rate <= 0:
            return {"error": "年預期報酬率必須大於 0。"}
        if monthly_saving <= 0:
            return {"error": "每月儲蓄金額必須大於 0。"}
        if target_amount <= 0:
            return {"error": "目標金額必須大於 0。"}

        # 將年報酬率轉換為月報酬率
        monthly_return_rate = (annual_return_rate / 100) / 12

        # 計算所需的月數
        months_needed = math.log((target_amount * monthly_return_rate / monthly_saving) + 1) / math.log(1 + monthly_return_rate)

        # 將月數轉換為年數
        years_needed = months_needed / 12

        return {"years_needed": round(years_needed, 2)}

# 創建 Agent 並加入工具
agent = Agent(
    tools=[
        PythonTools()
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
    "目標金額、每月規劃投資金額、預計達成時間、預期報酬率等這四者是互相驗證與計算計劃是否可行的要素",
    "若資訊不足，可以詢問user必要的要素",
    ],
)

# # 與 Agent 互動
# response = agent.run(
#     input_text="如果我每月儲蓄 10,000 元，年預期報酬率為 5%，要達成 1,000,000 元的目標需要多久？",
#     context={
#         "target_amount": 1000000,
#         "monthly_saving": 10000,
#         "annual_return_rate": 5
#     }
# )

agent.print_response("如果我每月儲蓄 10,000 元，年預期報酬率為 5%，要達成 1,000,000 元的目標需要多久？", markdown=True)