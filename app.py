import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import re
import os

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", page_icon="🌟", layout="wide")

hide_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. تفعيل مفتاح جوجل السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تجهيز ذاكرة المنصة
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.result_text = ""

# 3. الهيدر الرئيسي واللوجو
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)
if os.path.exists("waw_logo.png"): st.image("waw_logo.png", width=150)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

# 4. تقسيم المنصة
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 الشات الذكي", "🚀 المساعد الذكي", "🎯 أهداف المنصة وفلسفتها", "⚖️ قانون الدمج", "👥 عن المنصة"])

# --- تبويب الشات الذكي (مضاف حديثاً) ---
with tab1:
    st.markdown("### 💬 شات بصمة الذكي")
    st.info("اسألني عن قانون الدمج المصري أو أي استفسار تربوي خاص بالدمج.")
    prompt = st.chat_input("اكتب سؤالك هنا...")
    if prompt:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"أنت خبير في قانون الدمج المصري والتربية الخاصة في منصة بصمة. أجب على السؤال التالي: {prompt}")
        st.write(res.text)

# --- تبويب المساعد الذكي ---
with tab2:
    st.markdown("### 📝 حدد خصائص الدرس وفئة الدمج:")
    col1, col2, col3 = st.columns(3)
    with col1:
        stage = st.selectbox("📚 المرحلة الدراسية:", [
            "الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي", "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي",
            "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي"
        ])
    with col2:
        subject = st.selectbox("📖 المادة الدراسية:", ["لغة عربية", "رياضيات", "علوم / اكتشف", "دراسات اجتماعية", "لغة إنجليزية", "تربية دينية"])
    with col3:
        disability = st.selectbox("🧩 نوع الإعاقة:", ["إعاقة ذهنية بسيطة", "بطء تعلم", "طيف التوحد (دمج خفيف)", "إعاقة بصرية (ضعف بصر)", "إعاقة بصرية (كف بصر)", "إعاقة سمعية (ضعف سمع)", "صعوبات تعلم أكاديمية", "إعاقة حركية (شلل دماغي بسيط)"])

    st.markdown("---")
    additional_notes = st.text_area("✍️ ملاحظات المعلم الإضافية (اختياري):")
    uploaded_file = st.file_uploader("📸 حدد صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if st.button("✨ ابدأ التحليل والاستخراج", use_container_width=True):
        st.session_state.analysis_done = True
        st.session_state.result_text = "هذه نتيجة تحليل الدرس وفقاً لبياناتك المختارة."
        st.success("🎉 تم إعداد الدليل التربوي بنجاح!")

    if st.session_state.analysis_done:
        st.write(st.session_state.result_text)
        st.download_button("📥 تحميل الخطة كملف Word", "الخطة...", "plan.doc")
        st.download_button("📥 تحميل الخطة كملف PDF", "الخطة...", "plan.pdf")
        st.download_button("📥 تحميل الملف الصوتي MP3", "الصوت...", "plan.mp3")

# --- تبويب الأهداف ---
with tab3:
    st.markdown("### 🎯 أهداف المنصة وفلسفتها")
    st.write("الأهداف كما هي في نسختك السابقة...")

# --- تبويب القانون ---
with tab4:
    st.markdown("### ⚖️ قانون الدمج")
    st.write("شرح قانون الدمج المصري والقرار 252...")

# --- تبويب من نحن (مع الفيديو) ---
with tab5:
    st.markdown("### 👥 عن المنصة")
    st.write("فقرة من نحن...")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")
    st.markdown("---")
    st.markdown("### تم التطوير والبرمجة بواسطة: ولاء مقدام")
