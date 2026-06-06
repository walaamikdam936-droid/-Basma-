import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io
import re
import os
import base64

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة بصمة للدمج التعليمية", page_icon="🌟", layout="wide")

hide_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. تفعيل مفتاح جوجل السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تجهيز ذاكرة المنصة (Session State) لحفظ النتائج ومنع اختفائها
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.result_text = ""
    st.session_state.audio_bytes = None
    st.session_state.formatted_doc = None
    st.session_state.audio_lang = 'ar'

# 3. الهيدر الرئيسي وعرض الصورتين (الصورة الأصلية واللوجو الجديد)
col_img1, col_img2 = st.columns(2)
with col_img1:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_column_width=True)
with col_img2:
    if os.path.exists("waw_logo.png"):
        st.image("waw_logo.png", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

# دالة خبيرة لتحويل الصورة إلى كود يمكن قراءته داخل الملفات المحملة
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception:
        return ""

# دالة خبيرة لتحويل النصوص إلى صيغة Word و Web/PDF مع دمج اللوجو
def create_formatted_doc(text, direction, align):
    html_text = text.replace('\n', '<br>')
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_text)
    
    # دمج اللوجو في أعلى الملف المحمل
    logo_base64 = get_base64_image("waw_logo.png")
    img_html = f'<div style="text-align: center; margin-bottom: 20px;"><img src="data:image/png;base64,{logo_base64}" width="150" /></div>' if logo_base64 else ''
    
    doc_content = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head><meta charset='utf-8'></head>
    <body dir='{direction}' style='font-family: "Arial", sans-serif; text-align: {align}; line-height: 1.8; font-size: 16px;'>
        {img_html}
        <h2 style='color: #1e3a8a; text-align: center;'>🌟 الدليل التربوي المخصص - منصة بصمة 🌟</h2>
        <hr>
        <div>{html_text}</div>
    </body>
    </html>
    """
    return doc_content.encode('utf-8')

# 4. تقسيم المنصة (5 تبويبات تفصيلية)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 المساعد الذكي", "🎯 أهداف المنصة وفلسفتها", "⚖️ قانون الدمج", "👥 عن المنصة والفيديو الترحيبي", "📚 مكتبة الإعاقات والمقالات"])

# ==========================================
# --- الصفحة الأولى: المساعد الذكي ---
# ==========================================
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

    st.markdown("---")
    additional_notes = st.text_area("✍️ ملاحظات المعلم الإضافية (اختياري):", placeholder="اكتب هنا أي تفاصيل خاصة بمستوى الطالب...")

    st.markdown("---")
    st.markdown("### 📸 استخراج الخطة والأنشطة (نصياً وصوتياً)")
    uploaded_file = st.file_uploader("ارفع صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="تم رفع الصورة بنجاح", width=350)
        
        if st.button("✨ ابدأ التحليل والاستخراج", use_container_width=True):
            with st.spinner("الذكاء الاصطناعي يقوم بالتحليل..."):
                try:
                    if subject == "لغة إنجليزية":
                        prompt = f"You are a special education expert. Analyze the attached lesson and provide a plan for a grade ({stage}) English lesson for a student with ({disability}). REQUIRED: Fluent English only."
                        if additional_notes:
                            prompt += f"\nTeacher notes: '{additional_notes}'. Integrate these notes."
                        prompt += "\nPoints: 1. Teaching method 2. Three activities 3. Evaluation 4. Teacher Support Tip."
                        audio_lang = 'en'
                    else:
                        prompt = f"أنت خبير تربوي مصري متخصص في التربية الخاصة والدمج التعليمي. حلل الدرس المرفق وقدم دليلاً لمعلم يدرس طالب في ({stage}) لمادة ({subject}) يعاني من ({disability})."
                        if additional_notes:
                            prompt += f"\nملاحظات المعلم: '{additional_notes}'. وظفها إلزامياً في إجابتك وصمم الأنشطة بناءً عليها."
                        prompt += "\nالنقاط الإلزامية: 1. طريقة التدريس المثلى 2. ثلاثة أنشطة تطبيقية ومبتكرة 3. طريقة التقييم المناسبة 4. نصيحة دعم المعلم (توجيه نفسي وتربوي)."
                        audio_lang = 'ar'
                    
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    response = model.generate_content([prompt, image])
                    
                    # حفظ النتائج في ذاكرة الجلسة
                    st.session_state.result_text = response.text
                    st.session_state.audio_lang = audio_lang
                    
                    text_dir = "rtl" if audio_lang == 'ar' else "ltr"
                    text_align = "right" if audio_lang == 'ar' else "left"
                    
                    st.session_state.formatted_doc = create_formatted_doc(st.session_state.result_text, text_dir, text_align)
                    
                    tts = gTTS(text=st.session_state.result_text, lang=audio_lang, slow=False)
                    audio_io = io.BytesIO()
                    tts.write_to_fp(audio_io)
                    st.session_state.audio_bytes = audio_io.getvalue()
                    
                    st.session_state.analysis_done = True
                    st.success("🎉 تم إعداد الدليل التربوي بنجاح!")
                    
                except Exception as e:
                    st.error("حدث خطأ أثناء المعالجة، يرجى المحاولة مرة أخرى.")

    # عرض النتائج من الذاكرة (لكي لا تختفي عند ضغط التحميل)
    if st.session_state.analysis_done:
        text_dir = "rtl" if st.session_state.audio_lang == 'ar' else "ltr"
        text_align = "right" if st.session_state.audio_lang == 'ar' else "left"
        
        res_tab1, res_tab2 = st.tabs(["📑 الخطة المفصلة", "📥 الاستماع والتحميل"])
        with res_tab1:
            st.markdown(f"""<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #cbd5e1; direction: {text_dir}; text-align: {text_align}; line-height: 1.8;">""" + st.session_state.result_text + "</div>", unsafe_allow_html=True)
        with res_tab2:
            st.audio(st.session_state.audio_bytes, format='audio/mp3')
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            col_btn1.download_button("📄 تحميل Word منسق", data=st.session_state.formatted_doc, file_name="lesson_plan.doc", mime="application/msword", use_container_width=True)
            col_btn2.download_button("📑 تحميل كـ PDF (عبر المتصفح)", data=st.session_state.formatted_doc, file_name="lesson_plan.html", mime="text/html", use_container_width=True)
            col_btn3.download_button("🎵 تحميل الملف الصوتي MP3", data=st.session_state.audio_bytes, file_name="lesson_audio.mp3", mime="audio/mp3", use_container_width=True)

