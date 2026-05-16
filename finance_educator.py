from system_prompt import SENSITIVE_WORDS

class FinanceEducator:
    FINANCIAL_TERMS = {
        '公募基金': {
            'explanation': '就像和一群朋友一起拼车——大家把钱凑起来，请专业司机（基金经理）开车，一起到达目的地（赚钱）。风险和收益都由大家共同承担。',
            'key_points': ['分散投资', '专业管理', '门槛低']
        },
        '私募基金': {
            'explanation': '类似高端拼车服务，只有特定的人（高净值人群）才能参加，门槛很高，但可能有更高的收益潜力。',
            'key_points': ['高门槛', '特定人群', '灵活性高']
        },
        '指数基金': {
            'explanation': '就像跟着整个车队一起走，不选特定的车，而是复制整个市场的表现。比如沪深300指数基金，就是跟着300只大公司股票走。',
            'key_points': ['被动投资', '费用低', '市场平均收益']
        },
        'ETF': {
            'explanation': '可以在股票市场上买卖的指数基金，像买股票一样方便，但本质是基金。',
            'key_points': ['场内交易', '实时价格', '流动性好']
        },
        '定投': {
            'explanation': '定期定额投资，就像每个月固定存一笔钱到基金里，不管市场涨跌都坚持买，长期下来可以平摊成本。',
            'key_points': ['纪律性', '平摊成本', '适合新手']
        },
        '年化收益率': {
            'explanation': '把不同时间的收益换算成一年的收益率，方便比较。比如1个月赚了1%，年化就是12%。',
            'key_points': ['标准化', '便于比较', '复利计算']
        },
        '复利': {
            'explanation': '利滚利，就像滚雪球一样，利息也会产生新的利息。爱因斯坦说这是世界第八大奇迹。',
            'key_points': ['长期效应', '越早开始越好', '指数增长']
        },
        '分散投资': {
            'explanation': '不要把鸡蛋放在同一个篮子里，把钱投资在不同类型的资产上，降低风险。',
            'key_points': ['降低风险', '资产配置', '不把鸡蛋放一个篮子']
        },
        '流动性': {
            'explanation': '资产变现的方便程度。现金流动性最高，房子流动性最低。',
            'key_points': ['变现速度', '紧急备用金', '资产配置']
        },
        '风险偏好': {
            'explanation': '你能承受多大的投资波动。保守型喜欢稳，激进型能接受大起大落。',
            'key_points': ['保守型', '稳健型', '激进型']
        }
    }
    
    SCAM_PATTERNS = {
        '校园贷': {
            'warning': '⚠️ 请注意：校园贷是国家明令禁止的非法借贷行为！',
            'explanation': '所谓"日息万分之五"换算成年化利率高达18.25%，远超正常理财收益，属于典型的高利贷陷阱！',
            'advice': '理财第一步是保住本金，请务必远离校园贷！如有资金需求，请通过正规渠道申请助学贷款。'
        },
        '高息群': {
            'warning': '⚠️ 警惕！"高息群"通常是诈骗陷阱！',
            'explanation': '声称"日息1%"、"月入30%"等超高收益，都是庞氏骗局的典型特征。',
            'advice': '记住：高收益必然伴随高风险，年化超过15%的承诺都需要极度警惕！'
        },
        '兼职垫资': {
            'warning': '⚠️ "兼职垫资"是常见的诈骗手段！',
            'explanation': '以"刷单"、"代付"等名义要求你先垫付资金的，100%是诈骗！',
            'advice': '正规兼职不会要求你先交钱！保护好自己的钱包，不要轻易转账给陌生人。'
        },
        '传销': {
            'warning': '⚠️ 警惕传销陷阱！',
            'explanation': '以"拉人头"、"入门费"为特征，靠发展下线赚钱而非销售真实产品。',
            'advice': '远离任何需要"发展下线"才能赚钱的项目，保护自己和身边的同学！'
        }
    }
    
    def explain_term(self, term):
        term = term.replace('解释', '').replace('什么是', '').strip()
        
        if term in self.FINANCIAL_TERMS:
            data = self.FINANCIAL_TERMS[term]
            response = f"📚 **{term}**\n\n"
            response += f"{data['explanation']}\n\n"
            response += "💡 关键点：\n"
            for point in data['key_points']:
                response += f"  - {point}\n"
            return response
        
        return f"抱歉，我暂时还不了解「{term}」这个概念。你可以问我其他金融术语哦~"
    
    def detect_scam(self, text):
        for word in SENSITIVE_WORDS:
            if word in text:
                return self.generate_scam_warning(word)
        return None
    
    def generate_scam_warning(self, keyword):
        for pattern, content in self.SCAM_PATTERNS.items():
            if keyword in pattern or pattern in keyword:
                return f"{content['warning']}\n\n{content['explanation']}\n\n{content['advice']}"
        
        return f"⚠️ 警告：你提到的「{keyword}」可能涉及金融风险或诈骗！\n\n请务必保持警惕，不要轻易相信高收益承诺，保护好自己的财产安全。如有疑问，建议咨询学校辅导员或正规金融机构。"
    
    def get_basic_tips(self):
        tips = [
            '💡 **先存后花**：发生活费后先存一部分，剩下的再花',
            '💡 **应急金**：建议预留3-6个月生活费作为应急储备',
            '💡 **记账习惯**：每天花1分钟记录支出，月底复盘',
            '💡 **远离高息诱惑**：年化超过15%的承诺要极度警惕',
            '💡 **分散投资**：不要把所有钱放在同一个地方',
            '💡 **学习理财**：先学习基础知识，再开始投资'
        ]
        return "\n\n".join(tips)
    
    def calculate_annual_rate(self, daily_rate):
        """计算日利率对应的年化利率"""
        annual_rate = (1 + daily_rate) ** 365 - 1
        return annual_rate * 100
