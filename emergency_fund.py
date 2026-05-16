from datetime import datetime

class EmergencyFund:
    """应急金管理模块 - 帮助用户建立应急储蓄意识"""
    
    def __init__(self):
        self.SUGGESTED_MONTHS = 3  # 建议预留3个月生活费作为应急金
    
    def calculate_target(self, monthly_expense):
        """计算应急金目标金额"""
        target_amount = monthly_expense * self.SUGGESTED_MONTHS
        return {
            'target_amount': target_amount,
            'suggested_months': self.SUGGESTED_MONTHS,
            'monthly_expense': monthly_expense
        }
    
    def calculate_progress(self, current_amount, target_amount):
        """计算应急金进度"""
        if target_amount == 0:
            return 0
        return (current_amount / target_amount) * 100
    
    def generate_status_message(self, current_amount, monthly_expense):
        """生成应急金状态报告"""
        target = self.calculate_target(monthly_expense)
        progress = self.calculate_progress(current_amount, target['target_amount'])
        
        message = "💰 **应急金状态**\n\n"
        message += f"📊 当前应急金：{current_amount}元\n"
        message += f"🎯 建议目标：{target['target_amount']}元（{self.SUGGESTED_MONTHS}个月生活费）\n"
        message += f"📈 完成进度：{progress:.1f}%\n\n"
        
        if progress >= 100:
            message += "🎉 太棒了！你的应急金已经达标！继续保持！"
        elif progress >= 80:
            message += "🔥 差一点就完成了！再加把劲！"
        elif progress >= 50:
            message += "💪 已经完成一半了，继续加油！"
        elif progress >= 20:
            message += "👍 开始积累应急金是个好习惯，坚持下去！"
        else:
            message += "🌱 应急金是理财的第一道防线，建议从每月结余中划出一部分作为应急金哦~"
        
        return message
    
    def suggest_monthly_saving(self, monthly_expense, current_emergency, target_months=3):
        """建议每月应急金储蓄金额"""
        target = monthly_expense * target_months
        gap = target - current_emergency
        
        if gap <= 0:
            return "✅ 应急金已达标！可以考虑其他理财目标~"
        
        # 建议在6个月内完成
        monthly_saving = gap / 6
        
        return f"💡 建议每月存 {monthly_saving:.2f}元，约6个月可完成{target_months}个月应急金目标~"
    
    def get_emergency_tips(self):
        """获取应急金相关建议"""
        tips = [
            '💡 **流动性优先**：应急金应放在活期存款或货币基金中，随时可取',
            '💡 **逐步积累**：不用一下子存够，可以每月定期存入',
            '💡 **专款专用**：应急金只用于真正的紧急情况，不要随意动用',
            '💡 **定期检查**：每月查看应急金进度，保持充足储备',
            '💡 **动态调整**：随着生活费增加，应急金目标也应相应提高'
        ]
        return "\n\n".join(tips)