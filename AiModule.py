# ai_module.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import random
from datetime import datetime, timedelta

class AIFinancialAdvisor:
    def __init__(self):
        self.spending_model = LinearRegression()
        self.savings_model = LinearRegression()
    
    def analyze_spending_patterns(self, expenses):
        """Analyze spending patterns using a local model"""
        if len(expenses) < 2:
            return "💡 Add more data to analyze spending patterns."
        
        try:
            # تحليل البيانات
            salaries = np.array([e['salary'] for e in expenses]).reshape(-1, 1)
            totals = np.array([e['transport'] + e['food'] + e['internet'] + e['credit'] + e['personal'] 
                             for e in expenses])
            
            # تدريب النموذج
            self.spending_model.fit(salaries, totals)
            
            # التنبؤ
            last_salary = salaries[-1][0]
            next_salary = last_salary * 1.1  # افتراض زيادة 10%
            predicted_spending = self.spending_model.predict([[next_salary]])[0]
            
            return f" Expected spending: with salary {next_salary:,.0f}، Expected spending: {predicted_spending:,.0f}"
            
        except Exception as e:
            return f" Parsing error: {str(e)}"
    
    def get_smart_recommendations(self, expenses):
        """Smart recommendations based on spending patterns"""
        if not expenses:
            return " Start logging expenses to get personalized recommendations."
        
        # تحليل الفئات
        categories = ['transport', 'food', 'internet', 'credit', 'personal']
        arabic_categories = {
            'transport': 'Transportation',
            'food': 'food', 
            'internet': 'Internet',
            'credit': 'Credit',
            'personal': 'Personal'
        }
        
        last_expense = expenses[-1]
        category_values = {cat: last_expense[cat] for cat in categories}
        
        # العثور على أعلى إنفاق
        highest_cat = max(category_values, key=category_values.get)
        highest_value = category_values[highest_cat]
        
        # قاعدة معرفة للتوصيات
        recommendations_db = {
            'transport': [
                " Try shared transportation to save 30% on transportation costs.",
                " Use public transportation two days a week.",
                " Short distances: Walk instead of driving."
            ],
            'food': [
                " Plan meals for the week to avoid eating out.",
                " Buy grains and staples in bulk.",
                " Reduce eating out at restaurants"
            ],
            'internet': [
                " Check your current internet package, there may be better offers.",
                " use WiFi Free in public places when available",
                " Turn off the internet at night to save energy."
            ],
            'credit': [
                " Pay the balance in full each month to avoid interest.",
                " Reduce credit card use for small purchases.",
                " Review your statement to find unnecessary subscriptions."
            ],
            'personal': [
                " Make a shopping list and stick to it.",
                " Reduce impulse purchases online",
                " Set a monthly budget for personal expenses."
            ]
        }
        
        # اختيار توصية عشوائية
        recommendation = random.choice(recommendations_db[highest_cat])
        
        return f" highest spending: {arabic_categories[highest_cat]} ({highest_value:,})\n{recommendation}"
    
    def predict_savings_goals(self, savings_data, target_amount):
        """Predict when you will achieve your savings goal"""
        if len(savings_data) < 3:
            return "⏳ Add at least 3 months of data for forecasting."
        
        try:
            # تحليل معدل الادخار
            saved_amounts = [s['saved_amount'] for s in savings_data]
            dates = [datetime.strptime(s.get('date', '01/01/2023'), '%m/%d/%Y') for s in savings_data]
            
            # حساب متوسط الادخار الشهري
            monthly_savings = np.mean(saved_amounts[-3:])  # آخر 3 أشهر
            
            if monthly_savings <= 0:
                return "📉 You need to increase your savings rate to achieve the goal."
            
            # حساب الوقت المطلوب
            months_needed = target_amount / monthly_savings
            target_date = datetime.now() + timedelta(days=months_needed * 30)
            
            return f"📈 Average savings: {monthly_savings:,.0f} Monthly, you will achieve {target_amount:,.0f} Throw {months_needed:.1f} Months (≈ {target_date.strftime('%b %Y')})"
            
        except Exception as e:
            return f" prediction error: {str(e)}"
    
    def detect_spending_anomalies(self, expenses):
        """Detecting abnormal spending"""
        if len(expenses) < 4:
            return " Add at least 4 months to detect abnormal patterns."
        
        try:
            # حساب متوسط الإنفاق
            spending_totals = [e['transport'] + e['food'] + e['internet'] + e['credit'] + e['personal'] 
                             for e in expenses]
            
            avg_spending = np.mean(spending_totals[:-1])  # كل البيانات ما عدا الأخيرة
            std_spending = np.std(spending_totals[:-1])
            
            current_spending = spending_totals[-1]
            
            # كشف الشذوذ (أكثر من انحرافين معياريين)
            if current_spending > avg_spending + 2 * std_spending:
                return f" abnormal spending: {current_spending:,.0f} (Average:{avg_spending:,.0f})"
            elif current_spending < avg_spending - 2 * std_spending:
                return f"✅ Spending less than usual: {current_spending:,.0f} (Provided {avg_spending - current_spending:,.0f})"
            else:
                return f" Spending is normal: {current_spending:,.0f} (Within the expected range)"
                
        except Exception as e:
            return f" Pattern detection error:{str(e)}"
    
    def generate_financial_tips(self):
        """Random financial tips from a local knowledge base"""
        tips_arabic = [
            " Save 15% of your income every month",
            " Set clear and measurable financial goals.",
            " Track your expenses daily for a month",
            " Buy needs, not wants.",
            " Create an emergency fund for 3-6 months.",
            " Reduce high-interest debt first.",
            " Invest in your financial education",
            " Review your budget every month.",
            " Pay yourself first (saving before spending)",
            " Use finance apps to monitor your spending.",
            " Avoid impulse purchases",
            " Increase your income with additional sources",
            " Learn to cook at home to save money",
            " Car maintenance prevents major expenses later.",
            " Use your credit card wisely."
        ]
        
        return random.choice(tips_arabic)

# نموذج محلي بديل لـ ChatGPT
class LocalChatAI:
    def __init__(self):
        self.responses_db = {
            "saving": [
                "Start by saving 10% of your income and gradually increase the percentage.",
                "Use the 50-30-20 rule: 50% for needs, 30% for wants, 20% for savings.",
                "Create separate accounts for savings and spending."
            ],
            "investment": [
                "Invest in your education first, it is the best investment.",
                "Diversify your investments to reduce risk.",
                "Start investing in low-cost index funds."
            ],
            "budget": [
                "Set a realistic and achievable budget.",
                "Review your budget weekly and adapt to changes.",
                "Set aside an amount for unexpected expenses."
            ],
            "religion": [
                "Focus on paying off high-interest debt first.",
                "Negotiate better interest rates",
                "Avoid accumulating new debt while repaying."
            ]
        }
    
    def get_advice(self, question):
        """Simulate smart responses based on keywords in the question"""
        question_lower = question.lower()
        
        for keyword, responses in self.responses_db.items():
            if keyword in question_lower:
                return random.choice(responses)
        
        return "Focus on regular savings and reviewing your expenses monthly. Small, consistent steps lead to big results."