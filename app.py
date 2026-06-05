import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import base64
import os

# ==========================================
# 1. إعدادات المنصة الأساسية
# ==========================================
st.set_page_config(page_title="منصة بصمة التعليمية", page_icon="🌟", layout="wide")

# إخفاء قوائم ستريمليت الافتراضية
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'result_text' not in st.session_state:
    st.session_state.result_text = "سيتم عرض خطة الدرس هنا بعد التحليل."

# ==========================================
# 2. صناديق أكواد الألعاب (ضعي أكواد HTML هنا لتعمل الألعاب)
# ==========================================
# أستاذة ولاء: امسحي كلمة "ضعي كود اللعبة هنا" والصقي كود الـ HTML الطويل الخاص بكل لعبة بين علامات التنصيص الثلاثية """ """

GAME_1_TRAIN = """
<!-- ضعي كود قطار الحروف السعيد هنا بالكامل -->
"""

GAME_2_APPLE = """
<!-- ضعي كود شجرة التفاح الإنجليزية هنا بالكامل -->
"""

GAME_3_MAP = """
<!-- ضعي كود أبطال خريطة مصر هنا بالكامل -->
"""

GAME_4_MATH = """
<!-- ضعي كود فقاعات جدول الضرب هنا بالكامل -->
"""

GAME_5_FRUITS = """
<!-- ضعي كود سلة الفواكه والألوان هنا بالكامل -->
"""

GAME_6_TIME = """
<!-- ضعي كود آلة الزمن الفرعونية هنا بالكامل -->
"""

GAME_7_EMOTIONS = """
<!-- ضعي كود مسرح المشاعر والأخلاق هنا بالكامل -->
"""

GAME_8_GRAMMAR = """
<!-- ضعي كود المحقق اللغوي هنا بالكامل -->
"""

GAME_9_ENGINEER = """
<!-- ضعي كود المهندس الذكي هنا بالكامل -->
"""

GAME_10_CELLS = """
<!-- ضعي كود معمل أينشتاين الملون هنا بالكامل -->
"""

# ==========================================
# 3. وظائف الهوية البصرية
# ==========================================
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return ""
    return ""

# ==========================================
# 4. الهيدر والشعارات
# ==========================================
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_column_width=True)

if os.path.exists("waw_logo.png"):
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("waw_logo.png", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white;">
        <h1 style="font-family: 'Cairo'; font-weight:900;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3>"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع"</h3>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. الأبواب الرئيسية
# ==========================================
tab_chat, tab_assist, tab_games, tab_goals, tab_law, tab_about, tab_lib = st.tabs([
    "💬 شات بصمة الذكي", 
    "🚀 المساعد الذكي", 
    "🎮 الألعاب التفاعلية",
    "🎯 الأهداف", 
    "⚖️ قانون الدمج", 
    "👥 من نحن", 
    "📚 المكتبة"
])

# ------------------------------------------
# شات بصمة الذكي
# ------------------------------------------
with tab_chat:
    st.markdown("### 🤖 شات بصمة الذكي (خبير التربية الخاصة)")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"أنت خبير تربية خاصة في منصة بصمة. أجب على: {prompt}")
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except:
                st.error("يرجى التأكد من إعدادات API Key.")

# ------------------------------------------
# المساعد الذكي
# ------------------------------------------
with tab_assist:
    st.markdown("### 📝 خصائص الدرس وفئة الدمج:")
    c1, c2, c3 = st.columns(3)
    with c1: 
        stage = st.selectbox("حدد المرحلة الدراسية:", [
            "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي",
            "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي",
            "الأول الإعدادي", "الثاني الإعدادي", "الثالث الإعدادي"
        ])
    with c2: 
        subject = st.selectbox("حدد المادة:", ["اللغة العربية", "الرياضيات", "العلوم", "الدراسات الاجتماعية", "اللغة الإنجليزية", "التربية الدينية"])
    with c3: 
        disability = st.selectbox("حدد نوع الإعاقة:", ["إعاقة ذهنية", "توحد", "بصرية", "سمعية", "حركية", "صعوبات تعلم"])

    st.markdown("---")
    teacher_desc = st.text_area("✍️ ماذا يحتاج المعلم من هذا الدرس؟ (اكتب وصفك هنا):", height=100)
    uploaded_file = st.file_uploader("📸 حدد صورة الدرس لرفعها:", type=["jpg", "png"])
    
    if st.button("✨ ابدأ التحليل"):
        st.session_state.analysis_done = True
        st.session_state.result_text = f"خطة درس مقترحة لمادة {subject} - {stage} لتناسب الطلاب ذوي ({disability}).\n\n(سيقوم الذكاء الاصطناعي بتوليد الخطة هنا بناءً على الوصف والصورة)."
        st.success("تم استلام البيانات بنجاح! يتم الآن التحليل.")
    
    if st.session_state.analysis_done:
        st.markdown("### نتيجة التحليل:")
        st.write(st.session_state.result_text)
        
        logo_base64 = get_base64_image("waw_logo.png")
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="150" style="margin-bottom: 10px;" />' if logo_base64 else ''
        
        branded_html_content = f"""
        <html dir="rtl" lang="ar">
        <head><meta charset="utf-8"></head>
        <body style="font-family: Arial, sans-serif; padding: 40px; text-align: right;">
            <div style="text-align: center; border-bottom: 4px solid #1e3a8a; padding-bottom: 20px; margin-bottom: 30px;">
                {logo_html}
                <h1 style="color: #1e3a8a;">منصة بصمة للدمج التعليمية</h1>
                <h3>تقرير خطة الدرس المخصصة - {subject} | {stage} | {disability}</h3>
            </div>
            <div style="font-size: 16px;">
                {st.session_state.result_text.replace(chr(10), '<br>')}
            </div>
        </body>
        </html>
        """
        st.download_button("📥 تحميل خطة الدرس (مرفقة بشعار المنصة)", data=branded_html_content.encode('utf-8'), file_name="Basma_Lesson_Plan.doc", mime="application/msword")

