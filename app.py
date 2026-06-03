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

# دالة خبيرة لتحويل النصوص إلى صيغة Word و Web/PDF
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

# 4. تقسيم المنصة (تمت إضافة التبويب الخامس)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 المساعد الذكي", "🎯 الأهداف", "⚖️ قانون الدمج", "👥 عن المنصة", "📚 مكتبة بصمة الشاملة"])

# --- الصفحة الأولى: المساعد الذكي ---
with tab1:
    st.markdown("### 📝 حددي خصائص الدرس وفئة الدمج:")
    col1, col2, col3 = st.columns(3)
    with col1:
        stage = st.selectbox("📚 المرحلة الدراسية:", ["الصف الأول الابتدائي", "الصف الثاني الابتدائي", "الصف الثالث الابتدائي", "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي"])
    with col2:
        subject = st.selectbox("📖 المادة الدراسية:", ["لغة عربية", "رياضيات", "علوم / اكتشف", "دراسات اجتماعية", "لغة إنجليزية", "تربية دينية"])
    with col3:
        disability = st.selectbox("🧩 نوع الإعاقة:", ["إعاقة ذهنية بسيطة", "بطء تعلم", "طيف التوحد (دمج خفيف)", "إعاقة بصرية (ضعف بصر)", "إعاقة بصرية (كف بصر)", "إعاقة سمعية (ضعف سمع)", "صعوبات تعلم أكاديمية", "إعاقة حركية (شلل دماغي بسيط)"])

    st.markdown("---")
    additional_notes = st.text_area("✍️ ملاحظات المعلم الإضافية (اختياري):", placeholder="اكتب هنا أي تفاصيل خاصة بمستوى الطالب...")

    st.markdown("---")
    st.markdown("### 📸 استخراج الخطة والأنشطة (نصياً وصوتياً)")
    uploaded_file = st.file_uploader("ارفعي صورة الدرس هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
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
                        prompt = f"أنت خبير تربوي. حلل الدرس المرفق وقدم دليلاً لمعلم يدرس طالب في ({stage}) لمادة ({subject}) يعاني من ({disability})."
                        if additional_notes:
                            prompt += f"\nملاحظات المعلم: '{additional_notes}'. وظفها في إجابتك."
                        prompt += "\nالنقاط: 1. طريقة التدريس 2. ثلاثة أنشطة 3. التقييم 4. نصيحة دعم المعلم."
                        audio_lang = 'ar'
                    
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    response = model.generate_content([prompt, image])
                    result_text = response.text
                    
                    st.success("🎉 تم الإعداد بنجاح!")
                    st.balloons()
                    
                    text_dir = "rtl" if audio_lang == 'ar' else "ltr"
                    text_align = "right" if audio_lang == 'ar' else "left"
                    
                    res_tab1, res_tab2 = st.tabs(["📑 الخطة المفصلة", "📥 الاستماع والتحميل"])
                    with res_tab1:
                        st.markdown(f"""<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #cbd5e1; direction: {text_dir}; text-align: {text_align};">""" + result_text + "</div>", unsafe_allow_html=True)
                    with res_tab2:
                        tts = gTTS(text=result_text, lang=audio_lang, slow=False)
                        audio_bytes = io.BytesIO()
                        tts.write_to_fp(audio_bytes)
                        audio_bytes.seek(0)
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        formatted_doc = create_formatted_doc(result_text, text_dir, text_align)
                        col_btn1.download_button("📄 تحميل Word", data=formatted_doc, file_name="lesson.doc", mime="application/msword", use_container_width=True)
                        col_btn2.download_button("📑 تحميل PDF/Web", data=formatted_doc, file_name="lesson.html", mime="text/html", use_container_width=True)
                        col_btn3.download_button("🎵 تحميل MP3", data=audio_bytes.getvalue(), file_name="audio.mp3", mime="audio/mp3", use_container_width=True)
                except Exception as e:
                    st.error("حدث خطأ، يرجى المحاولة مرة أخرى.")

# --- الصفحة الثانية والثالثة والرابعة (بدون تغيير) ---
with tab2:
    st.markdown("### 🎯 الرؤية والأهداف\n* توفير خطط تربوية فورية.\n* دعم المعلمين تقنياً ونفسياً.")
with tab3:
    st.markdown("### ⚖️ قانون الدمج (القرار 252)\nينظم قبول الطلاب ذوي الإعاقة البسيطة بمدارس التعليم العام وتوفير سبل التقييم المناسبة.")
with tab4:
    st.markdown("### 👤 عن المنصة\nتم التطوير بواسطة **فريق بصمة - أ. ولاء مقدام** لخدمة أبنائنا من ذوي الهمم.")

# ==========================================
# --- الصفحة الخامسة الجديدة: مكتبة بصمة ---
# ==========================================
with tab5:
    st.markdown("""
    <div style="background-color: #e0f2fe; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #0369a1; margin:0;">📚 مكتبة بصمة الشاملة لمصادر التعلم</h2>
        <p style="color: #0c4a6e; font-size: 18px;">مرجعك الشامل للوسائل، الألعاب، والمقالات التربوية المتخصصة</p>
    </div>
    """, unsafe_allow_html=True)

    lib_tab1, lib_tab2, lib_tab3, lib_tab4 = st.tabs(["📝 مقالات تربوية", "🎨 الوسائل التعليمية", "🎮 ألعاب تفاعلية", "📺 مكتبة الفيديو"])

    # 1. المقالات التربوية
    with lib_tab1:
        with st.expander("📌 استراتيجية التدريس المتمايز في فصول الدمج"):
            st.write("التدريس المتمايز هو عملية تكييف المناهج وطرق التدريس لتناسب الاختلافات بين المتعلمين. يشمل ذلك تعديل المحتوى، أو طريقة التقديم، أو بيئة التعلم.")
        with st.expander("📌 الدعم النفسي للطالب المدمج (كيف تبني ثقته بنفسه؟)"):
            st.write("يبدأ الدعم بدمج الطالب اجتماعياً، وتجنب عزله في المقاعد الخلفية، والاحتفاء بإنجازاته الصغيرة أمام زملائه لتعزيز صورته الذاتية.")

    # 2. الوسائل التعليمية الذكية
    with lib_tab2:
        st.markdown("### 🔍 اختر الإعاقة لعرض الوسائل المناسبة:")
        selected_disability = st.selectbox("نوع الإعاقة:", ["إعاقة بصرية", "إعاقة سمعية", "إعاقة ذهنية / بطء تعلم", "طيف التوحد"])
        
        if selected_disability == "إعاقة بصرية":
            st.info("💡 **أفضل الوسائل:**\n1. الكتب المطبوعة بطريقة برايل.\n2. المجسمات ثلاثية الأبعاد (3D).\n3. الخرائط البارزة.\n4. التسجيلات الصوتية للدروس.")
        elif selected_disability == "إعاقة سمعية":
            st.info("💡 **أفضل الوسائل:**\n1. البطاقات المصورة (Flashcards).\n2. الفيديوهات المترجمة بلغة الإشارة.\n3. الخرائط الذهنية الملونة.\n4. الإشارات الضوئية داخل الفصل.")
        elif selected_disability == "إعاقة ذهنية / بطء تعلم":
            st.info("💡 **أفضل الوسائل:**\n1. الألعاب التعليمية البسيطة (البازل).\n2. العدادات اليدوية والخرز.\n3. الصلصال لتشكيل الحروف والأرقام.\n4. القصص المصورة القصيرة.")
        elif selected_disability == "طيف التوحد":
            st.info("💡 **أفضل الوسائل:**\n1. الجداول البصرية اليومية (Visual Schedules).\n2. القصص الاجتماعية (Social Stories).\n3. أدوات تخفيف التوتر (Fidget toys).\n4. بيئة صفية خالية من المشتتات البصرية العالية.")

    # 3. الألعاب التفاعلية (دمج ألعاب تعليمية)
    with lib_tab3:
        st.markdown("### 🎲 ألعاب تنمية المهارات والتركيز")
        st.write("يمكن للمعلم استخدام هذه الألعاب الجاهزة لتحفيز الطلاب:")
        st.markdown("[🔗 اضغط هنا للذهاب إلى منصة الألعاب التعليمية المجانية (Wordwall)](https://wordwall.net/ar)")
        st.markdown("[🔗 اضغط هنا لمنصة LearningApps التفاعلية](https://learningapps.org/)")
        st.success("ملاحظة: يمكنكِ لاحقاً تزويدي بروابط الألعاب الخاصة بمدرستك لأقوم بدمجها مباشرة هنا!")

    # 4. مكتبة الفيديوهات التربوية
    with lib_tab4:
        st.markdown("### 📽️ فيديوهات توعوية وتدريبية")
        st.write("مثال لفيديو توعوي عن الدمج (يمكنك تغييره لاحقاً بأي فيديو خاص بالمدرسة):")
        # تم وضع رابط فيديو تعليمي عام كمثال، يمكنك تغييره متى شئتِ
        st.video("https://www.youtube.com/watch?v=FjHGZj2Ij_Q")
