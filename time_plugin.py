from datetime import datetime

class TimePlugin:
    def get_current_time(self):
        return datetime.now()
    
    def get_day_of_month(self):
        return datetime.now().day
    
    def get_month(self):
        return datetime.now().month
    
    def get_year(self):
        return datetime.now().year
    
    def get_weekday(self):
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[datetime.now().weekday()]
    
    def is_beginning_of_month(self):
        return self.get_day_of_month() <= 5
    
    def is_end_of_month(self):
        today = datetime.now()
        next_month = today.replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        return (last_day - today).days <= 5
    
    def get_month_phase(self):
        day = self.get_day_of_month()
        if day <= 10:
            return 'beginning'
        elif day <= 20:
            return 'middle'
        else:
            return 'end'
    
    def get_phase_description(self):
        phase = self.get_month_phase()
        if phase == 'beginning':
            return '月初（发生活费啦！💰）'
        elif phase == 'middle':
            return '月中（花钱要节制哦~）'
        else:
            return '月末（吃土模式开启？😢）'
    
    def get_season(self):
        month = self.get_month()
        if month in [3, 4, 5]:
            return '春天'
        elif month in [6, 7, 8]:
            return '夏天'
        elif month in [9, 10, 11]:
            return '秋天'
        else:
            return '冬天'
    
    def get_special_events(self):
        today = datetime.now()
        month = today.month
        day = today.day
        
        events = []
        
        if month == 1 and day == 1:
            events.append('🎆 元旦')
        elif month == 2 and day == 14:
            events.append('💝 情人节')
        elif month == 3 and day == 8:
            events.append('👩 妇女节')
        elif month == 3 and day == 15:
            events.append('🌍 消费者权益日')
        elif month == 4 and day == 1:
            events.append('🎭 愚人节')
        elif month == 5 and day == 1:
            events.append('💪 劳动节')
        elif month == 5 and day == 4:
            events.append('🌟 青年节')
        elif month == 6 and day == 1:
            events.append('👶 儿童节')
        elif month == 9 and day == 10:
            events.append('👨‍🏫 教师节')
        elif month == 10 and day == 1:
            events.append('🇨🇳 国庆节')
        elif month == 12 and day == 25:
            events.append('🎄 圣诞节')
        
        # 考试季提醒
        if month in [6, 12]:
            events.append('📚 考试季')
        # 毕业季
        if month == 6:
            events.append('🎓 毕业季')
        # 开学季
        if month == 9:
            events.append('🎒 开学季')
        
        return events
    
    def generate_time_based_message(self):
        message = f"⏰ 现在是{self.get_year()}年{self.get_month()}月{self.get_day_of_month()}日，{self.get_weekday()}，{self.get_phase_description()}"
        
        events = self.get_special_events()
        if events:
            message += "\n\n📅 今日特别提醒："
            for event in events:
                message += f"\n  - {event}"
        
        return message
    
    def get_spending_strategy(self):
        phase = self.get_month_phase()
        
        if phase == 'beginning':
            return {
                'strategy': 'relaxed',
                'message': '刚发生活费，可以适当放松，但记得先存一部分哦！',
                'emoji': '💰'
            }
        elif phase == 'middle':
            return {
                'strategy': 'normal',
                'message': '月中啦，检查一下预算使用情况，合理规划后续支出~',
                'emoji': '📊'
            }
        else:
            return {
                'strategy': 'tight',
                'message': '月末了，看看还剩多少预算，准备迎接下个月！',
                'emoji': '💸'
            }
