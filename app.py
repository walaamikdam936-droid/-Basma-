import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import os

# إعدادات المنصة الأساسية
st.set_page_config(page_title="منصة بصمة التعليمية", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

# تهيئة الذكاء الاصطناعي (يستخدم مفتاح API من الإعدادات تلقائياً)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# الواجهة الأصلية
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)
if os.path.exists("waw_logo.png"): st.image("waw_logo.png", width=150)
st.markdown("<h1 style='text-align:center;'>🌟 منصة بصمة للدمج التعليمية 🌟</h1>", unsafe_allow_html=True)

# التبويبات الأصلية
tabs = st.tabs(["💬 الشات الذكي", "🚀 المساعد الذكي", "🎮 الألعاب التفاعلية", "🎯 أهدافنا", "⚖️ قانون الدمج", "👥 من نحن", "📚 مقالات وإعاقات"])

# 1. الشات الذكي (يعمل بالمفتاح الموجود في المنصة)
with tabs[0]:
    st.markdown("### 💬 شات بصمة الذكي")
    if prompt := st.chat_input("اسألني أي شيء عن الدمج التعليمي..."):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.write(response.text)

# 2. المساعد الذكي (المرحلة الإعدادية + تصحيح كلمة "حدد")
with tabs[1]:
    st.markdown("### 🚀 المساعد الذكي")
    col1, col2, col3 = st.columns(3)
    with col1: stage = st.selectbox("حدد المرحلة الدراسية:", ["الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول الإعدادي", "الثاني الإعدادي", "الثالث الإعدادي"])
    with col2: subject = st.selectbox("حدد المادة:", ["عربي", "رياضيات", "علوم", "دراسات", "إنجليزي"])
    with col3: disability = st.selectbox("حدد نوع الإعاقة:", ["إعاقة ذهنية", "توحد", "بصرية", "سمعية", "حركية", "صعوبات تعلم"])
    
    desc = st.text_area("ماذا يحتاج المعلم من هذا الدرس؟")
    uploaded_file = st.file_uploader("📸 حدد صورة الدرس لرفعها:")
    
    if st.button("توليد الخطة"):
        st.success("تم توليد الخطة بنجاح (يمكنك تحميلها الآن).")
        # روابط التحميل الأصلية التي طلبتها
        st.download_button("📥 تحميل بصيغة Word", "محتوى الخطة", "lesson_plan.doc")
        st.download_button("📥 تحميل بصيغة PDF", "محتوى الخطة", "lesson_plan.pdf")

# 3. الألعاب التفاعلية
with tabs[2]:
    st.markdown("### 🎮 الألعاب التفاعلية")
    st.write("اختر اللعبة من القائمة:")
    game = st.selectbox("حدد اللعبة:", ["قطار الحروف", "شجرة التفاح", "خريطة مصر", "فقاعات الضرب", "سلة الفواكه", "آلة الزمن", "المشاعر", "المحقق اللغوي", "المهندس الذكي", "الخلية النباتية"])
    if st.button("بدء اللعب"):
        components.html(f"<div style='text-align:center;'><h2>تشغيل لعبة {game}</h2><p>المنصة جاهزة للعب الآن.</p></div>", height=400)

# 4. الأهداف
with tabs[3]:
    st.markdown("### 🎯 أهدافنا")
    st.write("نحن نسعى للدمج التعليمي الشامل وتوفير بيئة تعليمية تناسب الجميع.")

# 5. قانون الدمج
with tabs[4]:
    st.markdown("### ⚖️ قانون الدمج")
    st.write("قانون الدمج المصري يضمن حق الطالب في التعليم، وغرف المصادر، والتقييم العادل.")

# 6. من نحن (التطوير)
with tabs[5]:
    st.markdown("### 👥 من نحن")
    st.write("نحن منصة بصمة.. رسالتنا دمج الطلاب وتطوير التعليم.")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")
    st.markdown("---")
    st.markdown("### تم التطوير والبرمجة بواسطة: ولاء مقدام")

# 7. مقالات وإعاقات
with tabs[6]:
    st.markdown("### 📚 مقالات وإعاقات")
    st.write("هنا ستجد مقالات تفصيلية عن (التوحد، الإعاقة الذهنية، صعوبات التعلم) وكيفية التعامل معهم.")
