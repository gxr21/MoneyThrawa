from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty, NumericProperty
from AiModule import AIFinancialAdvisor
from AiModule import LocalChatAI
from license import LicenseManager
from anti_piracy import AntiPiracy
import json
import os
from datetime import datetime

# Set window size for testing on computer
if platform != 'android':
    Window.size = (1920, 1080)

# Data Manager
class DataManager:
    def __init__(self):
        self.data_file = "expenses_data.json"
        self.data = {
            "expenses": [],
            "savings": [],
            "goals": ["Emergency", "Car", "Wedding", "House", "Travel", "Umrah", "Hajj", "General Savings"]
        }
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
        except:
            pass
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except:
            pass
from license import LicenseManager
from anti_piracy import AntiPiracy

class FinanceApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.license_manager = LicenseManager()
        self.anti_piracy = AntiPiracy()
    
    def on_start(self):
        """عند بدء التشغيل"""
        # التحقق من القرصنة
        if self.anti_piracy.detect_tampering():
           warning = self.anti_piracy.show_warning()
            # عرض التحذير للمستخدم
        
        # التحقق من الترخيص
        license_status = self.license_manager.validate_license()
        if not license_status["valid"]:
            self.show_license_screen(license_status)
    
    def show_license_screen(self, status):
        """عرض شاشة الترخيص"""
        # إنشاء واجهة إدخال الترخيص
        pass
    
    def activate_license(self, license_key):
        """تفعيل الترخيص"""
        result = self.license_manager.verify_license_key(license_key)
        if result["valid"]:
            # تم التفعيل بنجاح
            return True
        else:
            # فشل التفعيل
            return False
# Custom Button
class RoundedButton(Button):
    from kivy.properties import ListProperty

    color_rgb = ListProperty([0.2, 0.6, 0.3, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = '16sp'
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color_rgb)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[10])

# Custom Text Input
class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '16sp'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(10), dp(15)]
        self.background_color = (0.95, 0.98, 0.95, 1)

# Splash Screen
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'splash'
        
        with self.canvas.before:
            Color(0.1, 0.3, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', spacing=dp(30), padding=dp(40))
        
        title = Label(
            text=' Expense & Savings Manager',
            font_size='28sp',
            color=(1, 1, 1, 1),
            bold=True,
            halign='center'
        )
        
        welcome_text = Label(
            text='Your smart money management app\nAchieving financial goals made easy',
            font_size='16sp',
            color=(0.8, 0.9, 0.8, 1),
            halign='center'
        )
        
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.8, None),
            height=dp(6),
            pos_hint={'center_x': 0.5}
        )
        
        loading_label = Label(
            text='Loading...',
            font_size='14sp',
            color=(0.9, 0.95, 0.9, 1)
        )
        
        layout.add_widget(Widget())
        layout.add_widget(title)
        layout.add_widget(welcome_text)
        layout.add_widget(Widget())
        layout.add_widget(self.progress)
        layout.add_widget(loading_label)
        layout.add_widget(Widget())
        
        self.add_widget(layout)
        Clock.schedule_interval(self.update_progress, 0.05)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_progress(self, dt):
        if self.progress.value < 100:
            self.progress.value += 2
        else:
            Clock.unschedule(self.update_progress)
            Clock.schedule_once(self.go_to_main, 0.5)
            return False
    
    def go_to_main(self, dt):
        self.manager.current = 'main'

