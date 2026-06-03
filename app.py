import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io
import re

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", page_icon="🌟", layout="wide")

hide_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. تفعيل مفتاح جوجل السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. الهيدر الرئيسي
st.image("logo.jpg", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

# دالة خبيرة لتحويل النصوص إلى صيغة Word و Web/PDF منسقة
def create_formatted_doc(text, direction, align):
    # تحويل التنسيقات النجمية إلى تنسيقات HTML ليقرأها الوورد
    html_text = text.replace('\n', '<br>')
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_text)
    
    doc_content = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head><meta charset='utf-8'></head>
    <body dir='{direction}' style='font-family: "Arial", sans-serif; text-align: {align}; line-height: 1.8; font-size: 16px;'>
        <h2 style='color: #1e3a8a; text-align: center;'>🌟 الدليل التربوي المخصص - منصة بصمة 🌟</h2>
        <hr>
        <div>{html_text}</div>
    </body>
    </html>
    """
    return doc_content.encode('utf-8')

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
        disability = st.selectbox("🧩 نوع الإعاقة (حسب القرار الوزاري):", [
            "إعاقة ذهنية بسيطة", "بطء تعلم", "طيف التوحد (دمج خفيف)", 
            "إعاقة بصرية (ضعف بصر)", "إعاقة بصرية (كف بصر)", 
            "إعاقة سمعية (ضعف سمع)", "صعوبات تعلم أكاديمية", "إعاقة حركية (شلل دماغي بسيط)"
        ])

    st.markdown("---")
    additional_notes = st.text_area("✍️ ملاحظات المعلم الإضافية (اختياري):", 
                                    placeholder="اكتب هنا أي تفاصيل خاصة بمستوى الطالب، أو صعوبات يواجهها، ليقوم الذكاء الاصطناعي ببناء الخطة بناءً عليها...")

    st.markdown("---")
    st.markdown("### 📸 استخراج الخطة والأنشطة (نصياً وصوتياً)")
    uploaded_file = st.file_uploader("ارفعي صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="تم رفع الصورة بنجاح", width=350)
        
        if st.button("✨ ابدأ التحليل والاستخراج", use_container_width=True):
            with st.spinner("الذكاء الاصطناعي يقوم بتحليل الدرس وإعداد الدليل التربوي والصوتي..."):
                try:
                    if subject == "لغة إنجليزية":
                        prompt = f"""
                        You are an educational expert specializing in special education and educational inclusion.
                        Analyze the attached lesson image and provide a comprehensive lesson plan for a teacher teaching a student in ({stage}) for the subject (English) who has ({disability}).
                        
                        CRITICAL REQUIRED RULE: The entire response must be written in fluent English. Do not write Arabic words.
                        """
                        if additional_notes:
                            prompt += f"\nCRITICAL: The teacher provided these specific notes: '{additional_notes}'. You MUST explicitly integrate these notes into the teaching method and activities. Create a specific section titled 'Addressing Teacher Notes' to show how you used them."
                        
                        prompt += """
                        Provide the response in clear points:
                        1. The optimal teaching method.
                        2. Three (3) practical educational activities suited for the student.
                        3. Evaluation method.
                        4. "Teacher Support" Tip (Psychological guidance).
                        """
                        audio_lang = 'en'
                    else:
                        prompt = f"""
                        أنت خبير تربوي مصري متخصص في التربية الخاصة والدمج التعليمي. 
                        قم بتحليل الدرس المرفق، وقدم دليلاً لمعلم يدرس طالب في ({stage}) لمادة ({subject}) يعاني من ({disability}).
                        """
                        if additional_notes:
                            prompt += f"\nهام جداً: لقد كتب المعلم هذه الملاحظات الخاصة بالطالب: '{additional_notes}'. يجب عليك إلزامياً بناء الأنشطة وطريقة التدريس لتتلاءم مع هذه الملاحظات، مع إضافة قسم في إجابتك بعنوان 'تلبية ملاحظات المعلم' توضح فيه كيف وظفت ملاحظاته في خطتك."
                            
                        prompt += """
                        قدم الإجابة باللغة العربية الفصحى في نقاط مباشرة:
                        1. طريقة التدريس المثلى لهذا المحتوى.
                        2. ثلاثة (3) أنشطة تعليمية تطبيقية ومبتكرة.
                        3. طريقة التقييم المناسبة.
                        4. نصيحة "دعم المعلم": توجيه نفسي وتربوي قصير للمعلم.
                        """
                        audio_lang = 'ar'
                    
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    response = model.generate_content([prompt, image])
                    
                    result_text = response.text
                    
                    st.success("🎉 تم إعداد الدليل التربوي بنجاح!")
                    st.balloons()
                    
                    text_direction = "rtl" if audio_lang == 'ar' else "ltr"
                    text_align = "right" if audio_lang == 'ar' else "left"
                    
                    res_tab1, res_tab2 = st.tabs(["📑 الخطة التربوية المفصلة", "📥 الاستماع والتحميل المنسق"])
                    
                    with res_tab1:
                        st.markdown(f"""<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #cbd5e1; direction: {text_direction}; text-align: {text_align}; line-height: 1.8;">""", unsafe_allow_html=True)
                        st.markdown(result_text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    with res_tab2:
                        with st.spinner("جاري تجهيز المقطع الصوتي..."):
                            tts = gTTS(text=result_text, lang=audio_lang, slow=False)
                            audio_bytes = io.BytesIO()
                            tts.write_to_fp(audio_bytes)
                            audio_bytes.seek(0)
                            
                            st.markdown("### 🎧 استمع إلى الخطة والأنشطة:")
                            st.audio(audio_bytes, format='audio/mp3')
                            
                            st.markdown("---")
                            st.markdown("### 💾 خيارات الحفظ (Word & PDF)")
                            
                            col_btn1, col_btn2, col_btn3 = st.columns(3)
                            
                            # 1. تحميل كملف Word منسق
                            formatted_doc = create_formatted_doc(result_text, text_direction, text_align)
                            with col_btn1:
                                st.download_button(
                                    label="📄 تحميل كملف Word (للتعديل والطباعة)",
                                    data=formatted_doc,
                                    file_name="lesson_plan.doc",
                                    mime="application/msword",
                                    use_container_width=True
                                )
                                
                            # 2. تحميل كصفحة ويب (للحفظ كـ PDF)
                            with col_btn2:
                                st.download_button(
                                    label="📑 تحميل كصفحة ويب (احفظها كـ PDF)",
                                    data=formatted_doc,
                                    file_name="lesson_plan.html",
                                    mime="text/html",
                                    use_container_width=True
                                )
                                
                            # 3. تحميل الصوت
                            with col_btn3:
                                st.download_button(
                                    label="🎵 تحميل المقطع الصوتي (MP3)",
                                    data=audio_bytes.getvalue(),
                                    file_name="lesson_audio.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True
                                )
                        
                except Exception as e:
                    st.error("حدث خطأ أثناء المعالجة، يرجى التأكد من وضوح الصورة والمحاولة مرة أخرى.")
                    st.info(f"تفاصيل الخطأ: {str(e)}")

# --- باقي الصفحات (الأهداف، القانون، عن المنصة) ---
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

with tab3:
    st.markdown("""
    <div style="background-color: #fffbeb; padding: 20px; border-radius: 10px; border-right: 5px solid #f59e0b;">
        <h3 style="color: #b45309;">⚖️ ملخص قانون الدمج المصري (القرار الوزاري 252 لسنة 2017)</h3>
        <ul style="font-size: 18px; line-height: 1.8;">
            <li><b>نظام الدمج:</b> يهدف إلى توفير فرص تعليمية متكافئة للطلاب ذوي الإعاقة البسيطة بمدارس التعليم العام.</li>
            <li><b>الفئات المسموح لها بالدمج:</b> الإعاقة البصرية، الإعاقة الحركية، الإعاقة السمعية، الإعاقة الذهنية البسيطة، بطء التعلم، التوحد.</li>
            <li><b>دور المعلم:</b> إعداد خطة تربوية فردية تتناسب مع قدرات الطالب.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

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
        st.image("logo.jpg", caption="ذوو الهمم.. طاقة وإصرار يبني المستقبل الفردي والمجتمعي", use_column_width=True)
        
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
