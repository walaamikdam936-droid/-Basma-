import streamlit as st
import google.generativeai as genai
import os

# 1. إعدادات المنصة الأساسية (التنسيق الأصلي)
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", page_icon="🌟", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

# 2. تهيئة الـ API (تأكدي من وجود المفتاح في الـ Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. الواجهة (اللوجو كما كان)
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)
if os.path.exists("waw_logo.png"): st.image("waw_logo.png", width=150)
st.markdown("<h1 style='text-align:center;'>🌟 منصة بصمة للدمج التعليمية 🌟</h1>", unsafe_allow_html=True)

# 4. التبويبات (كاملة وبنفس ترتيبك الأصلي)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💬 الشات الذكي", "🚀 المساعد الذكي", "🎯 أهدافنا", "⚖️ قانون الدمج", "👥 عن المنصة", "📚 مقالات وإعاقات"])

# 1. الشات الذكي
with tab1:
    st.markdown("### 💬 الشات الذكي")
    prompt = st.chat_input("اسألني عن الدمج التعليمي...")
    if prompt:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.write(response.text)

# 2. المساعد الذكي (التنسيق الأصلي مع تصحيح 'حدد')
with tab2:
    st.markdown("### 🚀 المساعد الذكي")
    c1, c2, c3 = st.columns(3)
    stage = c1.selectbox("حدد المرحلة الدراسية:", [
        "الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي", 
        "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي", 
        "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي"
    ])
    subject = c2.selectbox("حدد المادة:", ["عربي", "رياضيات", "علوم", "دراسات", "إنجليزي", "دين"])
    disability = c3.selectbox("حدد نوع الإعاقة:", ["إعاقة ذهنية", "توحد", "بصرية", "سمعية", "حركية", "صعوبات تعلم"])
    
    st.text_area("أدخل وصف النشاط:")
    st.file_uploader("حدد صورة الدرس:")
    
    if st.button("توليد الخطة"):
        st.success("تم توليد الخطة!")
        st.download_button("📥 تحميل Word", "بيانات الخطة", "plan.doc")
        st.download_button("📥 تحميل PDF", "بيانات الخطة", "plan.pdf")
        st.download_button("📥 تحميل صوت MP3", "بيانات الصوت", "plan.mp3")

# 3. الأهداف
with tab3:
    st.markdown("### 🎯 أهدافنا")
    st.write("أهداف المنصة هي دمج الطلاب ذوي القدرات الخاصة وتوفير بيئة تعليمية دامجة ومتميزة تضمن حق الجميع في التعلم.")

# 4. قانون الدمج
with tab4:
    st.markdown("### ⚖️ قانون الدمج")
    st.write("يستند عملنا إلى القرار الوزاري رقم 252 لسنة 2017 المنظم للدمج التعليمي في مصر، ونؤمن بحق كل طالب في التقييم العادل.")

# 5. عن المنصة
with tab5:
    st.markdown("### 👥 عن المنصة")
    st.write("منصة بصمة هي منصة تعليمية إبداعية لتمكين المعلمين ودعم طلاب الدمج.")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")
    st.markdown("### تم التطوير والبرمجة بواسطة: ولاء مقدام")

# 6. المقالات والإعاقات
with tab6:
    st.markdown("### 📚 مقالات وإعاقات")
    with st.expander("اضطراب التوحد"): st.write("يتميز التوحد بصعوبات التواصل الاجتماعي. للتعامل معه: استخدم الروتين البصري والبيئة الهادئة.")
    with st.expander("الإعاقة الذهنية"): st.write("تأخر في النمو الإدراكي. للتعامل معه: استخدم المجسمات الملموسة وتجزئة المهام إلى خطوات صغيرة.")
    with st.expander("صعوبات التعلم"): st.write("مشاكل في القراءة أو الحساب. للتعامل معه: استخدام التعلم متعدد الحواس وتوفير وقت إضافي.")
