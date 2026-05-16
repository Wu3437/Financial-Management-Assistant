import re
from datetime import datetime

class IncomeManager:
    """收入管理模块 - 支持记录兼职、奖学金等收入"""
    
    INCOME_CATEGORIES = {
        'part_time': ['兼职', '打工', '家教', '实习', '副业'],
        'scholarship': ['奖学金', '助学金', '补助'],
        'family': ['生活费', '家里给的', '父母'],
        'investment': ['理财收益', '利息', '股息', '分红'],
        'other_income': ['其他', '红包', '礼金']
    }
    
    CATEGORY_LABELS = {
        'part_time': '兼职收入',
        'scholarship': '奖学金',
        'family': '生活费',
        'investment': '投资收益',
        'other_income': '其他收入'
    }
    
    def extract_amount(self, text):
        """从文本中提取金额"""
        patterns = [
            r'(\d+\.?\d*)元',
            r'(\d+\.?\d*)块',
            r'(\d+\.?\d*)钱',
            r'收到(\d+\.?\d*)',
            r'(\d+\.?\d*)元?'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        return None
    
    def classify_category(self, text):
        """分类收入类型"""
        text = text.lower()
        for category, keywords in self.INCOME_CATEGORIES.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        return 'other_income'
    
    def parse_income(self, text):
        """解析收入输入"""
        amount = self.extract_amount(text)
        category = self.classify_category(text)
        return {
            'amount': amount,
            'category': category,
            'category_label': self.CATEGORY_LABELS[category],
            'raw_text': text
        }
    
    def generate_friendly_feedback(self, amount, category_label):
        """生成友好的反馈消息"""
        responses = [
            f"💰 收到！已记录{category_label} {amount}元~",
            f"🎉 {category_label}到账 {amount}元，太棒了！",
            f"好的，{category_label} {amount}元已入账！"
        ]
        return responses[0]
    
    def get_monthly_income(self, records):
        """获取本月收入统计"""
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
    
    def generate_income_summary(self, records):
        """生成收入汇总报告"""
        monthly_income = self.get_monthly_income(records)
        
        if not monthly_income:
            return "这个月还没有记录收入哦~"
        
        total = sum(monthly_income.values())
        
        message = "📈 **本月收入汇总**\n\n"
        message += f"💰 总收入：{total:.2f}元\n\n"
        message += "📊 收入明细：\n"
        
        for category, amount in monthly_income.items():
            label = self.CATEGORY_LABELS.get(category, category)
            percentage = (amount / total) * 100
            message += f"  - {label}: {amount:.2f}元 ({percentage:.1f}%)\n"
        
        return message
    
    def get_income_tips(self):
        """获取收入管理建议"""
        tips = [
            '💡 **收入分配**：建议按比例分配：必要支出50%、储蓄/投资30%、灵活消费20%',
            '💡 **先存后花**：收到收入后先存一部分，再规划支出',
            '💡 **记录来源**：清晰记录每笔收入来源，便于财务规划',
            '💡 **提升技能**：利用业余时间学习，提高兼职收入能力',
            '💡 **合理避税**：了解个人所得税相关知识，合法合规'
        ]
        return "\n\n".join(tips)