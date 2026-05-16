from chatbot import Chatbot
from colorama import init, Fore, Style

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║                    🎯 财智元                           ║
{Fore.CYAN}║              陪伴你养成良好的理财习惯                         ║
{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_help():
    help_text = f"""
{Fore.YELLOW}📖 功能说明：

{Fore.GREEN}1. 消费记录
   {Fore.WHITE}支持一句话录入："刚点外卖花了25元"、"买奶茶30块"
   自动识别金额和消费类别，预算接近上限时会毒舌提醒

{Fore.GREEN}2. 攒钱规划
   {Fore.WHITE}设定目标："攒钱买手机目标5000元"
   查询进度："看看我的攒钱进度"

{Fore.GREEN}3. 收入管理
   {Fore.WHITE}记录收入："兼职收入500元"、"奖学金到账2000元"
   支持兼职、奖学金、生活费等类别

{Fore.GREEN}4. 应急储蓄
   {Fore.WHITE}查询状态："我的应急金"
   存入金额："应急金存入1000元"

{Fore.GREEN}5. 预算管理
   {Fore.WHITE}设置预算："设置预算3000元"
   查询状态："我的财务状态"

{Fore.GREEN}6. 消费分析
   {Fore.WHITE}月度报告："生成月度报告"
   趋势分析："分析消费趋势"
   储蓄率："计算储蓄率"
   优化建议："给我预算优化建议"

{Fore.GREEN}7. 理财知识
   {Fore.WHITE}解释术语："什么是公募基金"、"解释定投"
   获取建议："给我一些理财建议"

{Fore.GREEN}8. 防坑预警
   {Fore.WHITE}自动识别校园贷、高息群等敏感词并预警

{Fore.YELLOW}💡 输入示例：
   - "中午吃饭花了20元"
   - "兼职收入800元"
   - "攒钱旅游目标3000元"
   - "什么是复利"
   - "我的状态"
   - "生成月度报告"
   - "应急金存入500元"

{Fore.YELLOW}📱 输入 '退出' 或 'quit' 结束对话
"""
    print(help_text)

def main():
    print_banner()
    print_help()
    
    bot = Chatbot()
    
    print(f"\n{Fore.BLUE}💬 你好！我是财智通，有什么可以帮到你吗？")
    
    while True:
        try:
            user_input = input(f"\n{Fore.WHITE}你: ")
            
            if user_input.lower() in ['退出', 'quit', 'q', 'bye']:
                print(f"{Fore.CYAN}👋 再见！祝你理财顺利，早日实现财务自由！")
                break
            
            if user_input.lower() in ['帮助', 'help', '功能']:
                print_help()
                continue
            
            response = bot.respond(user_input)
            print(f"\n{Fore.GREEN}🤖 小助手: {response}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}👋 再见！")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ 出错了：{str(e)}")

if __name__ == "__main__":
    main()
