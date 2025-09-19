import os
import json
import hashlib
import inspect
import sys
from datetime import datetime

class AntiPiracy:
    def __init__(self):
        self.checksum_file = "data/app_checksum.dat"
        self.suspicious_activities = []
    
    def detect_tampering(self):
        """كشف التلاعب بالبرنامج"""
        checks = [
            self.check_file_integrity(),
            self.check_debugger(),
            self.check_virtual_machine(),
            self.check_runtime_modifications(),
            self.check_license_tampering()
        ]
        
        return any(checks)
    
    def check_file_integrity(self):
        """التحقق من سلامة الملفات"""
        current_checksum = self.calculate_checksum()
        saved_checksum = self.load_checksum()
        
        if saved_checksum and current_checksum != saved_checksum:
            self.log_suspicious("تغيير في ملفات البرنامج")
            return True
        
        # حفظ checksum جديد إذا لم يكن موجوداً
        if not saved_checksum:
            self.save_checksum(current_checksum)
        
        return False
    
    def calculate_checksum(self):
        """حساب checksum للبرنامج"""
        files_to_check = ["main.py", "ai_module.py", "data_manager.py"]
        total_hash = hashlib.sha256()
        
        for file in files_to_check:
            if os.path.exists(file):
                try:
                    with open(file, 'rb') as f:
                        content = f.read()
                        total_hash.update(content)
                        total_hash.update(file.encode())
                except:
                    pass
        
        return total_hash.hexdigest()
    
    def check_debugger(self):
        """كشف محاولات التصحيح"""
        try:
            # طرق كشف الdebugger
            if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
                self.log_suspicious("اكتشاف debugger")
                return True
        except:
            pass
        return False
    
    def check_virtual_machine(self):
        """كشف التشغيل على virtual machine"""
        try:
            # بعض علامات الVM
            vm_indicators = [
                "vbox", "vmware", "qemu", "xen", "virtual",
                "hyperv", "parallels", "kvm"
            ]
            
            # التحقق من أسماء الملفات والمسارات
            for root, dirs, files in os.walk("/proc"):
                for name in dirs + files:
                    if any(indicator in name.lower() for indicator in vm_indicators):
                        self.log_suspicious("اكتشاف virtual machine")
                        return True
                        
        except:
            pass
        return False
    
    def check_runtime_modifications(self):
        """كشف التعديلات أثناء التشغيل"""
        try:
            # التحقق من تعديل الذاكرة
            current_frame = inspect.currentframe()
            if current_frame and current_frame.f_back:
                # إذا كان هناك استدعاءات غير طبيعية
                self.log_suspicious("تعديلات أثناء التشغيل")
                return True
        except:
            pass
        return False
    
    def check_license_tampering(self):
        """كشف التلاعب بملفات الترخيص"""
        license_file = "data/license.lic"
        if os.path.exists(license_file):
            try:
                with open(license_file, 'r', encoding='utf-8') as f:
                    license_data = json.load(f)
                
                # التحقق من التوقيع الرقمي
                if "signature" in license_data:
                    signature = license_data.pop("signature")
                    calculated = self.sign_data(license_data)
                    if signature != calculated:
                        self.log_suspicious("تلاعب بملف الترخيص")
                        return True
            except:
                self.log_suspicious("ملف الترخيص تالف")
                return True
        return False
    
    def sign_data(self, data):
        """توقيع البيانات رقمياً"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def log_suspicious(self, activity):
        """تسيب النشاط المشبوه"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.suspicious_activities.append(f"{timestamp} - {activity}")
        
        # حفظ السجل
        self.save_activity_log()
    
    def save_activity_log(self):
        """حفظ سجل النشاط المشبوه"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/security.log", "w", encoding='utf-8') as f:
                for activity in self.suspicious_activities:
                    f.write(activity + "\n")
        except:
            pass
    
    def load_checksum(self):
        """تحميل الchecksum المحفوظ"""
        try:
            if os.path.exists(self.checksum_file):
                with open(self.checksum_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    def save_checksum(self, checksum):
        """حفظ الchecksum"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.checksum_file, 'w', encoding='utf-8') as f:
                f.write(checksum)
        except:
            pass
    
    def take_protective_action(self):
        """اتخاذ إجراء وقائي"""
        if self.detect_tampering():
            # إجراءات مختلفة حسب مستوى الخطورة
            actions = [
                self.limit_features,
                self.show_warning,
                self.close_application
            ]
            
            # تنفيذ إجراء عشوائي (يصعب التوقع)
            import random
            action = random.choice(actions)
            action()
    
    def limit_features(self):
        """تقييد الميزات"""
        # يمكنك تقييد الوصول لبعض الميزات
        pass
    
    def show_warning(self):
        """عرض تحذير"""
        # سيتم تنفيذ هذا في الواجهة
        return "⚠️ تم اكتشاف نشاط مشبوه. يرجى استخدام نسخة أصلية."
    
    def close_application(self):
        """إغلاق التطبيق"""
        sys.exit(0)