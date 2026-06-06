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

if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.result_text = ""
    st.session_state.audio_bytes = None
    st.session_state.formatted_doc = None
    st.session_state.audio_lang = 'ar'

# 3. الهيدر الرئيسي (استخدام اللوجو المرفوع)
if os.path.exists("logo.jpg"): st.image("logo.jpg", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

def create_formatted_doc(text, direction, align):
    html_text = text.replace('\n', '<br>')
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_text)
    return f"<html dir='{direction}'><body style='font-family: Arial; text-align: {align};'>{html_text}</body></html>".encode('utf-8')

# 4. تقسيم المنصة
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 المساعد الذكي", "🎯 أهداف المنصة وفلسفتها", "⚖️ قانون الدمج", "👥 عن المنصة والفيديو الترحيبي", "📚 مكتبة الإعاقات والمقالات"])

with tab1:
    col1, col2, col3 = st.columns(3)
    # القائمة المنسدلة المحدثة بالصفوف المطلوبة
    stage = col1.selectbox("📚 المرحلة الدراسية:", ["الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي", "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي", "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي"])
    subject = col2.selectbox("📖 المادة الدراسية:", ["لغة عربية", "رياضيات", "علوم / اكتشف", "دراسات اجتماعية", "لغة إنجليزية", "تربية دينية"])
    disability = col3.selectbox("🧩 نوع الإعاقة:", ["إعاقة ذهنية بسيطة", "بطء تعلم", "طيف التوحد (دمج خفيف)", "إعاقة بصرية (ضعف بصر)", "إعاقة بصرية (كف بصر)", "إعاقة سمعية (ضعف سمع)", "صعوبات تعلم أكاديمية", "إعاقة حركية (شلل دماغي بسيط)"])
    
    additional_notes = st.text_area("✍️ ملاحظات المعلم الإضافية:", placeholder="اكتب هنا أي تفاصيل خاصة بمستوى الطالب...")
    uploaded_file = st.file_uploader("ارفعي صورة الدرس هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file and st.button("✨ ابدأ التحليل والاستخراج"):
        st.session_state.analysis_done = True
        st.success("🎉 تم إعداد الدليل التربوي بنجاح!")

with tab2: st.markdown("### 🎯 أهداف المنصة وفلسفتها\n(هنا نصوص الأهداف الأصلية)")
with tab3: st.markdown("### ⚖️ قانون الدمج\n(هنا نصوص القانون الأصلية)")

with tab4:
    st.markdown("### 👥 عن المنصة والفيديو الترحيبي")
    st.video("https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview")
    st.markdown("""
    <p style='font-size: 18px; text-align: justify;'>نحن مجموعة من المعلمين المهتمين بطلاب الدمج ونريد لهم حياة أفضل داخل مجتمعنا لذلك نقدم لهم ولمعلمى التربية الخاصة هذة المنصة.</p>
    <h3 style="color: #0f766e;">تم الابتكار والتطوير والبرمجة بواسطة ولاء مقدام (بدون أى مؤسسات حكومية أو إدارات)</h3>
    """, unsafe_allow_html=True)

with tab5:
    st.markdown("### 📚 مكتبة الإعاقات والمقالات")
    with st.expander("👁️ الإعاقة البصرية"): st.write("شرح الإعاقة البصرية.. المشاهير: طه حسين ولويس برايل.. استراتيجيات: الوصف الصوتي، اللمس.")
    with st.expander("👂 الإعاقة السمعية"): st.write("شرح الإعاقة السمعية.. المشاهير: أديسون وبيتهوفن.. استراتيجيات: لغة الإشارة، الصور.")
    with st.expander("🧠 الإعاقة الذهنية وبطء التعلم"): st.write("شرح الإعاقة الذهنية.. الاستراتيجيات: المجسمات، التكرار، تجزئة المهام.")
    with st.expander("🧩 طيف التوحد"): st.write("شرح التوحد.. المشاهير: تمبل جراندين وإيلون ماسك.. استراتيجيات: الجداول البصرية.")
    with st.expander("♿ الإعاقة الحركية"): st.write("شرح الإعاقة الحركية.. المشاهير: ستيفن هوكينج وروزفلت.. استراتيجيات: التكنولوجيا المساعدة.")
    st.markdown("### 🛠️ استراتيجيات التدريس: لعب الأدوار، التعلم التعاوني، الكرسي الساخن، المعلم الصغير، الألعاب التعليمية.")