# ==========================================
# --- الصفحة الثانية: أهداف المنصة وفلسفتها ---
# ==========================================
with tab2:
    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 30px; border-radius: 15px; border-right: 6px solid #16a34a; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 25px;">
        <h2 style="color: #166534; font-family: 'Cairo', sans-serif; margin-bottom: 15px;">فلسفة "بصمة".. لماذا هذا الاسم؟</h2>
        <p style="font-size: 20px; line-height: 2; text-align: justify; color: #1e293b; font-weight: 500;">
            لقد خلقنا الله سبحانه وتعالى مختلفين، وكما أن لكل إنسان <b>"بصمة إصبع"</b> فريدة لا تتطابق أبداً مع أي إنسان آخر على وجه الأرض، فإن لكل طالب أيضاً بصمته العقلية والنفسية الخاصة في التعلم. فكرة "منصة بصمة" نابعة من إيماننا العميق بأن التعليم ليس قالباً جامداً يُصب فيه جميع الطلاب، بل هو ماء مرن يتشكل ليناسب وعاء كل متعلم. نحن لا نرى في فئات الدمج "طلاباً يعانون من قصور"، بل نراهم طلاباً يمتلكون "بصمات مختلفة" تحتاج فقط إلى أداة ذكية تقرأ هذه البصمة وتقدم لها المعرفة بالطريقة التي تفهمها وتتفاعل معها.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 25px; border-radius: 10px; border-right: 5px solid #3b82f6;">
        <h3 style="color: #1e3a8a;">🎯 الأهداف الاستراتيجية والتفصيلية للمنصة</h3>
        <ul style="font-size: 18px; line-height: 2;">
            <li><b>التمكين الفوري للمعلم:</b> القضاء على العبء الإداري والذهني المستنزف في تحضير خطط الدمج، وتحويله إلى إجراء يتم في ثوانٍ معدودة باستخدام تكنولوجيا الرؤية الحاسوبية والذكاء الاصطناعي، مما يتيح للمعلم التفرغ للجانب الإنساني والتربوي داخل الفصل.</li>
            <li><b>تطبيق مبدأ "العدالة التعليمية":</b> ضمان حصول كل طالب مدمج على حقه الأصيل في فهم المنهج الحكومي المقرر، ولكن من خلال مسارات استراتيجية مبسطة وأنشطة تم تفصيلها خصيصاً لنوع إعاقته.</li>
            <li><b>الدعم النفسي والمهني:</b> تزويد المعلمين بـ "روشتة" نفسية وتربوية مع كل درس لتوجيههم نحو أفضل لغة حوار وأفضل استراتيجية لاحتواء الطالب المدمج، مما يقلل من الفجوة النفسية داخل الفصول الدامجة.</li>
            <li><b>مواكبة الثورة التكنولوجية:</b> إدخال أحدث طرازات الذكاء الاصطناعي (Generative AI) لخدمة الفئات الخاصة، لنثبت أن التكنولوجيا في أسمى صورها هي تلك التي تُسخر لخدمة الإنسان وتذليل الصعاب أمامه.</li>
            <li><b>التوثيق والمتابعة:</b> توفير أدوات تحميل مرنة (Word, PDF, MP3) لضمان قدرة المعلم على طباعة الخطط وإدراجها في سجلاته الرسمية، والعودة إليها في أي وقت وتفعيلها واقعياً.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# --- الصفحة الثالثة: قانون الدمج ---
