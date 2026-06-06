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
st.image("logo.jpg", use_column_width=True)

st.markdown("""
    <div style="text-align: center; background-color: #1e3a8a; padding: 30px; border-radius: 15px; margin-bottom: 25px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-size: 40px;">🌟 منصة بصمة للدمج التعليمية 🌟</h1>
        <h3 style="color: #bfdbfe; font-style: italic; font-weight: normal; margin-top: 5px;">"التعليم حق للجميع.. وبدمجهم تكتمل لوحة المجتمع ونبني مستقبلاً يجمعنا"</h3>
    </div>
""", unsafe_allow_html=True)

# دالة تحويل النصوص إلى صيغة Word
def create_formatted_doc(text, direction, align):
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

# 4. تقسيم المنصة (التبويبات المحدثة)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 المساعد الذكي", "🎯 أهداف المنصة وفلسفتها", "⚖️ قانون الدمج", "👥 عن المنصة والفيديو الترحيبي", "📚 مكتبة الإعاقات والمقالات"])

# --- الصفحة الأولى: المساعد الذكي ---
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
    uploaded_file = st.file_uploader("حدد صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="تم رفع الصورة بنجاح", width=350)
        
        if st.button("✨ ابدأ التحليل والاستخراج", use_container_width=True):
            with st.spinner("الذكاء الاصطناعي يقوم بالتحليل..."):
                try:
                    if subject == "لغة إنجليزية":
                        prompt = f"Analyze the lesson for grade ({stage}) English lesson for a student with ({disability})."
                        audio_lang = 'en'
                    else:
                        prompt = f"حلل الدرس لمادة ({subject}) للصف ({stage}) لطالب يعاني من ({disability})."
                        audio_lang = 'ar'
                    
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, image])
                    
                    st.session_state.result_text = response.text
                    st.session_state.audio_lang = audio_lang
                    
                    text_dir = "rtl" if audio_lang == 'ar' else "ltr"
                    text_align = "right" if audio_lang == 'ar' else "left"
                    st.session_state.formatted_doc = create_formatted_doc(st.session_state.result_text, text_dir, text_align)
                    
                    tts = gTTS(text=st.session_state.result_text, lang=audio_lang)
                    audio_io = io.BytesIO()
                    tts.write_to_fp(audio_io)
                    st.session_state.audio_bytes = audio_io.getvalue()
                    
                    st.session_state.analysis_done = True
                    st.success("🎉 تم إعداد الدليل التربوي بنجاح!")
                except Exception as e:
                    st.error("حدث خطأ، تأكد من مفتاح API وحاول مرة أخرى.")

    if st.session_state.analysis_done:
        res_tab1, res_tab2 = st.tabs(["📑 الخطة المفصلة", "📥 الاستماع والتحميل"])
        with res_tab1:
            st.markdown(f'<div style="direction: rtl; text-align: right;">{st.session_state.result_text}</div>', unsafe_allow_html=True)
        with res_tab2:
            st.audio(st.session_state.audio_bytes, format='audio/mp3')
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            col_btn1.download_button("📄 تحميل Word", data=st.session_state.formatted_doc, file_name="lesson_plan.doc")
            col_btn2.download_button("📑 تحميل PDF", data=st.session_state.formatted_doc, file_name="lesson_plan.html")
            col_btn3.download_button("🎵 تحميل الصوت", data=st.session_state.audio_bytes, file_name="lesson_audio.mp3")

# --- الصفحة الثانية: أهداف المنصة ---
with tab2:
    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 30px; border-radius: 15px; border-right: 6px solid #16a34a; margin-bottom: 25px;">
        <h2 style="color: #166534; font-family: 'Cairo', sans-serif;">فلسفة "بصمة".. لماذا هذا الاسم؟</h2>
        <p style="font-size: 20px; line-height: 2; text-align: justify; color: #1e293b;">
            لقد خلقنا الله سبحانه وتعالى مختلفين، وكما أن لكل إنسان بصمة إصبع فريدة، فإن لكل طالب بصمته العقلية الخاصة. فكرة المنصة نابعة من إيماننا بأن التعليم ليس قالباً جامداً، بل هو ماء مرن يتشكل ليناسب وعاء كل متعلم.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة الثالثة: قانون الدمج ---
