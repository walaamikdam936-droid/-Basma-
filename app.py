import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import base64
import os

# ==========================================
# 1. إعدادات المنصة الأساسية
# ==========================================
st.set_page_config(page_title="منصة بصمة التعليمية", page_icon="🌟", layout="wide")

# إخفاء قوائم ستريمليت وتنسيق التبويبات
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 5px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px 8px 0px 0px; padding: 10px 15px; font-weight: bold; border: 1px solid #e2e8f0; border-bottom: none; }
    .stTabs [aria-selected="true"] { background-color: #1e3a8a !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# إعداد مفتاح API الخاص بجوجل (Gemini)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""

# ==========================================
# 2. وظائف مساعدة (اللوجو)
# ==========================================
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except:
        return ""
    return ""

stages_list = [
    "الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي",
    "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي",
    "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي"
]
disabilities_list = ["إعاقة ذهنية", "توحد", "بصرية", "سمعية", "حركية", "صعوبات تعلم"]

# ==========================================
# 3. واجهة المنصة (الهيدر والشعار)
# ==========================================
if os.path.exists("waw_logo.png"):
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2: st.image("waw_logo.png", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; border-bottom: 5px solid #facc15;">
        <h1 style="font-family: 'Cairo'; font-weight: 900; margin: 0; font-size: 3rem;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <p style="font-size: 1.2rem; margin-top: 10px; color: #e0f2fe;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع"</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. تبويبات المنصة
# ==========================================
tabs = st.tabs([
    "💬 شات بصمة الذكي", "🚀 المساعد الذكي", "🎮 الألعاب التفاعلية", 
    "🎯 أهدافنا", "⚖️ قانون الدمج", "👥 من نحن", "📚 مكتبة الاستراتيجيات"
])

# ------------------------------------------
# 1. شات بصمة الذكي
# ------------------------------------------
with tabs[0]:
    st.markdown("### 🤖 رفيقك الذكي (خبير الدمج والتربية الخاصة)")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("اكتب استفسارك هنا..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"أنت خبير في التربية الخاصة والدمج في منصة بصمة. أجب باحترافية: {prompt}")
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except:
                st.error("يرجى التأكد من إعدادات المفتاح (API Key).")

# ------------------------------------------
# 2. المساعد الذكي (تم التفعيل الحقيقي للذكاء الاصطناعي)
# ------------------------------------------
with tabs[1]:
    st.markdown("### 📝 المساعد الذكي لتحليل الدروس وإنشاء الخطط")
    c1, c2, c3 = st.columns(3)
    with c1: stage = st.selectbox("حدد المرحلة الدراسية:", stages_list)
    with c2: subject = st.selectbox("حدد المادة:", ["اللغة العربية", "الرياضيات", "العلوم", "الدراسات الاجتماعية", "اللغة الإنجليزية", "التربية الدينية"])
    with c3: disability = st.selectbox("حدد نوع الإعاقة:", disabilities_list)

    teacher_desc = st.text_area("✍️ ماذا تحتاج من هذا الدرس؟ (توضيح الهدف أو النشاط):", height=100)
    uploaded_file = st.file_uploader("📸 حدد صورة الدرس لرفعها (اختياري):", type=["jpg", "png", "jpeg"])
    
    if st.button("✨ ابدأ التحليل وإنشاء الخطة"):
        with st.spinner("يقوم الذكاء الاصطناعي الآن بإعداد الخطة المخصصة..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                # بناء الـ Prompt الحقيقي للذكاء الاصطناعي
                ai_prompt = f"قم بإعداد خطة درس تفاعلية ومبسطة لمادة {subject} لطلاب {stage}. الخطة مخصصة لطلاب الدمج ذوي إعاقة: ({disability}). وصف المعلم: {teacher_desc}. اجعل الخطة تتضمن: 1. أهداف مبسطة 2. استراتيجية تدريس مناسبة للإعاقة 3. نشاط تفاعلي 4. طريقة التقييم."
                
                response = model.generate_content(ai_prompt)
                st.session_state.result_text = response.text
                st.session_state.analysis_done = True
                st.success("تم توليد الخطة بنجاح!")
            except Exception as e:
                st.error("حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. تأكد من إعدادات API Key.")
    
    if st.session_state.analysis_done:
        st.markdown("---")
        st.markdown("### 📄 نتيجة التحليل والخطة المقترحة:")
        st.write(st.session_state.result_text)
        
        # تصدير ملف Word
        logo_b64 = get_base64_image("waw_logo.png")
        img_tag = f'<img src="data:image/png;base64,{logo_b64}" width="120" style="margin-bottom:10px;">' if logo_b64 else ''
        doc_html = f"""<html dir="rtl"><head><meta charset="utf-8"></head><body style="font-family:Arial; padding:40px; text-align:right;">
            <div style="text-align:center; border-bottom:3px solid #1e3a8a; padding-bottom:20px;">
                {img_tag}
                <h1 style="color:#1e3a8a;">منصة بصمة للدمج التعليمية</h1>
                <h3>خطة درس: {subject} | {stage} | {disability}</h3>
            </div>
            <div style="padding:20px; font-size:16px;">{st.session_state.result_text.replace('**', '')}</div>
        </body></html>"""
        
        st.download_button("📥 تحميل الخطة كملف Word", data=doc_html.encode('utf-8'), file_name="Basma_Lesson_Plan.doc", mime="application/msword")

# ------------------------------------------
# 3. الألعاب التفاعلية (تم تضمين الأكواد الفعلية لتعمل)
# ------------------------------------------
with tabs[2]:
    st.markdown("### 🎮 نظام الألعاب التفاعلية الذكي")
    st.write("حدد بيانات الطالب ليقوم النظام باختيار وتفعيل اللعبة الأنسب له تلقائياً:")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1: g_stage = st.selectbox("حدد المرحلة:", ["الصفوف الأولى", "الصفوف العليا", "المرحلة الإعدادية"])
    with col_g2: g_dis = st.selectbox("حدد الإعاقة:", disabilities_list)
    with col_g3: g_sub = st.selectbox("حدد المادة المستهدفة:", ["اللغة العربية", "الرياضيات", "اللغة الإنجليزية", "الدراسات", "العلوم", "مهارات سلوكية"])

    if st.button("🎲 استخراج وتشغيل اللعبة"):
        chosen_game = ""
        game_html = ""
        
        # خوارزمية اختيار الألعاب
        if g_sub == "مهارات سلوكية":
            if g_dis in ["توحد", "صعوبات تعلم"]:
                chosen_game, game_html = "مسرح المشاعر والأخلاق", """<!DOCTYPE html><html dir="rtl"><body style="background:#f8fafc; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#1e3a8a; font-size:3rem;">🎭 مسرح المشاعر والأخلاق</h1><p style="font-size:2rem;">(لعبة تفاعلية للذكاء العاطفي)</p><div style="font-size:6rem; margin-top:20px; cursor:pointer;" onclick="alert('إجابة صحيحة!')">😃 😔 😡</div></body></html>"""
            else:
                chosen_game, game_html = "سلة الفواكه والألوان", """<!DOCTYPE html><html dir="rtl"><body style="background:#fef08a; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#854d0e; font-size:3rem;">🎨 سلة الفواكه والألوان</h1><p style="font-size:2rem;">(تنمية الإدراك الحسي والبصري)</p><div style="font-size:6rem;">🍎 🍌 🍊</div></body></html>"""
        elif g_sub == "اللغة العربية":
            if "الإعدادية" in g_stage:
                chosen_game, game_html = "المحقق اللغوي", """<!DOCTYPE html><html dir="rtl"><body style="background:#fdf6e3; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#dcb37b; font-size:3rem;">🕵️‍♂️ المحقق اللغوي</h1><p style="font-size:2rem; cursor:pointer;"><span style="margin:10px;">ذهب</span><span style="color:red; margin:10px;" onclick="alert('أحسنت! فاعل مرفوع')">الطالبَ</span><span style="margin:10px;">إلى المدرسة</span></p></body></html>"""
            else:
                chosen_game, game_html = "قطار الحروف السعيد", """<!DOCTYPE html><html dir="rtl"><body style="background:#e0f2fe; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#1e3a8a; font-size:3rem;">🚂 قطار الحروف السعيد</h1><div style="font-size:8rem;">🚂 🦁</div></body></html>"""
        elif g_sub == "الرياضيات":
            if "الإعدادية" in g_stage or "العليا" in g_stage:
                chosen_game, game_html = "المهندس الذكي", """<!DOCTYPE html><html dir="rtl"><body style="background:#f0fdf4; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#166534; font-size:3rem;">🏗️ المهندس الذكي</h1><div style="display:flex; justify-content:center; gap:20px; margin-top:30px;"><div style="width:100px; height:100px; background:blue;"></div><div style="width:0; height:0; border-left:50px solid transparent; border-right:50px solid transparent; border-bottom:100px solid red;"></div></div></body></html>"""
            else:
                chosen_game, game_html = "فقاعات جدول الضرب", """<!DOCTYPE html><html dir="rtl"><body style="background:#ccfbf1; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#0f766e; font-size:3rem;">🫧 فقاعات جدول الضرب</h1><div style="width:100px; height:100px; border-radius:50%; background:white; font-size:2rem; line-height:100px; margin:auto; cursor:pointer;" onclick="alert('أحسنت')">12</div></body></html>"""
        elif g_sub == "اللغة الإنجليزية":
            chosen_game, game_html = "شجرة التفاح الإنجليزية", """<!DOCTYPE html><html><body style="background:#87ceeb; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:white; font-size:3rem;">🍎 Apple Tree Game</h1><div style="font-size:6rem;">🌳 🍎</div></body></html>"""
        elif g_sub == "الدراسات الاجتماعية":
            if "الإعدادية" in g_stage:
                chosen_game, game_html = "آلة الزمن الفرعونية", """<!DOCTYPE html><html dir="rtl"><body style="background:#020617; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#d4af37; font-size:3rem;">⏳ آلة الزمن الفرعونية</h1><div style="color:white; font-size:2rem; border:2px dashed gold; padding:20px; margin:auto; width:50%;">خوفو -> أحمس -> رمسيس</div></body></html>"""
            else:
                chosen_game, game_html = "أبطال خريطة مصر", """<!DOCTYPE html><html dir="rtl"><body style="background:#000000; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#ffff00; font-size:3rem;">🗺️ أبطال خريطة مصر</h1><svg viewBox="0 0 100 100" style="max-width:300px;"><rect width="100" height="100" fill="#ff0"/><path d="M 50 20 L 50 100" stroke="#00f" stroke-width="5"/></svg></body></html>"""
        elif g_sub == "العلوم":
            chosen_game, game_html = "معمل أينشتاين الملون", """<!DOCTYPE html><html dir="rtl"><body style="background:#1e293b; text-align:center; font-family:sans-serif; padding-top:50px;"><h1 style="color:#38bdf8; font-size:3rem;">🔬 معمل أينشتاين الملون</h1><div style="font-size:6rem;">🧫 🧬</div></body></html>"""

        st.success(f"المنصة ترشح لك وتفعل لعبة: **{chosen_game}**")
        components.html(game_html, height=500)

# ------------------------------------------
# 4. الأهداف
# ------------------------------------------
with tabs[3]:
    st.markdown("### 🎯 هدفنا")
    st.markdown("""
    تأسست **منصة بصمة** لتكون منارة تعليمية تضمن حق التعليم المتكافئ للجميع، وتواكب التطورات التكنولوجية الحديثة لخدمة أبنائنا من ذوي القدرات الخاصة. 
    
    **أهداف المنصة التفصيلية:**
    1. **تكافؤ الفرص:** توفير بيئة تعليمية دامجة تضمن حق الطلاب ذوي الإعاقة في التعلم جنباً إلى جنب مع أقرانهم.
    2. **تمكين المعلم:** استخدام تقنيات الذكاء الاصطناعي لتحليل المناهج وإنتاج خطط دروس مخصصة تلبي الاحتياجات الفردية لكل إعاقة في ثوانٍ معدودة.
    3. **التعلم التفاعلي:** تصميم وتطوير ألعاب إلكترونية تفاعلية تراعي الفروق الفردية (تباين عالي لضعاف البصر، بيئات هادئة للتوحد، إلخ).
    4. **دعم المنظومة:** توفير مكتبة استراتيجيات متكاملة لتكون مرجعاً تربوياً وقانونياً للمعلمين وأولياء الأمور.
    """)

# ------------------------------------------
# 5. قانون الدمج
# ------------------------------------------
with tabs[4]:
    st.markdown("### ⚖️ قانون الدمج التعليمي في مصر")
    st.markdown("""
    تولي الدولة المصرية اهتماماً بالغاً بدمج الأشخاص ذوي الإعاقة في التعليم العام، وذلك لضمان بيئة اجتماعية وتعليمية صحية.
    
    #### القرار الوزاري رقم 252 لسنة 2017
    يعتبر هذا القرار هو المظلة الأساسية التي تنظم وتكفل تطبيق الدمج التعليمي في المدارس المصرية. وينص على:
    * **حق القبول:** يحق لجميع الطلاب ذوي الإعاقات البسيطة (الإعاقة الذهنية البسيطة، بطء التعلم، التوحد، الشلل الدماغي، الإعاقات السمعية والبصرية والحركية) الالتحاق بمدارس التعليم العام.
    * **تكييف المناهج:** إلزام المدارس بإجراء التعديلات والمواءمات اللازمة في طرق التدريس والامتحانات لتناسب ظروف كل طالب.
    * **غرفة المصادر:** توفير غرف مصادر مجهزة بالمدارس الدامجة لمساندة الطلاب وتقديم جلسات فردية تدعم استيعابهم.
    * **التقييم العادل:** وضع نظم تقييم موضوعية تراعي نوع الإعاقة (مثل توفير مرافق للامتحانات، أو امتحانات موضوعية، أو تكبير الخط).
    """)

# ------------------------------------------
# 6. من نحن (عن المنصة)
# ------------------------------------------
with tabs[5]:
    st.markdown("### 👥 من نحن")
    st.markdown("""
    **"بصمة"** هي منصة تعليمية رقمية رائدة، وُلدت من الإيمان العميق بأن التعليم حق أصيل لكل طفل، وأن تنوع القدرات داخل الفصول الدراسية هو إثراء للمجتمع بأكمله.
    
    نعمل على تسخير أحدث تقنيات الذكاء الاصطناعي لدعم المعلمين في إعداد دروس تفاعلية، وتحويل المناهج المعقدة إلى مواد مبسطة تناسب أبنائنا من فئات الدمج المختلفة (كالتوحد، الإعاقات الذهنية، البصرية، السمعية، الحركية، وصعوبات التعلم).
    """)
    
    st.markdown("---")
    st.markdown("<h4 style='color:#1e3a8a; text-align:center;'>تم التطوير والبرمجة بواسطة: <br><span style='color:#f59e0b; font-size: 1.5rem;'>ولاء مقدام</span></h4>", unsafe_allow_html=True)
    
    st.markdown("#### 🎬 فيديو تعريفي بالمنصة:")
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <iframe src="https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview" width="800" height="480" allow="autoplay" style="border-radius: 15px; border: 4px solid #1e3a8a;"></iframe>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# 7. المكتبة والمقالات
# ------------------------------------------
with tabs[6]:
    st.markdown("### 📚 مكتبة الاستراتيجيات والمقالات")
    st.markdown("""
    نقدم للمعلمين مجموعة من أفضل استراتيجيات التدريس المتخصصة لفئات الدمج:
    
    #### 🧩 استراتيجيات تدريس طلاب التوحد:
    * **الروتين البصري:** استخدام الجداول المصورة لتوضيح سير الحصة وتقليل القلق.
    * **التعليمات المباشرة:** إعطاء أوامر قصيرة وواضحة خالية من التشبيهات اللغوية المعقدة.
    * **البيئة الهادئة (Low Sensory):** تقليل المشتتات البصرية والصوتية داخل الغرفة الصفية.
    
    #### 💡 استراتيجيات تدريس صعوبات التعلم:
    * **النهج متعدد الحواس (VAKT):** دمج الحواس (البصر، السمع، اللمس، الحركة) في توصيل المعلومة.
    * **تجزئة المهام (Chunking):** تقسيم الواجبات والمعلومات الكبيرة إلى خطوات صغيرة قابلة للإنجاز.
    
    #### 🧠 استراتيجيات تدريس الإعاقة الذهنية البسيطة:
    * **التعلم بالنمذجة والمحاكاة:** ربط المفاهيم المجردة بأشياء ملموسة من البيئة المحيطة بالطالب.
    * **التكرار المتباعد:** مراجعة المعلومات بشكل مستمر لتثبيتها في الذاكرة قصيرة المدى.
    
    #### 👁️ استراتيجيات تدريس الإعاقة البصرية والسمعية:
    * الاعتماد على الوسائل السمعية والمجسمات البارزة (للمكفوفين وضعاف البصر).
    * الاعتماد على لغة الإشارة والتواصل البصري ولغة الشفاه (لضعاف السمع).
    """)
