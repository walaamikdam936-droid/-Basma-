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

# 4. تقسيم المنصة 
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
                        prompt = f"أنت خبير تربوي مصري متخصص في التربية الخاصة والدمج التعليمي. حلل الدرس المرفق وقدم دليلاً لمعلم يدرس طالب في ({stage}) لمادة ({subject}) يعاني من ({disability})."
                        if additional_notes:
                            prompt += f"\nملاحظات المعلم: '{additional_notes}'. وظفها إلزامياً في إجابتك وصمم الأنشطة بناءً عليها."
                        prompt += "\nالنقاط الإلزامية: 1. طريقة التدريس المثلى 2. ثلاثة أنشطة تطبيقية ومبتكرة 3. طريقة التقييم المناسبة 4. نصيحة دعم المعلم (توجيه نفسي وتربوي)."
                        audio_lang = 'ar'
                    
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    response = model.generate_content([prompt, image])
                    result_text = response.text
                    
                    st.success("🎉 تم إعداد الدليل التربوي بنجاح!")
                    st.balloons()
                    
                    text_dir = "rtl" if audio_lang == 'ar' else "ltr"
                    text_align = "right" if audio_lang == 'ar' else "left"
                    
                    res_tab1, res_tab2 = st.tabs(["📑 الخطة المفصلة", "📥 الاستماع والتحميل"])
                    with res_tab1:
                        st.markdown(f"""<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #cbd5e1; direction: {text_dir}; text-align: {text_align}; line-height: 1.8;">""" + result_text + "</div>", unsafe_allow_html=True)
                    with res_tab2:
                        tts = gTTS(text=result_text, lang=audio_lang, slow=False)
                        audio_bytes = io.BytesIO()
                        tts.write_to_fp(audio_bytes)
                        audio_bytes.seek(0)
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        formatted_doc = create_formatted_doc(result_text, text_dir, text_align)
                        col_btn1.download_button("📄 تحميل Word منسق", data=formatted_doc, file_name="lesson_plan.doc", mime="application/msword", use_container_width=True)
                        col_btn2.download_button("📑 تحميل كـ PDF (عبر المتصفح)", data=formatted_doc, file_name="lesson_plan.html", mime="text/html", use_container_width=True)
                        col_btn3.download_button("🎵 تحميل الملف الصوتي MP3", data=audio_bytes.getvalue(), file_name="lesson_audio.mp3", mime="audio/mp3", use_container_width=True)
                except Exception as e:
                    st.error("حدث خطأ أثناء المعالجة، يرجى المحاولة مرة أخرى.")

# --- الصفحة الثانية والثالثة والرابعة ---
with tab2:
    st.markdown("### 🎯 الرؤية والأهداف\n* تحويل إعداد دروس فئات الدمج إلى عملية فورية وممتعة.\n* تمكين المعلم مهنياً ونفسياً باستخدام تكنولوجيا الذكاء الاصطناعي.")
with tab3:
    st.markdown("### ⚖️ ملخص قانون الدمج المصري (القرار الوزاري 252 لسنة 2017)\nينظم قبول الطلاب ذوي الإعاقة البسيطة بمدارس التعليم العام وتوفير مسارات تقييم عادلة تتناسب مع مهارات وقدرات كل طالب مدمج.")
with tab4:
    st.markdown("### 👥 عن المنصة\nتم التخطيط والتطوير والابتكار بواسطة **فريق بصمة - أ. ولاء مقدام** كجزء من تفعيل مبادرة وحدة التواصل ودعم المعلمين.")

