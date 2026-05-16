import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import Chatbot

print("测试财智通...")

bot = Chatbot()

test_cases = [
    "刚点外卖花了25元",
    "买奶茶花了18块",
    "设置预算2000元",
    "我的财务状态",
    "攒钱买演唱会门票目标1000元",
    "什么是公募基金",
    "校园贷靠谱吗"
]

print("\n测试结果：")
print("=" * 50)

for i, test_input in enumerate(test_cases, 1):
    print(f"\n测试 {i}: {test_input}")
    print("-" * 30)
    try:
        response = bot.respond(test_input)
        print(f"响应: {response}")
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 50)
print("测试完成！")
