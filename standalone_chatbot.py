import os
import re
from datetime import datetime, timedelta

class StandaloneChatbot:
    def __init__(self):
        self.memory = self._init_memory()
        self.conversation_history = []
    
    def _init_memory(self):
        return {
            'monthly_budget': 0,
            'spent_amount': 0,
            'saving_goals': [],
            'risk_preference': '稳健型',
            'spending_history': [],
            'income_history': [],
            'emergency_fund': 0,
            'last_update': datetime.now().isoformat()
        }
    
    def save_memory(self):
        self.memory['last_update'] = datetime.now().isoformat()
    
    def extract_amount(self, text):
        patterns = [
            r'(\d+\.?\d*)元',
            r'(\d+\.?\d*)块',
            r'(\d+\.?\d*)钱',
            r'花了(\d+\.?\d*)',
            r'收到(\d+\.?\d*)',
            r'(\d+\.?\d*)元?'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        return None
    
    def classify_expense_category(self, text):
        categories = {
            'food': ['外卖', '吃饭', '午餐', '晚餐', '早餐', '奶茶', '咖啡', '零食', '水果', '饮料'],
            'transport': ['打车', '地铁', '公交', '滴滴', '车费', '加油'],
            'shopping': ['购物', '衣服', '鞋子', '化妆品', '淘宝', '京东'],
            'entertainment': ['电影', '游戏', 'KTV', '娱乐', '演出'],
            'study': ['教材', '书', '课程', '培训', '文具'],
            'living': ['房租', '水电', '话费', '网费'],
            'health': ['医院', '药', '体检', '健身'],
            'misc': ['其他', '礼物', '红包']
        }
        category_labels = {
            'food': '餐饮',
            'transport': '交通',
            'shopping': '购物',
            'entertainment': '娱乐',
            'study': '学习',
            'living': '生活',
            'health': '健康',
            'misc': '其他'
        }
        
        text_lower = text.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category, category_labels[category]
        return 'misc', '其他'
    
    def classify_income_category(self, text):
        categories = {
            'part_time': ['兼职', '打工', '家教', '实习', '副业'],
            'scholarship': ['奖学金', '助学金', '补助'],
            'family': ['生活费', '家里给的', '父母'],
            'investment': ['理财收益', '利息', '股息', '分红'],
            'other_income': ['其他', '红包', '礼金']
        }
        category_labels = {
            'part_time': '兼职收入',
            'scholarship': '奖学金',
            'family': '生活费',
            'investment': '投资收益',
            'other_income': '其他收入'
        }
        
        text_lower = text.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category, category_labels[category]
        return 'other_income', '其他收入'
    
    def handle_expense_input(self, text):
        amount = self.extract_amount(text)
        if amount is None:
            return "抱歉，我没找到金额信息，你可以说'买奶茶花了25元'这样的格式~"
        
        category, category_label = self.classify_expense_category(text)
        
        self.memory['spent_amount'] += amount
        record = {
            'amount': amount,
            'category': category,
            'description': text,
            'date': datetime.now().isoformat()
        }
        self.memory['spending_history'].append(record)
        self.save_memory()
        
        budget = self.memory['monthly_budget']
        response = f"✅ 收到！已帮你记录{category_label}支出 {amount}元~"
        
        if budget > 0:
            percentage = (self.memory['spent_amount'] / budget) * 100
            if percentage >= 90:
                response += f"\n\n😱 警告！本月预算已用{percentage:.0f}%，再花就要吃土了！"
            elif percentage >= 70:
                response += f"\n\n⚠️ 提醒：本月预算已用{percentage:.0f}%，注意节制哦~"
        
        if '奶茶' in text:
            response += "\n\n😜 又喝奶茶？！你的恩格尔系数要上天啦！"
        
        return response
    
    def handle_income_input(self, text):
        amount = self.extract_amount(text)
        if amount is None:
            return "抱歉，我没找到金额信息，你可以说'兼职收入500元'这样的格式~"
        
        category, category_label = self.classify_income_category(text)
        
        record = {
            'amount': amount,
            'category': category,
            'description': text,
            'date': datetime.now().isoformat()
        }
        self.memory['income_history'].append(record)
        self.save_memory()
        
        return f"💰 收到！已记录{category_label} {amount}元~"
    
    def handle_saving_goal(self, text):
        match = re.search(r'攒钱(.+?)目标(\d+)元', text)
        if match:
            name = match.group(1).strip()
            target = int(match.group(2))
            deadline = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
            
            goal = {
                'id': len(self.memory['saving_goals']) + 1,
                'name': name,
                'target_amount': target,
                'current_amount': 0,
                'deadline': deadline,
                'priority': 'medium'
            }
            self.memory['saving_goals'].append(goal)
            self.save_memory()
            
            months_left = 6
            monthly = round(target / months_left, 2)
            weekly = round(monthly / 4, 2)
            
            return f"🎯 已创建攒钱目标「{name}」\n\n" \
                   f"📅 目标金额：{target}元\n" \
                   f"⏳ 截止日期：{deadline}\n" \
                   f"💰 每月需存：{monthly}元\n" \
                   f"📊 每周需存：{weekly}元\n\n" \
                   f"💪 加油！坚持就是胜利！"
        
        goals = self.memory['saving_goals']
        if not goals:
            return "你还没有设定攒钱目标呢！可以说'攒钱买手机目标5000元'来创建~"
        
        response = "📋 你的攒钱目标：\n"
        for goal in goals:
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            response += f"\n🎯 {goal['name']}: {goal['current_amount']}/{goal['target_amount']}元 ({progress:.1f}%)"
            response += f"\n   截止日期: {goal['deadline']}"
        
        return response
    
    def handle_emergency_fund(self, text):
        match = re.search(r'应急金(\d+)元', text)
        if match:
            amount = int(match.group(1))
            self.memory['emergency_fund'] += amount
            self.save_memory()
            return f"✅ 已存入应急金 {amount}元！当前应急金总额：{self.memory['emergency_fund']}元"
        
        monthly_expense = self.memory.get('spent_amount', 0)
        target = monthly_expense * 3
        progress = (self.memory['emergency_fund'] / target) * 100 if target > 0 else 0
        
        response = f"💰 **应急金状态**\n\n"
        response += f"📊 当前应急金：{self.memory['emergency_fund']}元\n"
        response += f"🎯 建议目标：{target}元（3个月生活费）\n"
        
        if target > 0:
            response += f"📈 完成进度：{progress:.1f}%\n\n"
            
            if progress >= 100:
                response += "🎉 太棒了！你的应急金已经达标！"
            elif progress >= 50:
                response += "💪 已经完成一半了，继续加油！"
            else:
                response += "🌱 建议每月从结余中划出一部分作为应急金哦~"
        else:
            response += "\n🌱 先记录一些消费，我才能帮你计算应急金目标~"
        
        return response
    
    def handle_analysis(self, text):
        spending_history = self.memory.get('spending_history', [])
        income_history = self.memory.get('income_history', [])
        budget = self.memory.get('monthly_budget', 0)
        
        if '报告' in text or '月度' in text:
            if not spending_history:
                return "本月还没有消费记录哦~"
            
            total_spent = sum(r['amount'] for r in spending_history)
            response = f"📊 **本月消费报告**\n\n"
            response += f"💰 总支出：{total_spent:.2f}元\n"
            
            if budget > 0:
                response += f"📋 月度预算：{budget}元\n"
                response += f"⚡ 预算使用：{(total_spent/budget*100):.1f}%\n"
            
            return response
        
        if '储蓄率' in text:
            total_income = sum(r['amount'] for r in income_history)
            total_spent = sum(r['amount'] for r in spending_history)
            
            if total_income == 0:
                return "还没有记录收入，无法计算储蓄率~"
            
            saving_rate = ((total_income - total_spent) / total_income) * 100
            response = f"💹 **储蓄率分析**\n\n"
            response += f"💰 本月收入：{total_income:.2f}元\n"
            response += f"💸 本月支出：{total_spent:.2f}元\n"
            response += f"🎯 储蓄率：{saving_rate:.1f}%\n\n"
            
            if saving_rate >= 30:
                response += "🎉 太棒了！储蓄率超过30%，非常优秀！"
            elif saving_rate >= 20:
                response += "👍 不错！储蓄率在20%-30%之间~"
            else:
                response += "💪 建议争取达到20%以上的储蓄率哦~"
            
            return response
        
        return "请问你想了解哪方面的分析呢？可以说'月度报告'、'储蓄率'等~"
    
    def handle_finance_question(self, text):
        terms = {
            '公募基金': '就像和一群朋友一起拼车——大家把钱凑起来，请专业司机（基金经理）开车，一起到达目的地（赚钱）。',
            '指数基金': '跟着整个车队一起走，复制整个市场的表现，比如沪深300指数基金。',
            '定投': '定期定额投资，每个月固定存一笔钱到基金里，长期下来可以平摊成本。',
            '复利': '利滚利，利息也会产生新的利息，爱因斯坦说这是世界第八大奇迹！',
            '分散投资': '不要把鸡蛋放在同一个篮子里，降低风险。'
        }
        
        for term, explanation in terms.items():
            if term in text:
                return f"📚 **{term}**\n\n{explanation}"
        
        if '解释' in text or '什么是' in text:
            return "你可以问我具体的金融术语，比如'什么是公募基金'、'解释定投'等~"
        
        if '理财' in text or '投资' in text:
            tips = [
                '💡 先存后花：发生活费后先存一部分，剩下的再花',
                '💡 应急金：建议预留3-6个月生活费',
                '💡 记账习惯：每天花1分钟记录支出',
                '💡 远离高息诱惑：年化超过15%要警惕',
                '💡 分散投资：不要把所有钱放一个地方'
            ]
            return "\n\n".join(tips)
        
        return None
    
    def handle_scam_warning(self, text):
        sensitive_words = ['高息群', '校园贷', '兼职垫资', '日息', '高回报', '无风险', '保本保息']
        for word in sensitive_words:
            if word in text:
                if '校园贷' in text or '日息' in text:
                    return "⚠️ 请注意：你提到的内容可能涉及高利贷陷阱！\n\n" \
                           "所谓'日息万分之五'换算成年化利率高达18.25%，远超正常理财收益！\n\n" \
                           "理财第一步是保住本金，请务必远离校园贷！"
                else:
                    return "⚠️ 警告：你提到的内容可能涉及金融风险或诈骗！\n\n" \
                           "请保持警惕，不要轻易相信高收益承诺，保护好自己的财产安全！"
        return None
    
    def handle_budget(self, text):
        match = re.search(r'(\d+)元', text)
        if match:
            budget = int(match.group(1))
            self.memory['monthly_budget'] = budget
            self.save_memory()
            return f"✅ 已设置月度预算为 {budget}元！"
        return "请告诉我预算金额，比如'设置预算3000元'~"
    
    def handle_status(self, text):
        spent = self.memory['spent_amount']
        budget = self.memory['monthly_budget']
        emergency = self.memory['emergency_fund']
        
        response = f"📊 当前财务状态：\n"
        response += f"   已消费：{spent:.2f}元\n"
        response += f"   月度预算：{budget}元\n"
        
        if budget > 0:
            percentage = (spent / budget) * 100
            response += f"   使用比例：{percentage:.1f}%\n"
            
            if percentage >= 100:
                response += "   ⚠️ 已超支！"
            elif percentage >= 90:
                response += "   ⚠️ 接近上限！"
            elif percentage >= 70:
                response += "   ⚡ 使用过半！"
            else:
                response += "   ✅ 状态良好！"
        
        response += f"\n💰 应急金：{emergency:.2f}元"
        
        goals = self.memory['saving_goals']
        if goals:
            response += "\n\n🎯 攒钱目标："
            for goal in goals:
                progress = (goal['current_amount'] / goal['target_amount']) * 100
                response += f"\n   {goal['name']}: {progress:.1f}%"
        
        return response
    
    def respond(self, user_input):
        scam_response = self.handle_scam_warning(user_input)
        if scam_response:
            return scam_response
        
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
        
        if any(word in user_input for word in ['解释', '什么是', '理财', '投资', '基金']):
            finance_response = self.handle_finance_question(user_input)
            if finance_response:
                return finance_response
        
        if any(word in user_input for word in ['预算', '设置预算']):
            return self.handle_budget(user_input)
        
        if any(word in user_input for word in ['状态', '查询', '看看']):
            return self.handle_status(user_input)
        
        return self.default_response(user_input)
    
    def default_response(self, user_input):
        responses = [
            "你好呀！我是财智通~ 有什么可以帮到你吗？",
            "嗨！需要我帮你记录消费、设置攒钱目标，还是解释理财知识呢？",
            "来啦来啦！我可以帮你记账、规划攒钱，还能教你理财知识哦！",
            "哈喽~ 今天想怎么规划你的小金库呢？"
        ]
        
        greetings = ['你好', '嗨', '哈喽', 'hi', 'hello']
        for greet in greetings:
            if greet in user_input.lower():
                return responses[0]
        
        return "我不太明白你的意思呢~ 你可以问我关于消费记录、收入管理、攒钱目标或理财知识的问题哦！"