# Expense Card
class ExpenseCard(BoxLayout):
    def __init__(self, expense_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(140)
        self.spacing = dp(8)
        self.padding = dp(15)
        
        with self.canvas.before:
            Color(0.9, 0.95, 0.9, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Calculate values
        total_expenses = (expense_data['transport'] + expense_data['food'] + 
                         expense_data['internet'] + expense_data['credit'] + expense_data['personal'])
        net = expense_data['salary'] - total_expenses
        
        # Date and Salary
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
        date_label = Label(
            text=f" {expense_data['date']}",
            color=(0.2, 0.4, 0.2, 1),
            font_size='16sp',
            bold=True,
            size_hint_x=0.6,
            halign='left'
        )
        salary_label = Label(
            text=f"💰 {expense_data['salary']:,}",
            color=(0.1, 0.5, 0.1, 1),
            font_size='16sp',
            bold=True,
            size_hint_x=0.4,
            halign='right'
        )
        header.add_widget(date_label)
        header.add_widget(salary_label)
        
        # Expense details
        details_text = f"🚗 Transport: {expense_data['transport']:,} | 🍽️ Food: {expense_data['food']:,}\n🌐 Internet: {expense_data['internet']:,} | 💳 Credit: {expense_data['credit']:,} | 👤 Personal: {expense_data['personal']:,}"
        details = Label(
            text=details_text,
            color=(0.3, 0.3, 0.3, 1),
            font_size='12sp',
            text_size=(Window.width - dp(40), None),
            halign='left'
        )
        
        # Final result
        result = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
        total_label = Label(
            text=f"📊 Total: {total_expenses:,}",
            color=(0.6, 0.2, 0.2, 1),
            font_size='14sp',
            size_hint_x=0.5,
            halign='left'
        )
        net_label = Label(
            text=f"💎 Net: {net:,}",
            color=(0.1, 0.6, 0.1, 1),
            font_size='14sp',
            bold=True,
            size_hint_x=0.5,
            halign='right'
        )
        result.add_widget(total_label)
        result.add_widget(net_label)
        
        self.add_widget(header)
        self.add_widget(details)
        self.add_widget(result)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# License Screen (moved outside MainScreen)
class LicenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        title = Label(
            text="تفعيل الترخيص",
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        
        self.license_input = TextInput(
            hint_text="أدخل مفتاح الترخيص",
            size_hint_y=None,
            height=40
        )
        
        activate_btn = Button(
            text="تفعيل",
            size_hint_y=None,
            height=50,
            on_press=self.activate_license
        )
        
        self.status_label = Label(
            text="أدخل مفتاح الترخيص لتفعيل النسخة الكاملة",
            size_hint_y=None,
            height=30
        )
        
        layout.add_widget(title)
        layout.add_widget(self.license_input)
        layout.add_widget(activate_btn)
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def activate_license(self, instance):
        license_key = self.license_input.text.strip()
        # 'app' is not defined in this context; you may need to pass a reference or use App.get_running_app()
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'activate_license') and app.activate_license(license_key):
            self.status_label.text = "✅ تم التفعيل بنجاح!"
            self.status_label.color = (0, 1, 0, 1)
        else:
            self.status_label.text = "❌ مفتاح ترخيص غير صالح"
            self.status_label.color = (1, 0, 0, 1)

# Main Screen
class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.data_manager = DataManager()
        self.ai_advisor = AIFinancialAdvisor()
        self.chat_ai = LocalChatAI()
        main_layout = BoxLayout(orientation='vertical', padding=dp(10))
        
        title = Label(
            text=' Expense & Savings Manager',
            font_size='20sp',
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.6, 0.3, 1),
            bold=True
        )
        main_layout.add_widget(title)
        
        tabs = TabbedPanel(do_default_tab=False, tab_height=dp(48))
        
        # Expenses Tab
        expenses_tab = TabbedPanelItem(text='Expenses')
        expenses_tab.add_widget(self.create_expenses_tab())
        tabs.add_widget(expenses_tab)
        
        # Savings Tab
        savings_tab = TabbedPanelItem(text='Savings')
        savings_tab.add_widget(self.create_savings_tab())
        tabs.add_widget(savings_tab)
        
        # Add Tab
        add_tab = TabbedPanelItem(text='Add New')
        add_tab.add_widget(self.create_add_tab())
        tabs.add_widget(add_tab)
        
        # AI Tab
        ai_tab = TabbedPanelItem(text=' AI Insights')
        ai_tab.add_widget(self.create_ai_tab())
        tabs.add_widget(ai_tab)
        
        main_layout.add_widget(tabs)
        self.add_widget(main_layout)
    
    def get_ai_insights(self):
        """get all AI insight"""
        insights = []
        spending_analysis = self.ai_advisor.analyze_spending_patterns(
            self.data_manager.data['expenses']
        )
        insights.append(spending_analysis)
        
        if self.data_manager.data['expenses']:
            recommendations = self.ai_advisor.get_smart_recommendations(
                self.data_manager.data['expenses']
            )
            insights.append(recommendations)
        
            tips = self.ai_advisor.generate_financial_tips()
            insights.append(tips)
        
        return insights
    
    def show_ai_analysis(self, instance):
        """View AI analysis"""
        analysis = self.get_ai_analysis()
        self.ai_result_label.text = analysis

    def show_random_tips(self, instance):
        """Show random tips"""
        tip = self.ai_advisor.generate_financial_tips()
        self.ai_result_label.text = f"💡 Financial advice:\n\n{tip}"

    def get_ai_analysis(self):
        """Get the full analysis"""
        insights = []
        
        # تحليل الإنفاق
        if self.data_manager.data['expenses']:
            spending_analysis = self.ai_advisor.analyze_spending_patterns(
                self.data_manager.data['expenses']
            )
            insights.append(spending_analysis)
            
            # توصيات ذكية
            recommendations = self.ai_advisor.get_smart_recommendations(
                self.data_manager.data['expenses']
            )
            insights.append(recommendations)
            
            # كشف الشذوذ
            anomalies = self.ai_advisor.detect_spending_anomalies(
                self.data_manager.data['expenses']
            )
            insights.append(anomalies)
        else:
            insights.append(" No expense data to analyze.")
        
        # تحليل المدخرات
        if self.data_manager.data['savings']:
            savings_prediction = self.ai_advisor.predict_savings_goals(
                self.data_manager.data['savings'],
                100000  # افترض هدف 100,000
            )
            insights.append(savings_prediction)
        
        # إضافة نصيحة أخيرة
        final_tip = self.ai_advisor.generate_financial_tips()
        insights.append(f"💡 One last piece of advice: {final_tip}")
        
        return "\n\n".join(insights)

    def create_expenses_tab(self):
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(5))
        layout.bind(minimum_height=layout.setter('height'))
        
        for expense in self.data_manager.data['expenses']:
            card = ExpenseCard(expense)
            layout.add_widget(card)
        
        # Quick statistics
        total_salary = sum([e['salary'] for e in self.data_manager.data['expenses']])
        total_expenses = sum([e['transport'] + e['food'] + e['internet'] + e['credit'] + e['personal'] 
                            for e in self.data_manager.data['expenses']])
        
        summary_card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(15))
        with summary_card.canvas.before:
            Color(0.1, 0.5, 0.1, 0.2)
            summary_card.rect = RoundedRectangle(size=summary_card.size, pos=summary_card.pos, radius=[10])
        summary_card.bind(size=lambda x, y: setattr(summary_card.rect, 'size', x.size), 
                         pos=lambda x, y: setattr(summary_card.rect, 'pos', x.pos))
        
        summary_text = f'Total Salary: {total_salary:,}\nTotal Expenses: {total_expenses:,}\nNet Amount: {total_salary - total_expenses:,}'
        summary_label = Label(
            text=summary_text,
            color=(0.1, 0.4, 0.1, 1),
            font_size='14sp',
            bold=True
        )
        summary_card.add_widget(summary_label)
        layout.add_widget(summary_card)
        
        scroll.add_widget(layout)
        return scroll
    
    def create_ai_tab(self):
        """Create an AI tab"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # عنوان التبويب
        title = Label(
            text=' Smart Financial Assistant',
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.6, 1),
            size_hint_y=None,
            height=dp(40)
        )
        
        # حقل لعرض النتائج
        self.ai_result_label = Label(
            text='Click on "Data Analysis" to see recommendations.',
            size_hint_y=0.7,
            text_size=(Window.width - dp(40), None),
            halign='right',
            valign='top',
            color=(0.2, 0.2, 0.4, 1),
            font_size='14sp'
        )
        
        # أزرار التحكم
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        analyze_btn = Button(
            text=' Data analysis',
            background_color=(0.2, 0.6, 0.3, 1),
            on_press=self.show_ai_analysis
        )
        
        tips_btn = Button(
            text=' Random tips',
            background_color=(0.3, 0.5, 0.8, 1),
            on_press=self.show_random_tips
        )
        
        btn_layout.add_widget(analyze_btn)
        btn_layout.add_widget(tips_btn)
        
        layout.add_widget(title)
        layout.add_widget(self.ai_result_label)
        layout.add_widget(btn_layout)
        
        return layout
    def create_savings_tab(self):
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(5))
        layout.bind(minimum_height=layout.setter('height'))
        
        for saving in self.data_manager.data['savings']:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(15))
            
            with card.canvas.before:
                Color(0.85, 0.95, 0.85, 1)
                card.rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[10])
            card.bind(size=lambda x, y: setattr(card.rect, 'size', x.size),
                     pos=lambda x, y: setattr(card.rect, 'pos', x.pos))
            
            header = BoxLayout(orientation='horizontal')
            goal_label = Label(
                text=f' {saving["goal"]}',
                color=(0.1, 0.4, 0.1, 1),
                font_size='16sp',
                bold=True,
                size_hint_x=0.5,
                halign='left'
            )
            amount_label = Label(
                text=f' {saving["saved_amount"]:,}',
                color=(0.1, 0.6, 0.1, 1),
                font_size='16sp',
                bold=True,
                size_hint_x=0.5,
                halign='right'
            )
            header.add_widget(goal_label)
            header.add_widget(amount_label)
            
            details_text = f'Net Salary: {saving["net"]:,} | Cumulative: {saving["cumulative"]:,} | Remaining: {saving["remaining"]:,}'
            details = Label(
                text=details_text,
                color=(0.3, 0.3, 0.3, 1),
                font_size='12sp',
                halign='left'
            )
            
            card.add_widget(header)
            card.add_widget(details)
            layout.add_widget(card)
        
        total_saved = sum([s['saved_amount'] for s in self.data_manager.data['savings']])
        total_net = sum([s['net'] for s in self.data_manager.data['savings']])
        
        summary_card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(15))
        with summary_card.canvas.before:
            Color(0.1, 0.5, 0.1, 0.2)
            summary_card.rect = RoundedRectangle(size=summary_card.size, pos=summary_card.pos, radius=[10])
        summary_card.bind(size=lambda x, y: setattr(summary_card.rect, 'size', x.size), 
                         pos=lambda x, y: setattr(summary_card.rect, 'pos', x.pos))
        
        summary_text = f'Total Savings: {total_saved:,}\nTotal Net: {total_net:,}\nSavings Rate: {(total_saved/total_net*100 if total_net > 0 else 0):.1f}%'
        summary_label = Label(
            text=summary_text,
            color=(0.1, 0.4, 0.1, 1),
            font_size='14sp',
            bold=True
        )
        summary_card.add_widget(summary_label)
        layout.add_widget(summary_card)
        
        scroll.add_widget(layout)
        return scroll
    
    def create_add_tab(self):
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(15))
        layout.bind(minimum_height=layout.setter('height'))
        
        self.inputs = {}
        fields = [
            ('date', 'Date (e.g., 09/15/2025)'),
            ('salary', 'Total Salary'),
            ('transport', 'Transportation'),
            ('food', 'Food + Drinks'),
            ('internet', 'Internet'),
            ('credit', 'Credit Card'),
            ('personal', 'Personal Needs')
        ]
        
        for field_id, hint in fields:
            input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
            label = Label(text=hint, size_hint_x=0.4, halign='left')
            self.inputs[field_id] = CustomTextInput(hint_text=hint, size_hint_x=0.6)
            input_layout.add_widget(label)
            input_layout.add_widget(self.inputs[field_id])
            layout.add_widget(input_layout)
        
        goal_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        goal_label = Label(text='Savings Goal', size_hint_x=0.4, halign='left')
        self.goal_input = CustomTextInput(text=self.data_manager.data['goals'][0], size_hint_x=0.6)
        goal_layout.add_widget(goal_label)
        goal_layout.add_widget(self.goal_input)
        layout.add_widget(goal_layout)
        
        add_btn = RoundedButton(text='Add New Record')
        add_btn.bind(on_press=self.add_expense_record)
        layout.add_widget(add_btn)
        
        calc_btn = RoundedButton(text='Calculate Savings')
        calc_btn.bind(on_press=self.calculate_savings)
        layout.add_widget(calc_btn)

        clear_btn = RoundedButton(text='Clear All' , color_rgb=(0.8, 0.2, 0.2, 1))
        clear_btn.bind(on_press=self.clear_all_fields)
        layout.add_widget(clear_btn)
        self.result_label = Label(
            text='',
            size_hint_y=None,
            height=dp(50),
            # color=(0.8, 0.2, 0.2, 1),
            font_size='14sp'
        )
        layout.add_widget(self.result_label)
        
        scroll.add_widget(layout)
        return scroll
    
    def add_expense_record(self, instance):
        try:
            if not self.inputs['salary'].text:
                self.result_label.text = 'Please enter a salary!'
                return
            
            date_str = self.inputs['date'].text
            if not date_str:
              date_str = datetime.now().strftime('%m/%d/%Y')
            
            new_expense = {
                'date': date_str,
                'salary': float(self.inputs['salary'].text or 0),
                'transport': float(self.inputs['transport'].text or 0),
                'food': float(self.inputs['food'].text or 0),
                'internet': float(self.inputs['internet'].text or 0),
                'credit': float(self.inputs['credit'].text or 0),
                'personal': float(self.inputs['personal'].text or 0)
            }
            
            self.data_manager.data['expenses'].append(new_expense)
            
            total_exp = sum([new_expense['transport'], new_expense['food'], new_expense['internet'], 
            new_expense['credit'], new_expense['personal']])
            net = new_expense['salary'] - total_exp
            saved = int(net * 0.15)
            
            cumulative = 0
            if self.data_manager.data['savings']:
                cumulative = self.data_manager.data['savings'][-1]['cumulative']
            
            new_saving = {
                'net': net,
                'saved_amount': saved,
                'goal': self.goal_input.text,
                'cumulative': cumulative + saved,
                'remaining': net - saved
            }
            self.data_manager.data['savings'].append(new_saving)
            
            self.data_manager.save_data()
            
            result_text = f'Record added successfully!\nNet: {net:,}\nSavings: {saved:,}'
            self.result_label.text = result_text
            
            for field in self.inputs.values():
                field.text = ''
                
        except ValueError:
            self.result_label.text = 'Please enter valid values!'
            
    def clear_all_fields(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='Are you sure you want to clear all fields?'))
        
        btn_layout = BoxLayout(spacing=5)
        
        # هنا التعديل: نمرر popup_ref إلى الدالة
        popup = Popup(title='Confirm Clear', content=content, size_hint=(0.7, 0.3))
        yes_btn = Button(text='Yes', on_press=lambda x: self._confirm_clear(popup))
        
        no_btn = Button(text='No', on_press=lambda x: popup.dismiss())
        
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)
        
        popup.open()
        
    def _confirm_clear(self, popup_instance):
        # الكود الأصلي للمسح هنا
        for field in self.inputs.values():
            field.text = ''
        self.goal_input.text = self.data_manager.data['goals'][0]
        self.result_label.text = ' All fields cleared!'
        self.result_label.color = (0.2, 0.6, 0.3, 1)
        
        # هنا التعديل: نستخدم المتغير الذي مررناه
        popup_instance.dismiss()

    def calculate_savings(self, instance):
        try:
            salary = float(self.inputs['salary'].text or 0)
            total_exp = sum([float(self.inputs[field].text or 0) 
                           for field in ['transport', 'food', 'internet', 'credit', 'personal']])
            net = salary - total_exp
            savings = net * 0.15
            
            result_text = f'Salary: {salary:,}\nExpenses: {total_exp:,}\nNet: {net:,}\nSavings (15%): {savings:,.0f}'
            self.result_label.text = result_text
        except:
            self.result_label.text = 'Error in data!'
 
# Main App
class ExpenseTrackerApp(App):
    def build(self):
        self.title = 'Expense & Savings Manager'
        
        sm = ScreenManager()
        splash = SplashScreen()
        main = MainScreen()
        
        sm.add_widget(splash)
        sm.add_widget(main)
        
        return sm

if __name__ == '__main__':
    ExpenseTrackerApp().run()
