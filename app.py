import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# إعدادات الصفحة البرمجية المتقدمة
st.set_page_config(
    page_title="منصة بسمة التعليمية",
    page_icon="🚀",
    layout="centered"
)

# الواجهة الرسمية للتطبيق
st.markdown("""
    <div style="text-align: center; background-color: #f0f7ff; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <h1 style="color: #1e3a8a; font-family: 'Cairo', sans-serif;">🚀 منصة بسمة التعليمية</h1>
        <h3 style="color: #3b82f6;">لتحليل الدروس واستخراج الخطط النموذجية بالذكاء الاصطناعي</h3>
        <p style="color: #4b5563; font-weight: bold;">تم التطوير بواسطة: أ. ولاء مقدام</p>
        <p style="color: #6b7280; font-size: 14px;">منسق وحدة التواصل ودعم المعلمين - مدرسة أحمد ضيف الله للتعليم الأساسي</p>
    </div>
""", unsafe_allow_html=True)

# تفعيل الربط السري بمفتاح جوجل
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ خطأ برمجي: لم يتم العثور على المفتاح السري GOOGLE_API_KEY في إعدادات Secrets.")

# خانة رفع الملفات
uploaded_file = st.file_uploader("📸 ارفعي صورة الدرس أو لقطة الشاشة هنا:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # فتح الصورة ومعالجتها برمجياً
    image = Image.open(uploaded_file)
    st.image(image, caption="تم رفع صورة الدرس بنجاح", use_container_width=True)
    
    # زر التشغيل الحاسم
    if st.button("🚀 تحليل الدرس واستخراج الخطة النموذجية"):
        with st.spinner("جاري الآن قراءة الصورة والاتصال بخوادم جوجل لإنتاج الخطة..."):
            try:
                # استدعاء النموذج الأحدث والأسرع للصور من جوجل
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # الأوامر التربوية الموجهة للذكاء الاصطناعي
                prompt = (
                    "أنت خبير تربوي وموجه متميز لمعلمي مدرسة أحمد ضيف الله للتعليم الأساسي. "
                    "قم بتحليل صورة الدرس المرفقة بدقة، واستخرج خطة درس نموذجية متكاملة تحتوي على: "
                    "1. عنوان الدرس والمستهدفين. "
                    "2. الأهداف السلوكية (المعرفية والوجدانية والمهارية). "
                    "3. التمهيد وإثارة الدافعية. "
                    "4. استراتيجيات التدريس المقترحة والمناسبة للمحتوى المكتوب. "
                    "5. الأنشطة التعليمية ودور الطالب. "
                    "6. التقويم (الأسئلة القياسية لضمان الفهم)."
                )
                
                # إرسال الصورة والأمر لجوجل
                response = model.generate_content([prompt, image])
                
                # عرض النتيجة المذهلة للمعلمين
                st.success("✨ تم تحليل الدرس بنجاح واستخراج الخطة النموذجية!")
                st.markdown("""<hr style="border:1px solid #3b82f6;">""", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("""<hr style="border:1px solid #3b82f6;">""", unsafe_allow_html=True)
                
            except Exception as e:
                st.error("❌ عذراً، واجه النظام صعوبة في معالجة هذه الصورة حالياً.")
                st.info(f"تفاصيل الاستجابة الفنية: {str(e)}")
