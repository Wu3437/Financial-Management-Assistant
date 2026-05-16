from datetime import datetime, timedelta
from collections import defaultdict

class SpendingAnalyzer:
    """消费分析模块 - 月度统计、趋势分析、预算优化建议"""
    
    def __init__(self):
        self.CATEGORY_LABELS = {
            'food': '餐饮',
            'transport': '交通',
            'shopping': '购物',
            'entertainment': '娱乐',
            'study': '学习',
            'living': '生活',
            'health': '健康',
            'misc': '其他'
        }
    
    def get_monthly_spending(self, records):
        """获取本月各类别消费统计"""
        monthly = defaultdict(float)
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        for record in records:
            record_date = datetime.fromisoformat(record['date'])
            if record_date.year == current_year and record_date.month == current_month:
                cat = record['category']
                monthly[cat] += record['amount']
        
        return dict(monthly)
    
    def get_trend_data(self, records, months=3):
        """获取近期消费趋势数据"""
        trend = []
        now = datetime.now()
        
        for i in range(months):
            target_date = now - timedelta(days=i*30)
            monthly_data = {}
            
            for record in records:
                record_date = datetime.fromisoformat(record['date'])
                if record_date.year == target_date.year and record_date.month == target_date.month:
                    cat = record['category']
                    if cat not in monthly_data:
                        monthly_data[cat] = 0
                    monthly_data[cat] += record['amount']
            
            trend.append({
                'month': f"{target_date.year}-{target_date.month:02d}",
                'data': dict(monthly_data),
                'total': sum(monthly_data.values())
            })
        
        return trend
    
    def generate_monthly_report(self, records, budget=0):
        """生成月度消费报告"""
        monthly_spending = self.get_monthly_spending(records)
        
        if not monthly_spending:
            return "本月还没有消费记录哦~"
        
        total_spent = sum(monthly_spending.values())
        
        message = "📊 **本月消费报告**\n\n"
        message += f"💰 总支出：{total_spent:.2f}元\n"
        
        if budget > 0:
            remaining = budget - total_spent
            percentage = (total_spent / budget) * 100
            message += f"📋 月度预算：{budget}元\n"
            message += f"⚡ 剩余可用：{remaining:.2f}元\n"
            message += f"📈 预算使用：{percentage:.1f}%\n\n"
        
        message += "🏷️ 消费分类：\n"
        sorted_categories = sorted(monthly_spending.items(), key=lambda x: x[1], reverse=True)
        
        for category, amount in sorted_categories:
            label = self.CATEGORY_LABELS.get(category, category)
            percentage = (amount / total_spent) * 100
            message += f"  - {label}: {amount:.2f}元 ({percentage:.1f}%)\n"
        
        return message
    
    def generate_trend_analysis(self, records):
        """生成消费趋势分析"""
        trend = self.get_trend_data(records, 3)
        
        if len(trend) < 2:
            return "数据不足，无法进行趋势分析~"
        
        message = "📈 **消费趋势分析**\n\n"
        
        for i, month_data in enumerate(trend):
            if i == 0:
                period = "本月"
            elif i == 1:
                period = "上月"
            else:
                period = f"{month_data['month']}"
            
            message += f"📅 {period}：{month_data['total']:.2f}元\n"
        
        # 计算环比变化
        if trend[0]['total'] > 0 and trend[1]['total'] > 0:
            change_rate = ((trend[0]['total'] - trend[1]['total']) / trend[1]['total']) * 100
            if change_rate > 0:
                message += f"\n⚠️ 较上月增长 {change_rate:.1f}%，注意控制支出哦~"
            elif change_rate < -5:
                message += f"\n🎉 较上月减少 {abs(change_rate):.1f}%，继续保持！"
            else:
                message += "\n📊 消费保持稳定，继续加油！"
        
        return message
    
    def generate_saving_rate_report(self, income_records, expense_records):
        """生成储蓄率报告"""
        # 计算本月收入
        income_total = 0
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        for record in income_records:
            record_date = datetime.fromisoformat(record['date'])
            if record_date.year == current_year and record_date.month == current_month:
                income_total += record['amount']
        
        # 计算本月支出
        expense_total = 0
        for record in expense_records:
            record_date = datetime.fromisoformat(record['date'])
            if record_date.year == current_year and record_date.month == current_month:
                expense_total += record['amount']
        
        if income_total == 0:
            return "还没有记录收入，无法计算储蓄率~"
        
        saving_rate = ((income_total - expense_total) / income_total) * 100
        
        message = "💹 **储蓄率分析**\n\n"
        message += f"💰 本月收入：{income_total:.2f}元\n"
        message += f"💸 本月支出：{expense_total:.2f}元\n"
        message += f"📈 本月结余：{(income_total - expense_total):.2f}元\n"
        message += f"🎯 储蓄率：{saving_rate:.1f}%\n\n"
        
        if saving_rate >= 30:
            message += "🎉 太棒了！你的储蓄率超过30%，非常优秀！"
        elif saving_rate >= 20:
            message += "👍 不错！储蓄率在20%-30%之间，继续努力！"
        elif saving_rate >= 10:
            message += "💪 还可以，建议争取达到20%以上~"
        elif saving_rate >= 0:
            message += "⚡ 收支基本平衡，建议减少不必要的支出~"
        else:
            message += "⚠️ 本月超支了！下个月要注意控制哦~"
        
        return message
    
    def get_budget_optimization_suggestions(self, records, budget=0):
        """获取预算优化建议"""
        monthly_spending = self.get_monthly_spending(records)
        
        if not monthly_spending:
            return "还没有足够的消费数据来提供建议~"
        
        suggestions = []
        total_spent = sum(monthly_spending.values())
        
        # 分析各类别占比
        for category, amount in monthly_spending.items():
            percentage = (amount / total_spent) * 100
            label = self.CATEGORY_LABELS.get(category, category)
            
            if category == 'food' and percentage > 40:
                suggestions.append(f"🍜 **餐饮支出偏高**：占比{percentage:.1f}%，建议适当减少外卖和奶茶消费~")
            elif category == 'shopping' and percentage > 25:
                suggestions.append(f"🛍️ **购物支出较多**：占比{percentage:.1f}%，建议理性消费，避免冲动购物~")
            elif category == 'entertainment' and percentage > 20:
                suggestions.append(f"🎮 **娱乐支出偏高**：占比{percentage:.1f}%，可以尝试一些低成本的娱乐方式~")
        
        # 预算预警
        if budget > 0 and total_spent > budget * 0.9:
            suggestions.append(f"⚠️ **预算即将超支**：已使用{total_spent/budget*100:.1f}%，本月剩余{budget-total_spent:.2f}元~")
        
        if not suggestions:
            suggestions.append("✅ 消费结构健康，继续保持！")
        
        return "\n\n".join(suggestions)