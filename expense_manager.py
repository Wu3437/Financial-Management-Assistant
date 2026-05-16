import re
from datetime import datetime

class ExpenseManager:
    CATEGORIES = {
        'food': ['外卖', '吃饭', '午餐', '晚餐', '早餐', '奶茶', '咖啡', '零食', '水果', '饮料'],
        'transport': ['打车', '地铁', '公交', '滴滴', '车费', '加油'],
        'shopping': ['购物', '衣服', '鞋子', '化妆品', '淘宝', '京东'],
        'entertainment': ['电影', '游戏', 'KTV', '娱乐', '演出'],
        'study': ['教材', '书', '课程', '培训', '文具'],
        'living': ['房租', '水电', '话费', '网费'],
        'health': ['医院', '药', '体检', '健身'],
        'misc': ['其他', '礼物', '红包']
    }
    
    CATEGORY_LABELS = {
        'food': '餐饮',
        'transport': '交通',
        'shopping': '购物',
        'entertainment': '娱乐',
        'study': '学习',
        'living': '生活',
        'health': '健康',
        'misc': '其他'
    }
    
    def extract_amount(self, text):
        patterns = [
            r'(\d+\.?\d*)元',
            r'(\d+\.?\d*)块',
            r'(\d+\.?\d*)钱',
            r'花了(\d+\.?\d*)',
            r'(\d+\.?\d*)元?'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        return None
    
    def classify_category(self, text):
        text = text.lower()
        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        return 'misc'
    
    def parse_expense(self, text):
        amount = self.extract_amount(text)
        category = self.classify_category(text)
        return {
            'amount': amount,
            'category': category,
            'category_label': self.CATEGORY_LABELS[category],
            'raw_text': text
        }
    
    def get_monthly_spending(self, records):
        monthly = {}
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        for record in records:
            record_date = datetime.fromisoformat(record['date'])
            if record_date.year == current_year and record_date.month == current_month:
                cat = record['category']
                if cat not in monthly:
                    monthly[cat] = 0
                monthly[cat] += record['amount']
        
        return monthly
    
    def generate_tongue_teasing(self, amount, category, budget_status, spending_history):
        teasings = []
        
        if category == 'food' and '奶茶' in spending_history[-1]['description'][:-10] if spending_history else '' or '咖啡' in spending_history[-1]['description'][:-10] if spending_history else '':
            teasings.append(f"又喝奶茶/咖啡？！这月第{sum(1 for r in spending_history if '奶茶' in r.get('description', '') or '咖啡' in r.get('description', '')) + 1}杯了吧宝子！")
        
        if budget_status['status'] == 'warning':
            teasings.append(f"你的预算已经用了{budget_status['percentage']:.0f}%啦，再花就要吃土了！")
        elif budget_status['status'] == 'caution':
            teasings.append(f"本月支出已达预算的{budget_status['percentage']:.0f}%，注意节制哦~")
        
        if amount > 100:
            teasings.append(f"一顿花{amount}块？！你的恩格尔系数要上天啦！")
        
        if teasings:
            return teasings[0] + " " + "你的攒钱梦想又远了一步哦~"
        return None
    
    def generate_friendly_feedback(self, amount, category_label):
        responses = [
            f"收到！已帮你记录{category_label}支出 {amount}元~",
            f"好的，{category_label}消费 {amount}元已入账！",
            f"记下啦！{category_label}花了 {amount}元，继续保持哦~"
        ]
        return responses[0]
