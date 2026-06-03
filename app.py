
import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", page_icon="🌟", layout="wide")

# إخفاء العلامات المائية لمنصة Streamlit
hide_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. تفعيل مفتاح جوجل السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. الهيدر (الصورة والجملة التحفيزية)
st.image("https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=1200&auto=format&fit=crop", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 25px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h4 style="color: #bfdbfe; font-style: italic;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h4>
    </div>
""", unsafe_allow_html=True)

# 4. تقسيم المنصة إلى 4 صفحات (تبويبات)
tab1, tab2, tab3, tab4 = st.tabs(["🚀 المساعد الذكي للدمج", "🎯 أهداف المنصة", "⚖️ قانون الدمج المصري", "👥 من نحن"])

# ==========================================
# الصفحة الأولى: المساعد الذكي (نص وصوت)
# ==========================================
with tab1:
    st.markdown("### 📝 حددي خصائص الدرس وفئة الدمج:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        stage = st.selectbox("📚 المرحلة الدراسية:", [
            "الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي",
            "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي"
        ])
    with col2:
        subject = st.selectbox("📖 المادة الدراسية:", [
            "لغة عربية", "رياضيات", "علوم / اكتشف", "دراسات اجتماعية", "لغة إنجليزية", "تربية دينية"
        ])
    with col3:
        disability = st.selectbox("🧩 نوع الإعاقة (حسب القرار الوزاري):", [
            "إعاقة ذهنية بسيطة (بطء تعلم)", "طيف التوحد (دمج خفيف)", 
            "إعاقة بصرية (ضعف بصر)", "إعاقة بصرية (كف بصر)", 
            "إعاقة سمعية (ضعف سمع)", "صعوبات تعلم أكاديمية", "إعاقة حركية (شلل دماغي بسيط)"
        ])

    st.markdown("---")
    st.markdown("### 📸 استخراج الخطة والأنشطة (نصياً وصوتياً)")
    uploaded_file = st.file_uploader("ارفعي صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="تم رفع الصورة بنجاح", width=350)
        
        if st.button("✨ ابدأ التحليل والاستخراج", use_container_width=True):
            with st.spinner("الذكاء الاصطناعي يقوم بتحليل الدرس وإعداد الدليل التربوي والصوتي..."):
                try:
                    # إعداد نموذج جوجل
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    
                    # الأمر الموجه (Prompt)
                    prompt = f"""
                    أنت خبير تربوي مصري متخصص في التربية الخاصة والدمج التعليمي. 
                    استناداً إلى قانون الدمج المصري، قم بتحليل الدرس في الصورة المرفقة، وقدم دليلاً مبسطاً وموجهاً لمعلم يدرس طالب في ({stage}) لمادة ({subject}) يعاني من ({disability}).
                    قدم الإجابة باللغة العربية الفصحى الواضحة في نقاط مباشرة تحتوي على:
                    1. طريقة التدريس المثلى لهذا المحتوى بما يتناسب مع الإعاقة المذكورة.
                    2. ثلاثة (3) أنشطة تعليمية تطبيقية ومبتكرة تناسب قدرات الطالب.
                    3. طريقة التقييم المناسبة لقياس استيعاب الطالب للدرس.
                    """
                    
                    # استلام الرد من جوجل
                    response = model.generate_content([prompt, image])
                    result_text = response.text
                    
                    # عرض النص
                    st.success("🎉 تم إعداد الدليل التربوي بنجاح!")
                    st.markdown("""<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #cbd5e1;">""", unsafe_allow_html=True)
                    st.markdown(result_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # تحويل النص إلى صوت (Audio Generation)
                    with st.spinner("جاري تجهيز المقطع الصوتي..."):
                        tts = gTTS(text=result_text, lang='ar', slow=False)
                        audio_bytes = io.BytesIO()
                        tts.write_to_fp(audio_bytes)
                        audio_bytes.seek(0)
                        
                        st.markdown("### 🎧 استمع إلى الخطة التربوية والأنشطة:")
                        st.audio(audio_bytes, format='audio/mp3')
                        
                except Exception as e:
                    st.error("حدث خطأ أثناء المعالجة، يرجى المحاولة مرة أخرى.")
                    st.info(f"تفاصيل الخطأ: {str(e)}")

# ==========================================
# الصفحة الثانية: الأهداف
# ==========================================
with tab2:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border-right: 5px solid #3b82f6;">
        <h3 style="color: #1e3a8a;">🎯 الرؤية والأهداف</h3>
        <ul style="font-size: 18px; line-height: 1.8;">
            <li><b>مواكبة التطور:</b> دمج أحدث أدوات الذكاء الاصطناعي في فصول الدمج التعليمي.</li>
            <li><b>تمكين المعلم:</b> دعم السادة المعلمين وتسهيل عمليات إعداد الدروس والأنشطة المخصصة لذوي الهمم.</li>
            <li><b>الشمولية:</b> تغطية جميع المراحل الابتدائية وأنواع الإعاقات المقررة في قانون الدمج.</li>
            <li><b>الابتكار التعليمي:</b> خلق مناخ تفاعلي يعود بالنفع المباشر على أبنائنا الطلاب.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# الصفحة الثالثة: قانون الدمج
# ==========================================
with tab3:
    st.markdown("""
    <div style="background-color: #fffbeb; padding: 20px; border-radius: 10px; border-right: 5px solid #f59e0b;">
        <h3 style="color: #b45309;">⚖️ ملخص قانون الدمج المصري (القرار الوزاري 252 لسنة 2017)</h3>
        <ul style="font-size: 18px; line-height: 1.8;">
            <li><b>نظام الدمج:</b> يهدف إلى توفير فرص تعليمية متكافئة للطلاب ذوي الإعاقة البسيطة بمدارس التعليم العام.</li>
            <li><b>الفئات المسموح لها بالدمج:</b> الإعاقة البصرية (المكفوفين وضعاف البصر)، الإعاقة الحركية، الإعاقة السمعية (ضعاف السمع)، الإعاقة الذهنية البسيطة، بطء التعلم، التوحد، ومتلازمة داون.</li>
            <li><b>التقييم والامتحانات:</b> يتم تعديل نظم الامتحانات لتناسب كل إعاقة (مثل توفير مرافق قانوني، أو امتحانات موضوعية لبعض الفئات بنسب معينة).</li>
            <li><b>دور المعلم:</b> إعداد خطة تربوية فردية (IEP) تتناسب مع قدرات الطالب، واستخدام وسائل إيضاح حسية وملموسة.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# الصفحة الرابعة: عن المنصة
# ==========================================
with tab4:
    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 10px; border-right: 5px solid #22c55e; text-align: center;">
        <h3 style="color: #166534;">👥 عن المنصة</h3>
        <br>
        <h4 style="color: #1e40af; font-family: 'Cairo', sans-serif;">تم التطوير بواسطة: فريق بصمة</h4>
        <h5 style="color: #047857; font-family: 'Cairo', sans-serif;">أ. ولاء مقدام</h5>
    </div>
    """, unsafe_allow_html=True)
