# -*- mode: python ; coding: utf-8 -*-
# -*- coding: utf-8 -*-

block_cipher = None

# قائمة الملفات والمجلدات المطلوبة
added_files = [
    ('ai_module.py', '.'),  # ملف الذكاء الاصطناعي
    ('data_manager.py', '.'),  # ملف إدارة البيانات
    ('license_manager.py', '.'),  # نظام الترخيص
    ('anti_piracy.py', '.'),  # كاشف القرصنة
    ('data', 'data'),  # مجلد البيانات
]

# المكتبات المخفية التي يحتاجها البرنامج
hidden_imports = [
    'kivy',
    'kivy.app',
    'kivy.uix',
    'kivy.uix.boxlayout',
    'kivy.uix.label',
    'kivy.uix.button',
    'kivy.uix.textinput',
    'kivy.uix.screenmanager',
    'kivy.uix.tabbedpanel',
    'kivy.uix.scrollview',
    'kivy.uix.progressbar',
    'kivy.graphics',
    'kivy.core',
    'kivy.core.window',
    'kivy.metrics',
    'kivy.properties',
    'kivy.clock',
    
    # مكتبات الذكاء الاصطناعي
    'sklearn',
    'sklearn.linear_model',
    'sklearn.linear_model._base',
    'sklearn.utils',
    'sklearn.utils._weight_vector',
    'sklearn.exceptions',
    
    # مكتبات البيانات
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',
    'numpy.core._multiarray_tests',
    'numpy.lib',
    'numpy.random',
    
    # مكتبات النظام
    'json',
    'os',
    'sys',
    'datetime',
    'hashlib',
    'uuid',
    'socket',
    'inspect',
    'collections',
    'threading',
    'time',
    'calendar',
    
    # مكتبات إضافية
    'random',
    'math',
    're',
    'codecs',
    'struct',
    'functools',
    'itertools',
    'operator',
]

# استثناءات غير ضرورية لتقليل الحجم
excludes = [
    'tkinter',
    'matplotlib',
    'scipy',
    'pandas',
    'PIL',
    'pygame',
    'docutils',
    'pytest',
    'setuptools',
    'email',
    'http',
    'xml',
    'html',
    'unittest',
    'multiprocessing',
    'asyncio',
    'ssl',
    'sqlite3',
    'zoneinfo',
]

a = Analysis(
    ['app.py'],  # الملف الرئيسي
    pathex=[],  # مسارات إضافية
    binaries=[],  # ملفات ثنائية
    datas=added_files,  # الملفات الإضافية
    hiddenimports=hidden_imports,  # المكتبات المخفية
    hookspath=[],  # مسارات الhooks
    hooksconfig={},  # إعدادات الhooks
    runtime_hooks=[],  # runtime hooks
    excludes=excludes,  # الاستثناءات
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1,  # مستوى التحسين
)

# ضغط الملفات
pyz = PYZ(
    a.pure, 
    a.zipped_data, 
    cipher=block_cipher,
    optimize=1,
)

# إعداد ملف EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FinanceApp',  # اسم التطبيق
    debug=False,  # وضع التصحيح
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # استخدام UPX للضغط
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # إخفاء نافذة الأوامر
    icon='assets/icon.ico',  # الأيقونة (إذا موجودة)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    ascii=False,
    version='1.0.0',  # إصدار التطبيق
    company_name='YourCompany',
    file_description='المساعد المالي الذكي',
    legal_copyright='© 2024 YourCompany. All rights reserved.',
    product_name='FinanceApp',
    product_version='1.0.0',
    manifest=None,
    resources=[],
)

# إعداد مجلد التجميع
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FinanceApp',  # اسم المجلد
)

# إعداد التوزيع
app = BUNDLE(
    coll,
    name='FinanceApp.app',  # للمستخدمين النهائيين
    icon=None,
    bundle_identifier='com.yourcompany.financeapp',
    info_plist={
        'NSHumanReadableCopyright': '© 2024 YourCompany',
        'CFBundleDisplayName': 'FinanceApp',
        'CFBundleName': 'FinanceApp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.12.0',
    },
)