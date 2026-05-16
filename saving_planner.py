from datetime import datetime, timedelta

class SavingPlanner:
    def calculate_monthly_saving(self, target_amount, deadline):
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
        today = datetime.now()
        
        if deadline_date <= today:
            return None
        
        months_left = (deadline_date.year - today.year) * 12 + (deadline_date.month - today.month)
        if months_left <= 0:
            months_left = 1
        
        monthly_amount = target_amount / months_left
        return {
            'months_left': months_left,
            'monthly_saving': round(monthly_amount, 2),
            'weekly_saving': round(monthly_amount / 4, 2),
            'daily_saving': round(monthly_amount / 30, 2)
        }
    
    def calculate_progress(self, current_amount, target_amount):
        if target_amount == 0:
            return 0
        return (current_amount / target_amount) * 100
    
    def generate_progress_message(self, goal):
        progress = self.calculate_progress(goal['current_amount'], goal['target_amount'])
        
        if progress >= 100:
            return f"🎉 恭喜！「{goal['name']}」目标已达成！"
        elif progress >= 80:
            return f"🔥 「{goal['name']}」进度超棒！已完成 {progress:.1f}%，继续保持！"
        elif progress >= 50:
            return f"💪 「{goal['name']}」已完成 {progress:.1f}%，过半啦！加油！"
        elif progress >= 20:
            return f"👍 「{goal['name']}」进度 {progress:.1f}%，积少成多哦~"
        else:
            return f"🌱 「{goal['name']}」刚开始呢，进度 {progress:.1f}%，坚持就是胜利！"
    
    def generate_plan_message(self, goal, plan):
        message = f"📝 「{goal['name']}」目标规划：\n"
        message += f"    🎯 目标金额：{goal['target_amount']}元\n"
        message += f"    📅 截止日期：{goal['deadline']}\n"
        message += f"    ⏳ 剩余时间：{plan['months_left']}个月\n"
        message += f"    💰 每月需存：{plan['monthly_saving']}元\n"
        message += f"    📊 每周需存：{plan['weekly_saving']}元\n"
        message += f"    🪙 每天需存：{plan['daily_saving']}元\n"
        return message
    
    def suggest_goal_priority(self, goals):
        sorted_goals = sorted(goals, key=lambda x: (x['priority'], x['deadline']))
        suggestions = []
        
        for i, goal in enumerate(sorted_goals[:3], 1):
            progress = self.calculate_progress(goal['current_amount'], goal['target_amount'])
            deadline_date = datetime.strptime(goal['deadline'], '%Y-%m-%d')
            days_left = (deadline_date - datetime.now()).days
            
            if days_left <= 30 and progress < 80:
                suggestions.append(f"⚠️ 「{goal['name']}」只剩{days_left}天了，进度才{progress:.0f}%，要加油哦！")
            elif goal['priority'] == 'high' and progress < 50:
                suggestions.append(f"🔥 「{goal['name']}」优先级高，目前进度{progress:.0f}%，建议优先完成！")
        
        if suggestions:
            return "\n".join(suggestions)
        return "✅ 所有目标进度良好，继续保持！"
    
    def calculate_emergency_fund(self, monthly_expense):
        emergency_amount = monthly_expense * 3
        return {
            'suggested_amount': emergency_amount,
            'description': '建议预留3个月生活费作为应急金'
        }