# --- الصفحة الخامسة المحدثة: مكتبة بصمة الشاملة ---
with tab5:
    st.markdown("""
    <div style="background-color: #e0f2fe; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #0369a1; margin:0; font-family: 'Cairo', sans-serif;">📚 مكتبة بصمة الشاملة لمصادر التعلم</h2>
        <p style="color: #0c4a6e; font-size: 18px;">المقالات التربوية المكتملة، الوسائل المخصصة، والمواد المرئية لدعم دمج الفروق الفردية</p>
    </div>
    """, unsafe_allow_html=True)

    lib_tab1, lib_tab2, lib_tab3, lib_tab4 = st.tabs(["📝 مقالات تربوية مكتملة", "🎨 الوسائل التعليمية", "🎮 ألعاب تفاعلية", "📺 مكتبة الفيديو التوعوي"])

    # 1. المقالات التربوية المكتملة
    with lib_tab1:
        with st.expander("📌 المقال الأول: استراتيجية التدريس المتمايز داخل الفصول الدامجة (دليل شامل)"):
            st.markdown("""
            ### مفهوم التدريس المتمايز وكيفية تطبيقه عملياً:
            التدريس المتمايز ليس منهجاً فريداً، بل هو فلسفة تربوية تهدف إلى تكييف عناصر المنهج (المحتوى، العمليات، المخرجات، وبيئة التعلم) لتلبية الاحتياجات الفريدة والتباينات بين الطلاب داخل نفس الصف الدراسي.
            
            #### آليات التطبيق داخل فصول الدمج:
            1. **تمايز المحتوى (Content):** تقديم المادة التعليمية الواحدة بأشكال متعددة تناسب القدرات الاستيعابية. على سبيل المثال، يقرأ الطالب العادي النص من الكتاب، بينما يتم تقديم نفس المفهوم لطالب الدمج السمعي أو البصري عبر مجسمات ملموسة أو صور فلاشية ملوّنة.
            2. **تمايز العمليات (Process):** تعديل أسلوب الأنشطة ومهام التعلم؛ بحيث تدرج المهام من البساطة التامة إلى التركيب لتلائم الطلاب ذوي الإعاقة الذهنية البسيطة أو بطء التعلم، مع إعطائهم وقتاً إضافياً لإنجاز المهمة والتركيز على المهارات الأساسية للدرس دون تشتيت.
            3. **تمايز المخرجات (Products):** تنويع أساليب التقييم وقياس الفهم، فلا يُشترط التقييم الورقي التقليدي؛ بل يُسمح لطالب الدمج بالتعبير عن استيعابه بالرسم، أو الإشارة، أو النطق الشفهي، أو ترتيب المكعبات التوضيحية.
            """)
            
        with st.expander("📌 المقال الثاني: الدعم النفسي والاجتماعي لطلاب الدمج وآليات تقبل الآخر"):
            st.markdown("""
            ### بناء البيئة النفسية الآمنة لطلاب الدمج:
            الدمج الأكاديمي لا يكتمل دون دمج اجتماعي ونفسي سوي. يقع على عاتق معلم الفصل وقائد المدرسة مسؤولية كبرى في إزالة الحواجز النفسية وبناء بيئة خالية تماماً من التنمر أو العزل.
            
            #### آليات تعزيز التقبل والاحتواء بين الطلاب:
            1. **أسلوب التعلم بالأقران (Peer Tutoring):** إشراك الطلاب العاديين في مساعدة زملائهم من ذوي الهمم داخل مجموعات عمل صغيرة، مما ينمي لدى الطلاب العاديين مشاعر التعاطف والمسؤولية، ويزيل لدى طالب الدمج مشاعر العزلة أو النقص.
            2. **ورش التوعية والأنشطة المشتركة:** تنظيم فعاليات دورية بالمدرسة (مثل مسرح العرائس، أو الإذاعة المدرسية الموجهة) لشرح فكرة الاختلاف الإنساني، والتأكيد على أن التنوع هو سر تكامل المجتمع البشري، وأن لكل فرد فينا بصمته وقدراته الخاصة.
            3. **التعزيز الإيجابي العلني:** الاحتفاء الجماعي بأي نجاح أو تميز يحققه طالب الدمج أمام أقرانه داخل الفصل، مما يرفع من تقديره لذاته ويعزز مكانته الاجتماعية والتربوية وسط زملائه.
            """)

    # 2. الوسائل التعليمية
    with lib_tab2:
        st.markdown("### 🔍 اختر الفئة لعرض أفضل الوسائل التعليمية المخصصة:")
        selected_disability = st.selectbox("نوع الإعاقة الحالية:", ["إعاقة بصرية", "إعاقة سمعية", "إعاقة ذهنية / بطء تعلم", "طيف التوحد"])
        if selected_disability == "إعاقة بصرية":
            st.info("💡 **أفضل الوسائل:**\n1. مجسمات بارزة ثلاثية الأبعاد (3D Models).\n2. لوحات وخرائط جغرافية ملموسة.\n3. تسجيلات صوتية تفصيلية للمحتوى.")
        elif selected_disability == "إعاقة سمعية":
            st.info("💡 **أفضل الوسائل:**\n1. بطاقات تعليمية مصورة (Flashcards).\n2. خرائط ذهنية ملونة شديدة التباين البصري.\n3. قواميس إشارية متحركة.")
        elif selected_disability == "إعاقة ذهنية / بطء تعلم":
            st.info("💡 **أفضل الوسائل:**\n1. عدادات يدوية وخرز ملون لتبسيط الرياضيات.\n2. بازل خشبي لتجميع الكلمات والحروف.\n3. صلصال طبي لتشكيل الأرقام حسياً.")
        elif selected_disability == "طيف التوحد":
            st.info("💡 **أفضل الوسائل:**\n1. جداول بصرية يومية ثابتة لتنظيم المهام.\n2. قصص اجتماعية مصورة لتعديل السلوك.\n3. أدوات الاسترخاء والتركيز الحسي.")

    # 3. الألعاب التفاعلية
    with lib_tab3:
        st.markdown("### 🎲 منصات الألعاب التفاعلية المدمجة لتعزيز التركيز")
        st.write("يمكن الاستعانة بهذه المنصات العالمية المباشرة لتصميم ألعاب رقمية تفاعلية تناسب طلاب الدمج وتزيد من دافعيتهم للتعلم:")
        st.markdown("[🔗 اذهب الآن إلى منصة Wordwall الرقمية لتصميم ألعاب دمج تفاعلية](https://wordwall.net/ar)")
        st.markdown("[🔗 اذهب الآن إلى منصة LearningApps التعليمية للتمارين المصورة](https://learningapps.org/)")

    # 4. مكتبة الفيديو التوعوي (تم ربطه بفيديو واحد مركّز ومخصص لطلاب الدمج والتقبل)
    with lib_tab4:
        st.markdown("<h3 style='color: #0369a1;'>📽️ فيديو توعوي: تقبل الاختلاف ودمج أطفالنا من ذوي الهمم</h3>", unsafe_allow_html=True)
        st.write("يعرض هذا الفيديو أهمية تقبل الطلاب ذوي الهمم داخل البيئة المدرسية، وكيفية بناء جسور التعاطف والتواصل البناء والدمج الفعلي الحقيقي بين طلاب المدرسة.")
        # تم ربط مشغل الفيديو المدمج بفيديو توعوي عالي الجودة لتقبل أطفال الدمج والاختلاف
        st.video("https://www.youtube.com/watch?v=FjHGZj2Ij_Q")
