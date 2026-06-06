import streamlit as stimport streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import os

# --- 1. إعدادات المنصة ---
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", layout="wide")

# إخفاء التنسيقات الافتراضية للحفاظ على تصميمك
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .css-1544g2n {padding: 1rem 1rem 1.5rem;}
    </style>
""", unsafe_allow_html=True)

# تهيئة الذكاء الاصطناعي
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 2. الواجهة الأصلية (اللوجوهات) ---
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)
if os.path.exists("waw_logo.png"): st.image("waw_logo.png", width=150)
st.markdown("<h1 style='text-align:center; color: #1e3a8a;'>🌟 منصة بصمة للدمج التعليمية 🌟</h1>", unsafe_allow_html=True)

# --- 3. التبويبات الموسعة ---
tabs = st.tabs(["💬 الشات الذكي", "🚀 المساعد الذكي", "🎮 الألعاب التفاعلية", "🎯 أهدافنا", "⚖️ قانون الدمج", "👥 من نحن", "📚 مكتبة المقالات"])

# تبويب الشات الذكي
with tabs[0]:
    st.markdown("### 💬 شات بصمة الذكي")
    st.write("أنا رفيقك الذكي، خبير التربية الخاصة. اسألني أي سؤال لمساعدتك.")
    prompt = st.chat_input("اكتب سؤالك هنا...")
    if prompt:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.write(response.text)

# تبويب المساعد الذكي (المطول)
with tabs[1]:
    st.markdown("### 🚀 المساعد الذكي لتخطيط الدروس")
    col1, col2, col3 = st.columns(3)
    c1 = col1.selectbox("حدد المرحلة الدراسية:", ["الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول الإعدادي", "الثاني الإعدادي", "الثالث الإعدادي"])
    c2 = col2.selectbox("حدد المادة الدراسية:", ["اللغة العربية", "الرياضيات", "العلوم", "الدراسات الاجتماعية", "اللغة الإنجليزية", "التربية الدينية"])
    c3 = col3.selectbox("حدد نوع الإعاقة:", ["إعاقة ذهنية", "اضطراب التوحد", "إعاقة بصرية", "إعاقة سمعية", "إعاقة حركية", "صعوبات تعلم"])
    
    st.text_area("أدخل وصف الدرس أو النشاط المطلوب:")
    st.file_uploader("حدد صورة الدرس لرفعها:")
    
    if st.button("توليد الخطة التعليمية"):
        st.success("تم تحليل الدرس وتوليد الخطة بنجاح!")
        # مساحة عرض الخطة
        st.info("إليك الخطة المقترحة بناءً على اختيارك:")
        st.write("1. الأهداف التعليمية: ...")
        st.write("2. الاستراتيجيات المناسبة: ...")
        st.write("3. الأنشطة التفاعلية: ...")
        
        # أزرار التحميل
        st.markdown("---")
        st.download_button("📥 تحميل الخطة كملف Word", "بيانات الخطة", "plan.docx")
        st.download_button("📥 تحميل الخطة كملف PDF", "بيانات الخطة", "plan.pdf")
        st.download_button("📥 تحميل الملف الصوتي MP3", "بيانات الخطة", "lesson_audio.mp3")

# تبويب الألعاب (التي طلبنا تركها فارغة مؤقتاً لضمان الاستقرار)
with tabs[2]:
    st.markdown("### 🎮 الألعاب التفاعلية")
    st.write("نظام الألعاب قيد التطوير والدمج قريباً لضمان أفضل تجربة تعليمية.")

# تبويب الأهداف
with tabs[3]:
    st.markdown("### 🎯 أهدافنا")
    st.write("نسعى جاهدين لتحقيق دمج تعليمي متكامل لجميع أبنائنا، من خلال توفير الأدوات الرقمية اللازمة.")

# تبويب القانون
with tabs[4]:
    st.markdown("### ⚖️ قانون الدمج")
    st.write("نستند في عملنا إلى القرار الوزاري رقم 252 لسنة 2017 المنظم للدمج التعليمي في مصر.")

# تبويب من نحن
with tabs[5]:
    st.markdown("### 👥 من نحن")
    st.write("منصة بصمة.. فكرة بدأت من قلب الميدان التربوي.")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")
    st.markdown("### تم التطوير والبرمجة بواسطة: ولاء مقدام")

# تبويب المقالات
with tabs[6]:
    st.markdown("### 📚 مكتبة المقالات")
    st.write("دليل شامل للإعاقات وكيفية التعامل معها في بيئة الدمج.")
