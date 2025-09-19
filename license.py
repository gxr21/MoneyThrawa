import json
import os
import hashlib
from datetime import datetime, timedelta
import socket
import uuid
class LicenseManager:
    def __init__(self):
        self.license_file = "data/license.lic"
        self.trial_days = 30
        self.license_data = self.load_license()
    
    def generate_hardware_id(self):
        """إنشاء ID فريد للجهاز"""
        try:
            # جمع معلومات الجهاز
            mac = uuid.getnode()
            hostname = socket.gethostname()
            hardware_id = f"{mac}_{hostname}"
            return hashlib.sha256(hardware_id.encode()).hexdigest()[:16]
        except:
            return "default_hardware_id"
    
    def create_license(self, license_key, days_valid=365):
        """إنشاء ترخيص جديد"""
        hardware_id = self.generate_hardware_id()
        license_data = {
            "license_key": license_key,
            "hardware_id": hardware_id,
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
            "expiry_date": (datetime.now() + timedelta(days=days_valid)).strftime("%Y-%m-%d"),
            "is_valid": True,
            "product_version": "1.0"
        }
        
        self.save_license(license_data)
        return license_data
    
    def validate_license(self, entered_key=None):
        """التحقق من صحة الترخيص"""
        # إذا لم يكن هناك ترخيص، بدء الفترة التجريبية
        if not self.license_data:
            return self.start_trial_period()
        
        # التحقق من الترخيص المدخل
        if entered_key:
            return self.verify_license_key(entered_key)
        
        # التحقق من الترخيص الحالي
        return self.check_current_license()
    
    def start_trial_period(self):
        """بدء الفترة التجريبية"""
        trial_data = {
            "is_trial": True,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=self.trial_days)).strftime("%Y-%m-%d"),
            "hardware_id": self.generate_hardware_id()
        }
        
        self.save_license(trial_data)
        return {
            "valid": True,
            "is_trial": True,
            "days_remaining": self.trial_days,
            "message": "فترة تجريبية لمدة 30 يوم"
        }
    
    def verify_license_key(self, license_key):
        """التحقق من مفتاح الترخيص"""
        # نظام تحقق بسيط (يمكنك تطويره)
        if self.validate_key_format(license_key):
            license_data = self.create_license(license_key)
            return {
                "valid": True,
                "is_trial": False,
                "message": "تم تفعيل الترخيص بنجاح",
                "expiry_date": license_data["expiry_date"]
            }
        return {
            "valid": False,
            "message": "مفتاح ترخيص غير صالح"
        }
    
    def validate_key_format(self, key):
        """التحقق من تنسيق مفتاح الترخيص"""
        # تنسيق: FIN-XXXX-XXXX-XXXX-XXXX
        if len(key) != 19:
            return False
        if not key.startswith("FIN-"):
            return False
        
        parts = key.split("-")
        if len(parts) != 5:
            return False
        
        # تحقق أن كل الأجزاء hexadecimal
        for part in parts[1:]:
            if not all(c in "0123456789ABCDEF" for c in part):
                return False
        
        return True
    
    def check_current_license(self):
        """التحقق من الترخيص الحالي"""
        if self.license_data.get("is_trial", False):
            return self.check_trial_status()
        else:
            return self.check_paid_license()
    
    def check_trial_status(self):
        """التحقق من الفترة التجريبية"""
        end_date = datetime.strptime(self.license_data["end_date"], "%Y-%m-%d")
        remaining_days = (end_date - datetime.now()).days
        
        if remaining_days <= 0:
            return {
                "valid": False,
                "message": "انتهت الفترة التجريبية"
            }
        
        return {
            "valid": True,
            "is_trial": True,
            "days_remaining": remaining_days,
            "message": f"متبقي {remaining_days} يوم من الفترة التجريبية"
        }
    
    def check_paid_license(self):
        """التحقق من الترخيص المدفوع"""
        expiry_date = datetime.strptime(self.license_data["expiry_date"], "%Y-%m-%d")
        
        if datetime.now() > expiry_date:
            return {
                "valid": False,
                "message": "انتهت مدة الترخيص"
            }
        
        # التحقق من تطابق hardware ID
        current_hardware = self.generate_hardware_id()
        if self.license_data.get("hardware_id") != current_hardware:
            return {
                "valid": False,
                "message": "الترخيص غير نشط على هذا الجهاز"
            }
        
        return {
            "valid": True,
            "is_trial": False,
            "message": "الترخيص فعال",
            "expiry_date": self.license_data["expiry_date"]
        }
    
    def load_license(self):
        """تحميل بيانات الترخيص"""
        try:
            if os.path.exists(self.license_file):
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_license(self, data):
        """حفظ بيانات الترخيص"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.license_data = data
        except:
            pass
    
    def generate_license_key(self, customer_id):
        """إنشاء مفتاح ترخيص (للاستخدام من قبل البائع)"""
        base_key = f"FIN-{customer_id:04d}"
        hash_part = hashlib.sha256(base_key.encode()).hexdigest()[:12].upper()
        return f"FIN-{hash_part[:4]}-{hash_part[4:8]}-{hash_part[8:12]}"