# ==========================================
with tab3:
    st.markdown("""
    <div style="background-color: #fffbeb; padding: 30px; border-radius: 10px; border-right: 6px solid #f59e0b;">
        <h2 style="color: #b45309; margin-bottom: 20px;">⚖️ قراءة مفصلة في قانون الدمج المصري (القرار الوزاري 252 لسنة 2017)</h2>
        <p style="font-size: 20px; line-height: 2; text-align: justify; color: #451a03; margin-bottom: 20px;">
            يُعد القرار الوزاري المصري رقم 252 لسنة 2017 بمثابة المظلة القانونية والتربوية التي تضمن حقوق الطلاب ذوي الإعاقة البسيطة في تلقي تعليم متكافئ داخل مدارس التعليم العام والفني. يهدف هذا القرار إلى إنهاء العزلة التعليمية لهذه الفئات، حيث يسمح بدمج الطلاب الذين يعانون من إعاقات بصرية أو سمعية أو حركية، بالإضافة إلى ذوي الإعاقة الذهنية البسيطة، وبطء التعلم، واضطراب طيف التوحد (الدمج الخفيف)، ومتلازمة داون. وقد راعى القانون الفروق الفردية العميقة من خلال إقرار استثناءات تنظيمية هامة، مثل التجاوز عن شرط السن عند القبول بالمدارس بزيادة تصل إلى عامين عن الطلاب العاديين، وذلك لضمان حصول كل طالب على فرصته العادلة والكاملة في التعليم ضمن بيئة مدرسية طبيعية تدعم تقبل الاختلاف وتساند جهود الأسرة.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# --- الصفحة الرابعة: عن المنصة والفيديو الترحيبي ---
# ==========================================
with tab4:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 25px; border-radius: 15px; border-right: 6px solid #1e3a8a; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h2 style="color: #1e3a8a; font-family: 'Cairo', sans-serif; margin-bottom: 15px;">🚀 رسالتنا الفلسفية والتربوية</h2>
        <p style="font-size: 20px; line-height: 1.8; color: #1e293b; text-align: justify; font-weight: 500;">
            نحن مجموعة من المعلمين المهتمين بطلاب ذوي الهمم، هدفنا أن يحصل كل طالب على فرصة في التعليم، ويكون عضو فعال داخل المجتمع.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎬 الفيديو التعريفي للمنصة")
    st.markdown('<iframe src="https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview" width="100%" height="450" style="border: none; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></iframe>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #0f766e; margin-top: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
        <h2 style="color: #0f766e; font-family: 'Cairo', sans-serif; margin: 0; font-size: 28px;">تم الابتكار والتصميم والبرمجة بواسطة ولاء مقدام</h2>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# --- الصفحة الخامسة: مكتبة الإعاقات والمقالات ---
# ==========================================
with tab5:
    st.markdown("""
    <div style="background-color: #e0f2fe; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
        <h2 style="color: #0369a1; margin:0; font-family: 'Cairo', sans-serif;">📚 مكتبة بصمة التخصصية للإعاقات والمقالات المتجددة</h2>
    </div>
    """, unsafe_allow_html=True)
    
    lib_tab1, lib_tab2 = st.tabs(["📖 مقالات الإعاقات والشخصيات الملهمة", "📰 زاوية المقالات الأسبوعية المتجددة"])
    
    with lib_tab1:
        with st.expander("👁️ الإعاقة البصرية (ضعف البصر وكف البصر)"):
            st.markdown("""
            ### 🔸 ماهية الإعاقة البصرية
            هي فقدان كلي أو جزئي لحاسة البصر لا يمكن تصحيحه بالنظارات الطبية العادية، مما يؤثر على قدرة الطالب على التفاعل مع المدخلات البصرية.
            ### 🌟 شخصيات عالمية قهرت الإعاقة البصرية
            * **د. طه حسين:** عميد الأدب العربي.
            * **لويس برايل:** مخترع طريقة "برايل" للقراءة.
            ### 🎯 أفضل 3 استراتيجيات للتدريس
            1. **لعب الأدوار (القارئ الزميل):** تبادل الأدوار بوصف المجسمات.
            2. **الألعاب التعليمية (السمعية):** ألعاب التمييز الصوتي.
            3. **التعلم التعاوني:** دمج الطالب في أنشطة تعتمد على الحواس الأخرى.
            """)
        with st.expander("👂 الإعاقة السمعية (ضعاف السمع)"):
            st.markdown("""
            ### 🔸 ماهية الإعاقة السمعية
            هي قصور في حاسة السمع يؤثر على اكتساب اللغة واستقبال المعلومات الصوتية.
            ### 🌟 شخصيات عالمية قهرت الإعاقة السمعية
            * **توماس إديسون:** المخترع الأعظم في التاريخ.
            * **لودفيج فان بيتهوفن:** الموسيقار الأسطوري.
            ### 🎯 أفضل 3 استراتيجيات للتدريس
            1. **الألعاب التعليمية (البصرية):** ألعاب التطابق والتمثيل الصامت.
            2. **المعلم الصغير:** إعطاء الطالب دوراً في قيادة نشاط حركي أو بصري.
            3. **التعلم التعاوني:** باستخدام لغة الإشارة البسيطة بين الأقران.
            """)
        with st.expander("🧠 الإعاقة الذهنية البسيطة وبطء التعلم"):
            st.markdown("""
            ### 🔸 ماهية الإعاقة
            قصور في الوظائف الذهنية أو بطء في استيعاب المعلومات مقارنة بالأقران.
            ### 🌟 شخصيات تحدت الصعوبات الذهنية
            * **ألبرت أينشتاين:** عانى من صعوبات تعلم وتأخر نطق في طفولته.
            * **محمد علي كلاي:** عانى من صعوبات تعلم (الدسلكسيا).
            ### 🎯 أفضل 3 استراتيجيات للتدريس
            1. **الألعاب التعليمية:** ألعاب الفك والتركيب مع مكافآت فورية.
            2. **لعب الأدوار:** النمذجة والتقليد الهادئ.
            3. **الكرسي الساخن:** توجيه أسئلة مبسطة جداً لتعزيز ثقته عند الإجابة.
            """)
        with st.expander("🧩 اضطراب طيف التوحد (الدمج الخفيف)"):
            st.markdown("""
            ### 🔸 ماهية اضطراب طيف التوحد
            اضطراب نمائي عصبي يؤثر على التواصل الاجتماعي والتفاعل.
            ### 🌟 شخصيات عالمية ملهمة
            * **تمبل جراندين:** عالمة سلوك حيواني شهيرة.
            * **إيلون ماسك:** الملياردير والمبتكر.
            ### 🎯 أفضل 3 استراتيجيات للتدريس
            1. **الألعاب التعليمية (المنظمة):** ألعاب ذات قواعد واضحة ونهايات متوقعة مثل البازل.
            2. **التعلم التعاوني (الصديق الموازي):** اللعب الموازي بجوار الزميل لتقليل التوتر.
            3. **المعلم الصغير:** تكليفه بمهمة روتينية يحبها داخل الفصل.
            """)
        with st.expander("♿ الإعاقة الحركية (مثل الشلل الدماغي البسيط)"):
            st.markdown("""
            ### 🔸 ماهية الإعاقة الحركية
            خلل يؤثر على القدرة الحركية مع بقاء القدرات الذهنية سليمة أو ممتازة.
            ### 🌟 شخصيات عالمية قهرت الإعاقة
            * **ستيفن هوكينج:** عالم الفيزياء النظرية الأعظم.
            * **فرانكلين روزفلت:** الرئيس الأمريكي الذي قاد بلاده وهو مقعد.
            ### 🎯 أفضل 3 استراتيجيات للتدريس
            1. **التعلم التعاوني:** تعديل قواعد اللعب ليتمكن من المشاركة (مثل تسجيل النقاط).
            2. **الكرسي الساخن:** إبراز قدراته الذهنية ومهاراته اللفظية أمام زملائه.
            3. **المعلم الصغير:** قيادة المجموعات الشفهية والمناقشات.
            """)

    with lib_tab2:
        st.markdown("### 📰 مقالات تربوية تفصيلية (يتم تحديثها أسبوعياً):")
        
        with st.expander("📖 المقال الأول: الفارق الجوهري بين المساواة والعدالة في التعليم"):
            st.markdown("""
            تنطلق الفلسفة الحديثة للتربية الخاصة من فهم دقيق للفارق بين المساواة والعدالة. إن تقديم نفس المنهج ونفس الأدوات لجميع الطلاب داخل فصول الدمج يمثل نموذجاً للمساواة الظاهرية، لكنه يفتقر إلى العدالة الحقيقية.
            العدالة التعليمية تقتضي تزويد كل طالب ذي همة بالأداة أو الاستراتيجية التي تحيد أثر إعاقته، لتمكينه من الوصول للمعلومة على قدم المساواة مع أقرانه العاديين. فعلى سبيل المثال، تقديم النص المكتوب لطالب كفيف يعد مساواة، بينما توفير النص الصوتي أو بطريقة برايل هو التجسيد الفعلي للعدالة التعليمية.
            """)
            
        with st.expander("📖 المقال الثاني: الدور المحوري لمعلم غرفة المصادر في الفصول الدامجة"):
            st.markdown("""
            تُعد غرفة المصادر الركيزة الأساسية لإنجاح منظومة الدمج التعليمي في المدارس. ولا يقتصر دور معلم غرفة المصادر على التدريس الأكاديمي المباشر، بل يمتد ليشمل تشخيص الصعاب وتحديد مستويات الأداء الأكاديمي والنمائي للطلاب.
            يقوم المعلم ببناء الخطط التربوية الفردية بالتنسيق المستمر مع معلم الفصل العام، وتجهيز الوسائل التعليمية الملموسة والبصرية التي تساند الطالب، فضلاً عن تقديم الدعم النفسي والتربوي الذي يعزز دافعية الطالب للتعلم ويسهل اندماجه الأكاديمي.
            """)
            
        with st.expander("📖 المقال الثالث: أهمية الدمج التعليمي وأثره في تطوير القدرات"):
            st.markdown("""
            إن الدمج التعليمي ليس مجرد إجراء تنظيمي أو قانوني، بل هو استراتيجية إنسانية وتربوية متكاملة تهدف إلى صهر الطلاب ذوي الهمم في بيئات التعلم الطبيعية. يسهم الدمج التعليمي بشكل مباشر في رفع مستوى الاستيعاب الأكاديمي للطالب المدمج من خلال المحاكاة والتعلم بالأقران.
            كما يتيح للطلاب العاديين فرصة حقيقية لتقبل الاختلاف ونبذ التنمر، مما يخلق مجتمعاً مدرسياً سوياً يرى في التنوع البشري مصدراً للقوة والتميز الجماعي.
            """)
            
        with st.expander("📖 المقال الرابع: الدمج المجتمعي.. الغاية الأسمى للتمكين"):
            st.markdown("""
            يبدأ الدمج الفعلي من الغرفة الصفية، لكن غايته الأسمى هي التمكين المجتمعي الشامل. يهدف الدمج المجتمعي إلى إعداد الطالب ذي الهمة ليكون عنصراً مستقلاً، منتجاً، وقادراً على العطاء داخل نسيج المجتمع بعد انتهاء المراحل الدراسية.
            إن نجاح الدمج المجتمعي يقاس بمدى قدرة البيئات العامة، الثقافية، والمهنية على استيعاب قدرات هؤلاء الأفراد وتوفير الفرص العادلة لهم للعمل والمشاركة، مما يسهم في تغيير النظرة النمطية السلبية وتحويلها إلى شراكة حقيقية في بناء الوطن.
            """)
            
        st.markdown("""
        ---
        ### 💡 مراجعة لأهم استراتيجيات تدريس طلاب الدمج المضمنة في المنصة:
        1. **لعب الأدوار:** تضع الطالب في مواقف حياتية مبسطة، مما يحسن من مهاراته الاجتماعية والتواصلية (ممتازة للتوحد والإعاقة الذهنية).
        2. **التعلم التعاوني:** تذيب الفوارق بين الطلاب العاديين والمدمجين، وتخلق بيئة من الدعم المتبادل والألفة.
        3. **الكرسي الساخن:** تكسر حاجز الخجل والخوف لدى الطالب المدمج، حيث يجلس ليجيب عن أسئلة في مستوى قدراته، مما يرفع ثقته بنفسه للسماء.
        4. **المعلم الصغير:** تمنح الطالب المدمج دور القيادة ولو لدقائق معدودة (مثل توزيع الأوراق أو شرح فكرة بسيطة)، مما يجعله يشعر بأهميته وكيانه المستقل.
        5. **الألعاب التعليمية:** المدخل السحري لعقل أي طفل؛ فهي تحول المنهج الجاف إلى متعة وتحدٍ، وتناسب جميع الإعاقات بلا استثناء إذا تم توظيفها بذكاء.
        """)
