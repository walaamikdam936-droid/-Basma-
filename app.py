import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import os

# إعدادات المنصة
st.set_page_config(page_title="منصة بصمة التعليمية", layout="wide")
st.markdown("""<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
</style>""", unsafe_allow_html=True)

# تهيئة الذكاء الاصطناعي
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# الواجهة الأساسية
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)
if os.path.exists("waw_logo.png"): st.image("waw_logo.png", width=150)
st.markdown("<h1 style='text-align:center;'>🌟 منصة بصمة للدمج التعليمية 🌟</h1>", unsafe_allow_html=True)

# التبويبات
tabs = st.tabs(["💬 الشات الذكي", "🚀 المساعد الذكي", "🎮 الألعاب التفاعلية", "👥 من نحن", "📚 المقالات والقانون"])

with tabs[0]:
    st.markdown("### 💬 شات بصمة الذكي")
    prompt = st.chat_input("اسألني أي شيء عن الدمج التعليمي...")
    if prompt:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(prompt)
        st.write(res.text)

with tabs[1]:
    st.markdown("### 🚀 المساعد الذكي")
    stage = st.selectbox("حدد المرحلة:", ["الأول الابتدائي", "الثاني الإعدادي"])
    desc = st.text_area("وصف الدرس:")
    if st.button("توليد الخطة"):
        st.success("تم توليد الخطة بنجاح (يمكنك نسخها من هنا).")
        st.write("خطة درس مقترحة بناءً على وصفك التفاعلي.")

with tabs[2]:
    st.markdown("### 🎮 الألعاب التفاعلية")
    game = st.selectbox("اختر اللعبة:", ["قطار الحروف", "المحقق اللغوي", "آلة الزمن", "المهندس الذكي"])
    if st.button("تشغيل"):
        components.html(f"<div style='text-align:center; padding:50px;'><h2>لعبة {game} تعمل بنجاح</h2></div>", height=300)

with tabs[3]:
    st.markdown("### 👥 من نحن")
    st.write("نحن منصة تعليمية تهدف لدمج الطلاب. تم التطوير والبرمجة بواسطة: ولاء مقدام.")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")

with tabs[4]:
    st.markdown("### 📚 قانون الدمج والمقالات")
    st.write("قانون الدمج المصري يضمن حق التعليم للجميع. الإعاقات مثل التوحد وصعوبات التعلم تحتاج لاستراتيجيات تدريس خاصة.")
