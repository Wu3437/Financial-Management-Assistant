import openai
import os
from dotenv import load_dotenv
from system_prompt import SYSTEM_PROMPT, TRIGGER_WORDS, SENSITIVE_WORDS
from memory_system import MemorySystem
from expense_manager import ExpenseManager
from saving_planner import SavingPlanner
from finance_educator import FinanceEducator
from time_plugin import TimePlugin
from income_manager import IncomeManager
from emergency_fund import EmergencyFund
from spending_analyzer import SpendingAnalyzer
from datetime import datetime, timedelta

load_dotenv()

class Chatbot:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
        self.memory = MemorySystem()
        self.expense_manager = ExpenseManager()
        self.saving_planner = SavingPlanner()
        self.finance_educator = FinanceEducator()
        self.time_plugin = TimePlugin()
        self.income_manager = IncomeManager()
        self.emergency_fund = EmergencyFund()
        self.spending_analyzer = SpendingAnalyzer()
        self.conversation_history = []
    
    def detect_persona(self, text):
        text_lower = text.lower()
        advisor_count = sum(1 for word in TRIGGER_WORDS['advisor'] if word in text_lower)
        friend_count = sum(1 for word in TRIGGER_WORDS['friend'] if word in text_lower)
        
        if advisor_count > friend_count:
            return 'advisor'
        elif friend_count > advisor_count:
            return 'friend'
        else:
            return 'mixed'
    
    def check_sensitive_words(self, text):
        for word in SENSITIVE_WORDS:
            if word in text:
                return True, word
        return False, None
    
    def get_memory_context(self):
        memory = self.memory.memory
        context = f"""
用户记忆信息：
- 月度预算：{memory['monthly_budget']}元
- 已消费金额：{memory['spent_amount']}元
- 风险偏好：{memory['risk_preference']}
- 攒钱目标：{len(memory['saving_goals'])}个
"""
        return context
    
    def generate_prompt(self, user_input):
        memory_context = self.get_memory_context()
        time_info = self.time_plugin.generate_time_based_message()
        
        prompt = f"""
{SYSTEM_PROMPT}

【当前时间信息】
{time_info}

【用户记忆】
{memory_context}

【对话历史】
{self.format_conversation_history()}

【用户输入】
{user_input}

请根据以上信息，以合适的人格模式回复用户。
"""
        return prompt
    
    def format_conversation_history(self):
        history = []
        for i, msg in enumerate(self.conversation_history[-5:]):
            role = "用户" if i % 2 == 0 else "助手"
            history.append(f"{role}: {msg}")
        return "\n".join(history)
    
    def add_to_history(self, user_input, response):
        self.conversation_history.append(user_input)
        self.conversation_history.append(response)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def handle_expense_input(self, text):
        parsed = self.expense_manager.parse_expense(text)
        
        if parsed['amount'] is None:
            return "抱歉，我没找到金额信息，你可以说'买奶茶花了25元'这样的格式~"
        
        self.memory.add_expense(
            parsed['amount'],
            parsed['category'],
            parsed['raw_text']
        )
        
        budget_status = self.memory.get_budget_status()
        spending_history = self.memory.get_spending_history()
        
        teasing = self.expense_manager.generate_tongue_teasing(
            parsed['amount'],
            parsed['category'],
            budget_status,
            spending_history
        )
        
        feedback = self.expense_manager.generate_friendly_feedback(
            parsed['amount'],
            parsed['category_label']
        )
        
        if teasing:
            return f"{feedback}\n\n😜 {teasing}"
        return feedback
    
    def handle_saving_goal(self, text):
        import re
        
        match = re.search(r'攒钱(.+?)目标(\d+)元', text)
        if match:
            name = match.group(1).strip()
            target = int(match.group(2))
            deadline = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
            self.memory.add_saving_goal(name, target, deadline)
            plan = self.saving_planner.calculate_monthly_saving(target, deadline)
            return self.saving_planner.generate_plan_message(
                {'name': name, 'target_amount': target, 'deadline': deadline},
                plan
            )
        
        goals = self.memory.get_saving_goals()
        if not goals:
            return "你还没有设定攒钱目标呢！可以告诉我你的心愿，比如'我想攒钱买手机目标5000元'~"
        
        response = "📋 你的攒钱目标：\n"
        for goal in goals:
            progress = self.saving_planner.calculate_progress(goal['current_amount'], goal['target_amount'])
            response += f"\n🎯 {goal['name']}: {goal['current_amount']}/{goal['target_amount']}元 ({progress:.1f}%)"
            response += f"\n   截止日期: {goal['deadline']}"
        
        response += f"\n\n{self.saving_planner.suggest_goal_priority(goals)}"
        return response
    
    def handle_finance_question(self, text):
        if any(word in text for word in ['解释', '什么是', '什么叫', '什么意思']):
            return self.finance_educator.explain_term(text)
        
        if '理财' in text or '投资' in text:
            return self.finance_educator.get_basic_tips()
        
        return None
    
    def call_openai(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"抱歉，我暂时有点忙，稍后再试吧~ (错误: {str(e)})"
    
    def respond(self, user_input):
        has_sensitive, keyword = self.check_sensitive_words(user_input)
        if has_sensitive:
            return self.finance_educator.generate_scam_warning(keyword)
        
        if any(word in user_input for word in ['收到', '收入', '兼职', '奖学金', '生活费']):
            return self.handle_income_input(user_input)
        
        if any(word in user_input for word in ['花了', '买了', '支出', '消费']):
            return self.handle_expense_input(user_input)
        
        if any(word in user_input for word in ['攒钱', '目标', '心愿']):
            return self.handle_saving_goal(user_input)
        
        if any(word in user_input for word in ['应急金', '应急储蓄']):
            return self.handle_emergency_fund(user_input)
        
        if any(word in user_input for word in ['分析', '报告', '趋势', '储蓄率']):
            return self.handle_analysis(user_input)
        
        finance_response = self.handle_finance_question(user_input)
        if finance_response:
            return finance_response
        
        if any(word in user_input for word in ['预算', '设置预算', '修改预算']):
            import re
            match = re.search(r'(\d+)元', user_input)
            if match:
                budget = int(match.group(1))
                self.memory.set_budget(budget)
                return f"✅ 已设置月度预算为 {budget}元！"
            return "请告诉我预算金额，比如'设置预算3000元'~"
        
        if any(word in user_input for word in ['状态', '查询', '看看', '进度']):
            return self.handle_status_query(user_input)
        
        prompt = self.generate_prompt(user_input)
        response = self.call_openai(prompt)
        return response
    
    def handle_income_input(self, text):
        parsed = self.income_manager.parse_income(text)
        
        if parsed['amount'] is None:
            return "抱歉，我没找到金额信息，你可以说'兼职收入500元'这样的格式~"
        
        self.memory.add_income(
            parsed['amount'],
            parsed['category'],
            parsed['raw_text']
        )
        
        return self.income_manager.generate_friendly_feedback(
            parsed['amount'],
            parsed['category_label']
        )
    
    def handle_emergency_fund(self, text):
        import re
        
        match = re.search(r'应急金(\d+)元', text)
        if match:
            amount = int(match.group(1))
            self.memory.add_emergency_fund(amount)
            return f"✅ 已存入应急金 {amount}元！当前应急金总额：{self.memory.get_emergency_fund()}元"
        
        spending_history = self.memory.get_spending_history(30)
        monthly_expense = sum(r['amount'] for r in spending_history) / 30 * 30
        
        return self.emergency_fund.generate_status_message(
            self.memory.get_emergency_fund(),
            monthly_expense
        )
    
    def handle_analysis(self, text):
        spending_history = self.memory.get_spending_history(90)
        income_history = self.memory.get_income_history(90)
        budget = self.memory.get_budget()
        
        responses = []
        
        if '报告' in text or '月度' in text:
            responses.append(self.spending_analyzer.generate_monthly_report(spending_history, budget))
        
        if '趋势' in text:
            responses.append(self.spending_analyzer.generate_trend_analysis(spending_history))
        
        if '储蓄率' in text:
            responses.append(self.spending_analyzer.generate_saving_rate_report(income_history, spending_history))
        
        if '优化' in text or '建议' in text:
            responses.append(self.spending_analyzer.get_budget_optimization_suggestions(spending_history, budget))
        
        if not responses:
            return self.spending_analyzer.generate_monthly_report(spending_history, budget)
        
        return "\n\n---\n\n".join(responses)
    
    def handle_status_query(self, text):
        budget_status = self.memory.get_budget_status()
        spent = self.memory.get_spent_amount()
        budget = self.memory.get_budget()
        emergency = self.memory.get_emergency_fund()
        
        response = f"📊 当前财务状态：\n"
        response += f"   已消费：{spent:.2f}元\n"
        response += f"   月度预算：{budget}元\n"
        
        if budget > 0:
            percentage = (spent / budget) * 100
            response += f"   使用比例：{percentage:.1f}%\n"
            
            if budget_status['status'] == 'over_budget':
                response += "   ⚠️ 已超支！下个月要注意哦~"
            elif budget_status['status'] == 'warning':
                response += "   ⚠️ 接近预算上限，要节制啦！"
            elif budget_status['status'] == 'caution':
                response += "   ⚡ 预算使用过半，继续保持！"
            else:
                response += "   ✅ 状态良好，继续加油！"
        
        response += f"\n💰 应急金：{emergency:.2f}元"
        
        goals = self.memory.get_saving_goals()
        if goals:
            response += "\n\n🎯 攒钱目标进度："
            for goal in goals:
                progress = self.saving_planner.calculate_progress(goal['current_amount'], goal['target_amount'])
                response += f"\n   {goal['name']}: {progress:.1f}%"
        
        return response