with tab3:
    st.markdown("""
    <div style="background-color: #fffbeb; padding: 30px; border-radius: 10px; border-right: 6px solid #f59e0b;">
        <h2 style="color: #b45309;">⚖️ قراءة في القرار الوزاري 252 لسنة 2017</h2>
        <p style="font-size: 20px; line-height: 2; text-align: justify; color: #451a03;">
            يُعد القرار الوزاري رقم 252 لسنة 2017 بمثابة المظلة القانونية التي تضمن حقوق الطلاب ذوي الإعاقة البسيطة في التعليم العام. يهدف القرار لإنهاء العزلة التعليمية، ويضمن حق الطالب في "خطة تربوية فردية" وهو ما توفره منصة بصمة بضغطة زر.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة الرابعة: عن المنصة والفيديو ---
with tab4:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 30px; border-radius: 15px; border-right: 6px solid #1e3a8a; margin-bottom: 25px;">
        <h2 style="color: #1e3a8a; font-family: 'Cairo', sans-serif;">رسالتنا ومن نحن؟</h2>
        <p style="font-size: 22px; line-height: 1.8; color: #1e293b; text-align: justify;">
            نحن مجموعة من المعلمين المهتمين بطلاب الدمج ونريد لهم حياة أفضل داخل مجتمعنا، لذلك نقدم لهم ولمعلمى التربية الخاصة هذه المنصة لتكون يداً ممدودة تساعد في تقديم أفضل ما لديهم لهؤلاء الأطفال المبدعين.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎬 الفيديو التعريفي للمنصة")
    # تم تعديل الرابط ليعمل كـ Preview داخل Streamlit
    video_url = "https://drive.google.com/file/d/1hGUiJqBkjJhckuO72OMyOul_TtxjTkVJ/preview"
    st.video(video_url)
    
    st.markdown("""
    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0;">
        <h3 style="color: #0f766e; font-family: 'Cairo', sans-serif;">تم الابتكار والتطوير والبرمجة بواسطة: ولاء مقدام</h3>
        <p style="color: #64748b;">(عمل مستقل مخصص لخدمة التعليم - بدون أى مؤسسات حكومية أو إدارةت)</p>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة الخامسة: المكتبة والاستراتيجيات ---
with tab5:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>📚 مكتبة الإعاقات والاستراتيجيات الشاملة</h2>", unsafe_allow_html=True)
    
    m_tab1, m_tab2, m_tab3 = st.tabs(["🔍 شرح الإعاقات ومشاهيرها", "💡 استراتيجيات التدريس", "📝 مقالات الدمج المصرية"])
    
    with m_tab1:
        with st.expander("👁️ الإعاقة البصرية"):
            st.write("**الوصف:** فقدان كلي أو جزئي للبصر.")
            st.write("**أبرز المشاهير:** عميد الأدب العربي **طه حسين**، والمخترع **لويس برايل**.")
            st.info("🎯 الاستراتيجيات: 1. الوصف الصوتي الدقيق. 2. استخدام المجسمات الملموسة. 3. طريقة برايل.")
            
        with st.expander("👂 الإعاقة السمعية"):
            st.write("**الوصف:** ضعف في استقبال الترددات الصوتية.")
            st.write("**أبرز المشاهير:** العالم **توماس أديسون**، والموسيقار **بيتهوفن**.")
            st.info("🎯 الاستراتيجيات: 1. لغة الإشارة. 2. لغة الشفاه والتواصل البصري. 3. استخدام الصور التوضيحية.")
            
        with st.expander("🧩 طيف التوحد"):
            st.write("**الوصف:** اضطراب نمائي يؤثر على التواصل الاجتماعي.")
            st.write("**أبرز المشاهير:** العالمة **تمبل جراندين**، والمبتكر **إيلون ماسك**.")
            st.info("🎯 الاستراتيجيات: 1. الجداول البصرية. 2. القصص الاجتماعية. 3. النمذجة.")

        with st.expander("♿ الإعاقة الحركية"):
            st.write("**الوصف:** قصور في الجهاز الحركي.")
            st.write("**أبرز المشاهير:** العالم **ستيفن هوكينج**، والرئيس الأمريكي **روزفلت**.")
            st.info("🎯 الاستراتيجيات: 1. تهيئة البيئة الفيزيائية. 2. التكنولوجيا المساعدة. 3. دعم الأقران.")

    with m_tab2:
        st.markdown("""
        ### 🛠️ أفضل استراتيجيات تدريس الدمج:
        1. **لعب الأدوار:** تمثيل المواقف الاجتماعية لتبسيط المفاهيم.
        2. **التعلم التعاوني:** دمج طالب الدمج في مجموعات مع أقرانه لتعزيز التفاعل.
        3. **الكرسي الساخن:** تحفيز الطالب على الإجابة عن الأسئلة لزيادة الثقة.
        4. **المعلم الصغير:** إعطاء طالب الدمج دوراً قيادياً بسيطاً في الشرح.
        5. **الألعاب التعليمية:** استخدام اللعب كمدخل أساسي لجذب الانتباه وتثبيت المعلومة.
        """)

    with m_tab3:
        st.markdown("""
        ### 🇪🇬 مقالات في الدمج المصري:
        * **المساواة والعدالة:** الفرق بين مساواة الطلاب في المنهج وعدالة تقديم الوسيلة المناسبة.
        * **دور معلم غرف المصادر:** كيف يساهم المعلم في سد الفجوة بين المنهج وقدرات الطالب.
        * **أهمية الدمج المجتمعي:** لماذا الدمج المدرسي هو الخطوة الأولى لبيئة سوية.
        """)
