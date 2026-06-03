import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة والأيقونات
st.set_page_config(page_title="منصة بسمة التعليمية", page_icon="🏫", layout="wide")

# إخفاء العلامات المائية لتبدو كمنصة مستقلة واحترافية
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. تفعيل الربط السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. الواجهة العلوية (الهيدر) بتصميم احترافي
st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 25px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 5px;">🏫 منصة بسمة التعليمية للذكاء الاصطناعي</h1>
        <h3 style="color: #bfdbfe; margin-top: 0;">مدرسة أحمد ضيف الله للتعليم الأساسي</h3>
    </div>
""", unsafe_allow_html=True)

# 4. تقسيم الموقع إلى صفحات (تبويبات)
tab1, tab2, tab3 = st.tabs(["🚀 لوحة التحليل الأساسية", "🎯 أهداف المنصة", "👥 من نحن"])

# --- الصفحة الأولى: التحليل ---
with tab1:
    st.markdown("### 📸 أداة استخراج الخطط النموذجية")
    st.info("قومي برفع لقطة شاشة للدرس، وسيقوم الذكاء الاصطناعي باستخراج الخطة كاملة.")
    uploaded_file = st.file_uploader("ارفعي صورة الدرس هنا (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="تم رفع الصورة بنجاح", width=400)
        
        if st.button("✨ ابدأ التحليل واستخراج الخطة النموذجية", use_container_width=True):
            with st.spinner("جاري قراءة المحتوى وإعداد الخطة التربوية..."):
                try:
                    # الكود المحسن لتفادي أخطاء 404
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = """
                    أنت خبير تربوي وموجه متميز. قم بتحليل الدرس في الصورة واستخرج خطة درس نموذجية تحتوي على:
                    1. عنوان الدرس والمستهدفين.
                    2. الأهداف السلوكية.
                    3. التمهيد وإثارة الدافعية.
                    4. استراتيجيات التدريس.
                    5. الأنشطة التعليمية.
                    6. التقويم.
                    """
                    response = model.generate_content([prompt, image])
                    st.success("🎉 تم استخراج الخطة بنجاح!")
                    st.markdown("""<hr style="border:1px solid #3b82f6;">""", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown("""<hr style="border:1px solid #3b82f6;">""", unsafe_allow_html=True)
                except Exception as e:
                    st.error("عذراً، واجه النظام صعوبة. تم إرسال تقرير بالخطأ لمعالجته.")
                    st.info(f"تفاصيل الخطأ: {str(e)}")

# --- الصفحة الثانية: الأهداف ---
with tab2:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border-right: 5px solid #3b82f6;">
        <h3 style="color: #1e3a8a;">🎯 الرؤية والأهداف</h3>
        <ul style="font-size: 18px; line-height: 1.8;">
            <li><b>مواكبة التطور:</b> دمج أحدث أدوات الذكاء الاصطناعي في البيئة المدرسية.</li>
            <li><b>التنمية المهنية:</b> دعم السادة المعلمين وتسهيل عمليات إعداد الدروس والأنشطة.</li>
            <li><b>توفير الجهد والوقت:</b> استخراج خطط نموذجية دقيقة في ثوانٍ معدودة.</li>
            <li><b>الابتكار التعليمي:</b> خلق مناخ تفاعلي يعود بالنفع المباشر على أبنائنا الطلاب.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة الثالثة: من نحن ---
with tab3:
    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 10px; border-right: 5px solid #22c55e;">
        <h3 style="color: #166534;">👥 عن المنصة وإدارة الوحدة</h3>
        <p style="font-size: 16px;">تم تصميم وتطوير هذه المنصة الرقمية كإحدى المبادرات الرائدة لـ <b>وحدة التواصل ودعم المعلمين</b>، إيماناً بأهمية التكنولوجيا في خدمة المعلم.</p>
        <hr>
        <ul style="font-size: 16px; line-height: 1.8; list-style-type: none;">
            <li>👩‍💻 <b>تصميم وتطوير المنصة:</b> أ. ولاء مقدام (منسق الوحدة)</li>
            <li>👨‍🏫 <b>إشراف مباشر:</b> أ. أحمد محمد فرغلي (مدير الوحدة)</li>
            <li>🏫 <b>رعاية ودعم:</b> أ. أشرف مرسي (مدير المدرسة)</li>
            <li>🏢 <b>تحت رعاية:</b> د. أيمن أبو سداح (مدير إدارة سوهاج التعليمية)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
