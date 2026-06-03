import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", page_icon="🌟", layout="wide")

hide_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. تفعيل مفتاح جوجل السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. الهيدر الرئيسي (تم تعديله ليقرأ الصورة المحلية المعتمدة logo.jpg)
st.image("logo.jpg", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

# 4. تقسيم المنصة 
tab1, tab2, tab3, tab4 = st.tabs(["🚀 المساعد الذكي للدمج", "🎯 أهداف المنصة", "⚖️ قانون الدمج المصري", "👥 عن المنصة"])

# --- الصفحة الأولى: المساعد الذكي ---
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
        # تعديل وفصل الإعاقة الذهنية البسيطة عن بطء التعلم بناءً على طلبك
        disability = st.selectbox("🧩 نوع الإعاقة (حسب القرار الوزاري):", [
            "إعاقة ذهنية بسيطة", "بطء تعلم", "طيف التوحد (دمج خفيف)", 
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
                    # التحقق التلقائي إذا كانت المادة لغة إنجليزية لتغيير لغة المحتوى والصوت بالكامل
                    if subject == "لغة إنجليزية":
                        prompt = f"""
                        You are an educational expert specializing in special education and educational inclusion.
                        Based on educational inclusion standards, analyze the attached lesson image and provide a comprehensive, professional lesson plan for a teacher teaching a student in ({stage}) for the subject (English) who has ({disability}).
                        
                        CRITICAL REQUIRED RULE: The entire response must be written in fluent, professional English because the subject is English. Do not write any Arabic words.
                        
                        Provide the response in clear points containing:
                        1. The optimal teaching method for this content suited for the mentioned disability.
                        2. Three (3) practical and innovative educational activities suited for the student's abilities.
                        3. The appropriate evaluation and measurement method for their understanding.
                        """
                        audio_lang = 'en'
                    else:
                        prompt = f"""
                        أنت خبير تربوي مصري متخصص في التربية الخاصة والدمج التعليمي. 
                        استناداً إلى قانون الدمج المصري، قم بتحليل الدرس في الصورة المرفقة، وقدم دليلاً مبسطاً وموجهاً لمعلم يدرس طالب في ({stage}) لمادة ({subject}) يعاني من ({disability}).
                        قدم الإجابة باللغة العربية الفصحى الواضحة في نقاط مباشرة تحتوي على:
                        1. طريقة التدريس المثلى لهذا المحتوى بما يتناسب مع الإعاقة المذكورة.
                        2. ثلاثة (3) أنشطة تعليمية تطبيقية ومبتكرة تناسب قدرات الطالب.
                        3. طريقة التقييم المناسبة لقياس استيعاب الطالب للدرس.
                        """
                        audio_lang = 'ar'
                    
                    # نظام الحماية التبادلي التلقائي لمنع خطأ الـ 404 تماماً
                    try:
                        model = genai.GenerativeModel('gemini-pro-vision')
                        response = model.generate_content([prompt, image])
                    except Exception:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content([prompt, image])
                    
                    result_text = response.text
                    
                    st.success("🎉 تم إعداد الدليل التربوي بنجاح!")
                    st.markdown("""<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #cbd5e1;">""", unsafe_allow_html=True)
                    st.markdown(result_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    with st.spinner("جاري تجهيز المقطع الصوتي..."):
                        tts = gTTS(text=result_text, lang=audio_lang, slow=False)
                        audio_bytes = io.BytesIO()
                        tts.write_to_fp(audio_bytes)
                        audio_bytes.seek(0)
                        
                        st.markdown("### 🎧 استمع إلى الخطة التربوية والأنشطة:")
                        st.audio(audio_bytes, format='audio/mp3')
                        
                except Exception as e:
                    st.error("حدث خطأ أثناء المعالجة، يرجى التأكد من وضوح الصورة والمحاولة مرة أخرى.")
                    st.info(f"تفاصيل الخطأ: {str(e)}")

# --- الصفحة الثانية: الأهداف ---
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

# --- الصفحة الثالثة: قانون الدمج ---
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

# --- الصفحة الرابعة: عن المنصة ---
with tab4:
    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 30px; border-radius: 15px; border-right: 6px solid #16a34a; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 25px;">
        <h2 style="color: #166534; font-family: 'Cairo', sans-serif; margin-bottom: 15px;">👤 فلسفتنا ورؤيتنا</h2>
        <p style="font-size: 22px; line-height: 2; text-align: justify; color: #1e293b; font-weight: 500;">
            نحن أمة من حق كل طالب فيها أن يتعلم بالطريقة التي تناسبه، ومن هنا ولدت فكرة <b>"منصة بصمة"</b>؛ فكما أن لكل طالب بصمة أصابع فريدة ومختلفة تميزه عن غيره، فإن لكل إنسان طريقته الخاصة وأسلوبه الفريد في التعلم واستيعاب المعرفة.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_img, col_dev = st.columns([1.2, 1])
    
    with col_img:
        # تعديل الصورة لتقرأ الملف المحلي logo.jpg بدلاً من الرابط الخارجي
        st.image("logo.jpg", 
                 caption="ذوو الهمم.. طاقة وإصرار يبني المستقبل الفردي والمجتمعي", use_column_width=True)
        
    with col_dev:
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
            <div style="font-size: 50px; margin-bottom: 10px;">🛡️</div>
            <h3 style="color: #1e3a8a; font-family: 'Cairo', sans-serif; font-size: 26px; margin-bottom: 15px;">فريق العمل والإطلاق</h3>
            <div style="background-color: #ffffff; padding: 15px 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); width: 80%;">
                <h4 style="color: #2563eb; font-family: 'Cairo', sans-serif; margin: 0; font-size: 20px;">تم التطوير بواسطة:</h4>
                <h3 style="color: #0f766e; font-family: 'Cairo', sans-serif; margin: 10px 0 0 0; font-size: 24px;">فريق بصمة</h3>
                <p style="color: #475569; font-weight: bold; font-size: 18px; margin: 5px 0 0 0;">أ. ولاء مقدام</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