# ------------------------------------------
# الألعاب التفاعلية (المُرشح الذكي)
# ------------------------------------------
with tab_games:
    st.markdown("### 🎮 نظام الألعاب التفاعلية الذكي")
    st.write("حدد بيانات الطالب ليقوم النظام باختيار اللعبة الأنسب له تلقائياً:")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1: g_stage = st.selectbox("حدد المرحلة:", ["الابتدائي (الصفوف الأولى)", "الابتدائي (الصفوف العليا)", "المرحلة الإعدادية"])
    with col_g2: g_dis = st.selectbox("حدد الإعاقة:", ["إعاقة ذهنية", "توحد", "بصرية", "سمعية", "حركية", "صعوبات تعلم"])
    with col_g3: g_sub = st.selectbox("حدد المادة المستهدفة:", ["اللغة العربية", "الرياضيات", "اللغة الإنجليزية", "الدراسات", "العلوم", "مهارات سلوكية وإدراكية"])

    if st.button("🎲 استخراج اللعبة المناسبة"):
        chosen_game = ""
        game_html_to_render = ""

        # الخوارزمية الذكية للاختيار
        if g_sub == "مهارات سلوكية وإدراكية":
            chosen_game = "مسرح المشاعر والأخلاق" if g_dis in ["توحد", "صعوبات تعلم"] else "سلة الفواكه والألوان"
            game_html_to_render = GAME_7_EMOTIONS if chosen_game == "مسرح المشاعر والأخلاق" else GAME_5_FRUITS
            
        elif g_sub == "اللغة العربية":
            chosen_game = "المحقق اللغوي" if "الإعدادية" in g_stage else "قطار الحروف السعيد"
            game_html_to_render = GAME_8_GRAMMAR if chosen_game == "المحقق اللغوي" else GAME_1_TRAIN
            
        elif g_sub == "الرياضيات":
            chosen_game = "المهندس الذكي" if "الإعدادية" in g_stage or "العليا" in g_stage else "فقاعات جدول الضرب"
            game_html_to_render = GAME_9_ENGINEER if chosen_game == "المهندس الذكي" else GAME_4_MATH
            
        elif g_sub == "اللغة الإنجليزية":
            chosen_game = "شجرة التفاح الإنجليزية"
            game_html_to_render = GAME_2_APPLE
            
        elif g_sub == "الدراسات":
            chosen_game = "آلة الزمن الفرعونية" if "الإعدادية" in g_stage else "أبطال خريطة مصر"
            game_html_to_render = GAME_6_TIME if chosen_game == "آلة الزمن الفرعونية" else GAME_3_MAP
            
        elif g_sub == "العلوم":
            chosen_game = "معمل أينشتاين الملون"
            game_html_to_render = GAME_10_CELLS

        st.success(f"المنصة ترشح لك لعبة: **{chosen_game}**")
        
        # عرض اللعبة
        if game_html_to_render.strip() == "" or "<!-- ضعي كود" in game_html_to_render:
            st.warning("⚠️ اللعبة جاهزة للاستدعاء! يرجى لصق كود الـ HTML الخاص بهذه اللعبة في المتغير المخصص لها أعلى الكود لكي تظهر هنا.")
        else:
            components.html(game_html_to_render, height=750)

# ------------------------------------------
# التبويبات الأصلية (نفس محتواك)
# ------------------------------------------
with tab_goals:
    st.markdown("<!-- محتوى تبويب الأهداف الأصلي الخاص بك -->")
    st.write("ضع أهداف المنصة هنا كما كانت في كودك الأصلي.")

with tab_law:
    st.markdown("<!-- محتوى تبويب قانون الدمج الأصلي الخاص بك -->")
    st.write("ضع محتوى قوانين الدمج هنا كما كان في كودك الأصلي.")

with tab_about:
    st.markdown("<!-- محتوى تبويب من نحن الأصلي الخاص بك -->")
    st.write("ضع محتوى من نحن هنا كما كان في كودك الأصلي.")
    
    st.markdown("---")
    st.markdown("<h4 style='color:#1e3a8a; text-align:center;'>تم التطوير والبرمجة بواسطة: <br><span style='color:#f59e0b; font-size: 1.5rem;'>ولاء مقدام</span></h4>", unsafe_allow_html=True)
    
    st.markdown("#### 🎬 فيديو تعريفي بالمنصة:")
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <iframe src="https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview" width="800" height="480" allow="autoplay" style="border-radius: 15px; border: 4px solid #1e3a8a;"></iframe>
        </div>
    """, unsafe_allow_html=True)

with tab_lib:
    st.markdown("<!-- محتوى تبويب المكتبة والمقالات الأصلي الخاص بك -->")
    st.write("ضع محتوى المقالات والمكتبة هنا كما كان في كودك الأصلي.")
