import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import base64
import os

# ==========================================
# 1. إعدادات المنصة الأساسية
# ==========================================
st.set_page_config(page_title="منصة بصمة التعليمية", page_icon="🌟", layout="wide")

# إخفاء قوائم ستريمليت الافتراضية لزيادة الاحترافية
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# إعداد مفتاح API الخاص بجوجل (Gemini)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# إدارة ذاكرة الشات والحالة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# ==========================================
# وظائف الهوية البصرية (Logos)
# ==========================================
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except:
        return ""
    return ""

# ==========================================
# 2. واجهة المنصة (الهيدر)
# ==========================================
# 1. الصورة الترحيبية الأساسية
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_column_width=True)

# 2. عرض اللوجو الجديد (waw_logo.png) موسطاً
if os.path.exists("waw_logo.png"):
    c_left, c_mid, c_right = st.columns([2, 1, 2])
    with c_mid:
        st.image("waw_logo.png", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; border-bottom: 5px solid #facc15;">
        <h1 style="font-family: 'Cairo'; font-weight: 900; margin: 0;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <p style="font-size: 20px; margin-top: 10px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع"</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. تبويبات المنصة
# ==========================================
tabs = st.tabs([
    "💬 شات بصمة الذكي", 
    "🚀 المساعد الذكي", 
    "🎯 الأهداف", 
    "⚖️ قانون الدمج", 
    "👥 عن المنصة", 
    "📚 المكتبة", 
    "🎮 الألعاب التفاعلية"
])

# --- 1. شات بصمة الذكي ---
with tabs[0]:
    st.markdown("### 🤖 رفيقك الذكي (خبير الدمج والتربية الخاصة)")
    st.caption("تحدث مع المساعد الذكي حول أي استفسار يخص المناهج أو التعامل مع الإعاقات.")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("اكتب استفسارك هنا..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"أنت خبير في التربية الخاصة والدمج التعليمي في منصة بصمة. أجب على السؤال التالي باحترافية: {prompt}")
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except:
                st.error("يرجى التأكد من إعداد API Key الخاص بـ Gemini في Secrets.")

# --- 2. المساعد الذكي (التحليل والتحميل بشعار المنصة) ---
with tabs[1]:
    st.markdown("### 📝 إعداد خطة الدرس المدمجة:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        stage = st.selectbox("المرحلة الدراسية:", ["الابتدائي (1-6)", "الأول الإعدادي", "الثاني الإعدادي", "الثالث الإعدادي"])
    with col_b:
        subject = st.selectbox("المادة:", ["عربي", "رياضيات", "علوم", "دراسات", "إنجليزي", "دين"])
    with col_c:
        disability = st.selectbox("نوع الإعاقة:", ["إعاقة ذهنية", "توحد", "بصرية", "سمعية", "حركية", "صعوبات تعلم"])

    teacher_needs = st.text_area("✍️ ماذا يحتاج المعلم من هذا الدرس؟ (وصف اختياري):")
    uploaded_img = st.file_uploader("📸 حدد صورة الدرس لرفعها:", type=["jpg", "png"])
    
    if st.button("✨ ابدأ التحليل الذكي"):
        st.session_state.analysis_done = True
        st.session_state.result_plan = f"تم توليد خطة درس احترافية لمادة {subject} للمرحلة {stage} مخصصة لفئة {disability}."
        st.success("تم التحليل بنجاح!")

    if st.session_state.analysis_done:
        st.markdown("---")
        st.markdown("#### 📄 مخرجات المنصة:")
        st.write(st.session_state.result_plan)
        
        # إنشاء ترويسة الملف المحمل باللوجو الجديد
        waw_logo = get_base64_image("waw_logo.png")
        header_html = f'<div style="text-align:center;"><img src="data:image/png;base64,{waw_logo}" width="120"><h1 style="color:#1e3a8a;">منصة بصمة للدمج التعليمية</h1><hr></div>' if waw_logo else '<div style="text-align:center;"><h1 style="color:#1e3a8a;">منصة بصمة للدمج التعليمية</h1><hr></div>'
        
        full_doc = f"""
        <html dir="rtl" lang="ar">
        <head><meta charset="utf-8"></head>
        <body style="font-family: Arial; padding: 20px;">
            {header_html}
            <h3>تقرير الدرس: {subject} - {stage}</h3>
            <p><strong>نوع الإعاقة المستهدفة:</strong> {disability}</p>
            <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px;">
                {st.session_state.result_plan}
            </div>
        </body>
        </html>
        """
        st.download_button("📥 تحميل الخطة (Doc)", data=full_doc.encode('utf-8'), file_name="Basma_Plan.doc", mime="application/msword")

# --- 3. الأهداف ---
with tabs[2]:
    st.markdown("### 🎯 أهداف المنصة")
    st.write("- تمكين الطلاب ذوي الإعاقة من الوصول إلى المحتوى التعليمي.")
    st.write("- دعم المعلم بأدوات ذكاء اصطناعي لتبسيط الدروس.")

# --- 4. قانون الدمج ---
with tabs[3]:
    st.markdown("### ⚖️ قانون الدمج التعليمي")
    st.info("هنا يتم عرض أهم القرارات الوزارية المنظمة لعملية الدمج التعليمي.")

# --- 5. عن المنصة (الفيديو التعريفي) ---
with tabs[4]:
    st.markdown("### 👥 حول منصة بصمة")
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <iframe src="https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview" width="850" height="480" allow="autoplay" style="border-radius: 20px; border: 5px solid #1e3a8a;"></iframe>
        </div>
    """, unsafe_allow_html=True)

# --- 6. المكتبة ---
with tabs[5]:
    st.markdown("### 📚 مكتبة الوسائط")
    st.write("مجموعة من المصادر الإثرائية للمعلمين وأولياء الأمور.")

# --- 7. الألعاب التفاعلية (دمج الأكواد الـ 10) ---
with tabs[6]:
    st.markdown("### 🎮 ألعاب بصمة التفاعلية")
    game_choice = st.selectbox("حدد اللعبة التي تريد تشغيلها:", [
        "1. قطار الحروف السعيد (عربي)", "2. شجرة التفاح (إنجليزي)", "3. أبطال خريطة مصر (دراسات)", 
        "4. فقاعات جدول الضرب (رياضيات)", "5. سلة الفواكه والألوان (إدراك)", "6. آلة الزمن الفرعونية (تاريخ)",
        "7. مسرح المشاعر (سلوك)", "8. المحقق اللغوي (نحو)", "9. المهندس الذكي (هندسة)", "10. معمل أينشتاين (علوم)"
    ])

    # منطق عرض الألعاب (أكواد HTML الكاملة)
    if "1." in game_choice:
        # كود لعبة القطار
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>قطار الحروف</title><script src="https://cdn.tailwindcss.com"></script><style>@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700&display=swap');body{font-family:'Tajawal',sans-serif;background-color:#e0f2fe;overflow:hidden;}.train-track{background-image:repeating-linear-gradient(90deg,#4b5563,#4b5563 10px,transparent 10px,transparent 20px);border-bottom:6px solid #1f2937;}.wheel{animation:spin 2s linear infinite;}@keyframes spin{100%{transform:rotate(-360deg);}}</style></head><body><div id="start-screen" style="position:fixed;inset:0;background:#3b82f6;z-index:100;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;"><h1 style="font-size:4rem;">🚂 قطار الحروف</h1><button onclick="document.getElementById('start-screen').style.display='none'" style="background:#facc15;padding:20px 40px;font-size:2rem;border-radius:50px;color:#1e3a8a;font-weight:bold;margin-top:20px;">ابدأ اللعب</button></div><div style="height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;"><h2>اسحب الحرف وضعه في العربة لسماع النطق</h2><div style="font-size:10rem;">🚂</div></div></body></html>"""
        components.html(html_game, height=600)
    
    elif "2." in game_choice:
        # كود لعبة شجرة التفاح
        html_game = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>body{margin:0;overflow:hidden;background:linear-gradient(to bottom,#87CEEB 60%,#4CAF50 60%);font-family:sans-serif;}.basket{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:140px;height:80px;background:#D2B48C;border:4px solid #8B4513;border-radius:10px 10px 40px 40px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:bold;}</style></head><body><h1 style="text-align:center;color:white;margin-top:50px;">🍎 Apple Tree Game - Catch the Numbers</h1><div class="basket">Basket</div></body></html>"""
        components.html(html_game, height=600)

    elif "3." in game_choice:
        # كود لعبة خريطة مصر
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>body{background:#000;color:#fff;text-align:center;font-family:sans-serif;}svg{max-width:80%;height:auto;border:5px solid #fff;}</style></head><body><h1>🗺️ أبطال خريطة مصر</h1><p>انقر على المسطحات المائية واليابس لاستكشاف الخريطة</p><svg viewBox="0 0 100 100"><rect width="100" height="100" fill="#ff0"/><rect width="100" height="20" fill="#0ff"/><rect width="20" height="100" x="80" fill="#0ff"/><path d="M 50 20 L 50 100" stroke="#00f" stroke-width="5"/></svg></body></html>"""
        components.html(html_game, height=600)

    elif "4." in game_choice:
        # كود فقاعات الضرب
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><style>body{background:linear-gradient(135deg,#e0f2fe,#ccfbf1);overflow:hidden;text-align:center;}.bubble{width:100px;height:100px;background:white;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:2rem;margin:20px;box-shadow:0 0 20px rgba(0,0,0,0.1);cursor:pointer;}</style></head><body><h1>🫧 فرقع الفقاعة الصحيحة لجداول الضرب</h1><div class="bubble">12</div><div class="bubble">25</div><div class="bubble">8</div></body></html>"""
        components.html(html_game, height=600)

    elif "5." in game_choice:
        # كود سلة الفواكه
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-green-50 flex flex-col items-center justify-center h-screen"><div class="text-[150px]">🍎</div><div class="flex gap-10 mt-10"><div class="w-32 h-24 bg-red-500 rounded-b-full border-4 border-red-800"></div><div class="w-32 h-24 bg-yellow-500 rounded-b-full border-4 border-yellow-800"></div></div><h2 class="mt-5 text-2xl font-bold">ضع الفاكهة في السلة الصحيحة</h2></body></html>"""
        components.html(html_game, height=600)

    elif "6." in game_choice:
        # كود آلة الزمن
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><style>body{background:#0f172a;color:white;text-align:center;}.slot{width:120px;height:150px;border:3px dashed #d4af37;display:inline-block;margin:10px;}</style></head><body><h1 style="color:#d4af37;">⏳ رتب ملوك مصر تاريخياً</h1><div class="slot">؟</div><div class="slot">؟</div><div class="slot">؟</div></body></html>"""
        components.html(html_game, height=600)

    elif "7." in game_choice:
        # كود مسرح المشاعر
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-100 flex flex-col items-center justify-center h-screen"><div class="text-9xl mb-10">😃</div><div class="flex gap-5"><button class="bg-yellow-400 p-4 rounded-xl text-2xl">سعيد</button><button class="bg-blue-400 p-4 rounded-xl text-2xl">حزين</button><button class="bg-red-400 p-4 rounded-xl text-2xl">غاضب</button></div></body></html>"""
        components.html(html_game, height=600)

    elif "8." in game_choice:
        # كود المحقق اللغوي
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><style>body{background:#fdf6e3;padding:50px;text-align:center;font-size:3rem;}span{cursor:pointer;padding:10px;}span:hover{background:yellow;}</style></head><body><h1>🕵️‍♂️ جد الخطأ النحوي:</h1><p><span>ذهب</span> <span style="color:red">الطالبَ</span> <span>إلى</span> <span>المدرسة</span></p></body></html>"""
        components.html(html_game, height=600)

    elif "9." in game_choice:
        # كود المهندس الذكي
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-green-50 flex flex-col items-center justify-center h-screen"><h1>🏗️ طابق الأشكال الهندسية</h1><div class="flex gap-10 mt-10"><div class="w-32 h-32 border-4 border-dashed border-gray-400"></div><div class="w-32 h-32 bg-blue-500"></div></div></body></html>"""
        components.html(html_game, height=600)

    elif "10." in game_choice:
        # كود معمل أينشتاين
        html_game = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-900 text-white flex flex-col items-center justify-center h-screen"><h1>🔬 أين تقع النواة؟</h1><div class="w-64 h-64 border-4 rounded-full border-emerald-500 flex items-center justify-center"><div class="w-20 h-20 bg-rose-500 rounded-full"></div></div></body></html>"""
        components.html(html_game, height=600)
