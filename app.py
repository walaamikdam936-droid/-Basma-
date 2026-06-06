import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
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
    st.session_state.audio_bytes = None
    st.session_state.formatted_doc = None
    st.session_state.audio_lang = 'ar'

# 3. الهيدر الرئيسي
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

# دالة التنسيق
def create_formatted_doc(text, direction, align):
    html_text = text.replace('\n', '<br>')
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_text)
    doc_content = f"""
    <html dir='{direction}'><head><meta charset='utf-8'></head>
    <body style='font-family: Arial; text-align: {align};'>
        <h2 style='color: #1e3a8a; text-align: center;'>🌟 الدليل التربوي المخصص - منصة بصمة 🌟</h2>
        <hr><div>{html_text}</div>
    </body></html>
    """
    return doc_content.encode('utf-8')

# 4. تقسيم المنصة
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 المساعد الذكي", "🎯 أهداف المنصة وفلسفتها", "⚖️ قانون الدمج", "👥 عن المنصة", "📚 مكتبة الإعاقات والمقالات"])

# --- تبويب المساعد الذكي ---
with tab1:
    st.markdown("### 📝 حدد خصائص الدرس وفئة الدمج:")
    col1, col2, col3 = st.columns(3)
    with col1:
        stage = st.selectbox("📚 المرحلة الدراسية:", [
            "الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي", 
            "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي", 
            "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي"
        ])
    with col2:
        subject = st.selectbox("📖 المادة الدراسية:", ["لغة عربية", "رياضيات", "علوم / اكتشف", "دراسات اجتماعية", "لغة إنجليزية", "تربية دينية"])
    with col3:
        disability = st.selectbox("🧩 نوع الإعاقة:", ["إعاقة ذهنية بسيطة", "بطء تعلم", "طيف التوحد (دمج خفيف)", "إعاقة بصرية (ضعف بصر)", "إعاقة بصرية (كف بصر)", "إعاقة سمعية (ضعف سمع)", "صعوبات تعلم أكاديمية", "إعاقة حركية (شلل دماغي بسيط)"])

    additional_notes = st.text_area("✍️ ملاحظات المعلم الإضافية (اختياري):")
    uploaded_file = st.file_uploader("ارفعي صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file and st.button("✨ ابدأ التحليل والاستخراج"):
        st.session_state.analysis_done = True
        st.success("🎉 تم إعداد الدليل التربوي بنجاح!")

    if st.session_state.analysis_done:
        st.write("تم التحليل! (سيظهر المحتوى هنا)")
        st.download_button("📥 تحميل Word", "بيانات الخطة", "plan.doc")

# --- تبويب الأهداف، القانون، ومن نحن، والمقالات ---
with tab2: st.write("أهداف المنصة...")
with tab3: st.write("قانون الدمج المصري...")
with tab4:
    st.write("منصة بصمة تهدف لتمكين المعلمين.")
    st.markdown("### تم التطوير والبرمجة بواسطة: ولاء مقدام")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")

with tab5:
    st.markdown("### 📚 مكتبة الإعاقات")
    with st.expander("إعاقة حركية"):
        st.info("الوسائل المقترحة: 1. حوامل كتب. 2. أقلام سميكة. 3. كيبورد معدل. 4. طاولات قابلة للتحكم.")
