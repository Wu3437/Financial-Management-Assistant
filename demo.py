from standalone_chatbot import StandaloneChatbot

def print_banner():
    print("\n" + "="*60)
    print("          🎯 财智通 - 演示版")
    print("="*60)

def print_help():
    help_text = """
📖 功能说明：

1. 消费记录
   支持一句话录入："刚点外卖花了25元"、"买奶茶30块"

2. 攒钱规划
   设定目标："攒钱买手机目标5000元"
   查询进度："看看我的攒钱目标"

3. 预算管理
   设置预算："设置预算3000元"

4. 理财知识
   解释术语："什么是公募基金"、"解释定投"

5. 状态查询
   "我的财务状态"

💡 输入 '退出' 结束
"""
    print(help_text)

def main():
    print_banner()
    print_help()
    
    bot = StandaloneChatbot()
    print("💬 你好！我是财智通，有什么可以帮到你吗？")
    
    while True:
        try:
            user_input = input("\n你: ")
            
            if user_input.lower() in ['退出', 'quit', 'q', 'bye']:
                print("👋 再见！祝你理财顺利！")
                break
            
            response = bot.respond(user_input)
            print(f"\n🤖 小助手: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 出错了：{str(e)}")

if __name__ == "__main__":
    main()
