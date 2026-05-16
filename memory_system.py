import json
import os
from datetime import datetime

MEMORY_FILE = 'user_memory.json'

class MemorySystem:
    def __init__(self):
        self.memory = self.load_memory()
    
    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_memory()
        return self.get_default_memory()
    
    def get_default_memory(self):
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
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def set_budget(self, amount):
        self.memory['monthly_budget'] = amount
        self.save_memory()
    
    def add_expense(self, amount, category, description=''):
        self.memory['spent_amount'] += amount
        record = {
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now().isoformat()
        }
        self.memory['spending_history'].append(record)
        self.save_memory()
    
    def get_spent_amount(self):
        return self.memory['spent_amount']
    
    def get_budget(self):
        return self.memory['monthly_budget']
    
    def add_saving_goal(self, name, target_amount, deadline, priority='medium'):
        goal = {
            'id': len(self.memory['saving_goals']) + 1,
            'name': name,
            'target_amount': target_amount,
            'current_amount': 0,
            'deadline': deadline,
            'priority': priority,
            'created_at': datetime.now().isoformat()
        }
        self.memory['saving_goals'].append(goal)
        self.save_memory()
    
    def update_saving_progress(self, goal_id, amount):
        for goal in self.memory['saving_goals']:
            if goal['id'] == goal_id:
                goal['current_amount'] += amount
                self.save_memory()
                return True
        return False
    
    def get_saving_goals(self):
        return self.memory['saving_goals']
    
    def set_risk_preference(self, preference):
        valid_preferences = ['保守型', '稳健型', '激进型']
        if preference in valid_preferences:
            self.memory['risk_preference'] = preference
            self.save_memory()
            return True
        return False
    
    def get_risk_preference(self):
        return self.memory['risk_preference']
    
    def get_spending_history(self, days=30):
        history = []
        cutoff = datetime.now() - datetime.timedelta(days=days)
        for record in self.memory['spending_history']:
            record_date = datetime.fromisoformat(record['date'])
            if record_date >= cutoff:
                history.append(record)
        return history
    
    def reset_monthly_data(self):
        self.memory['spent_amount'] = 0
        self.save_memory()
    
    def get_budget_status(self):
        budget = self.memory['monthly_budget']
        spent = self.memory['spent_amount']
        if budget == 0:
            return {'status': 'no_budget', 'percentage': 0}
        percentage = (spent / budget) * 100
        if percentage >= 100:
            return {'status': 'over_budget', 'percentage': percentage}
        elif percentage >= 90:
            return {'status': 'warning', 'percentage': percentage}
        elif percentage >= 70:
            return {'status': 'caution', 'percentage': percentage}
        else:
            return {'status': 'safe', 'percentage': percentage}
    
    def add_income(self, amount, category, description=''):
        record = {
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now().isoformat()
        }
        self.memory['income_history'].append(record)
        self.save_memory()
    
    def get_income_history(self, days=30):
        history = []
        cutoff = datetime.now() - datetime.timedelta(days=days)
        for record in self.memory.get('income_history', []):
            record_date = datetime.fromisoformat(record['date'])
            if record_date >= cutoff:
                history.append(record)
        return history
    
    def get_total_income(self):
        return sum(record['amount'] for record in self.memory.get('income_history', []))
    
    def get_emergency_fund(self):
        return self.memory.get('emergency_fund', 0)
    
    def add_emergency_fund(self, amount):
        self.memory['emergency_fund'] = self.memory.get('emergency_fund', 0) + amount
        self.save_memory()
    
    def set_emergency_fund(self, amount):
        self.memory['emergency_fund'] = amount
        self.save_memory()
