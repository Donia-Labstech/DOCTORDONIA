import streamlit as st
from datetime import datetime
import json
import os

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="عيادة د. دنيا لطب الأسنان",
    page_icon="🦷",
    layout="wide"
)

# ==================== بيانات وهمية للمقالات ====================
BLOG_POSTS = [
    {
        "id": 1,
        "title": "10 نصائح يومية للحفاظ على صحة فمك وأسنانك",
        "date": "2026-04-14",
        "content": """
        الحفاظ على صحة الفم والأسنان ليس مجرد رفاهية، بل هو ضرورة صحية تؤثر على جودة حياتك بشكل عام.

        **1. تنظيف الأسنان مرتين يومياً**
        احرص على تنظيف أسنانك صباحاً ومساءً باستخدام معجون أسنان يحتوي على الفلورايد لمدة دقيقتين على الأقل.

        **2. استخدام خيط الأسنان**
        لا تهمل استخدام خيط الأسنان يومياً لإزالة بقايا الطعام بين الأسنان التي لا تصل إليها الفرشاة.

        **3. تنظيف اللسان**
        تنظيف اللسان يزيل البكتيريا المسببة لرائحة الفم الكريهة ويحسن من صحة الفم العامة.

        **4. زيارة طبيب الأسنان بانتظام**
        قم بزيارة طبيب الأسنان كل 6 أشهر للفحص والتنظيف الدوري والكشف المبكر عن المشاكل.

        **5. تجنب السكريات**
        قلل من تناول الحلويات والمشروبات الغازية التي تسبب تسوس الأسنان وتآكل المينا.

        **6. شرب الماء بكثرة**
        الماء يساعد في غسل الفم من بقايا الطعام ويزيد من إنتاج اللعاب الذي يحمي الأسنان.

        **7. استخدام غسول الفم**
        غسول الفم المضاد للبكتيريا يساعد في قتل الجراثيم والحفاظ على نفس منعش.

        **8. تجنب التدخين**
        التدخين يسبب اصفرار الأسنان وأمراض اللثة وسرطان الفم.

        **9. تناول الأطعمة المفيدة**
        الأطعمة الغنية بالكالسيوم مثل الحليب والجبن تقوي الأسنان.

        **10. استبدال فرشاة الأسنان**
        استبدل فرشاة أسنانك كل 3-4 أشهر أو عندما تظهر علامات التآكل.

        تذكر أن الوقاية خير من العلاج، والعناية المبكرة بصحة فمك توفر عليك الكثير من الوقت والجهد والمال.
        """,
        "author": "د. دنيا",
        "category": "نصائح يومية"
    },
    {
        "id": 2,
        "title": "دليل شامل حول تبييض الأسنان",
        "date": "2026-04-13",
        "content": """
        تبييض الأسنان أصبح من أكثر الإجراءات التجميلية طلباً في طب الأسنان الحديث.

        **ما هو تبييض الأسنان؟**
        هو إجراء طبي يهدف إلى تفتيح لون الأسنان وإزالة التصبغات الناتجة عن الطعام والشراب والتدخين والتقدم في العمر.

        **أنواع تبييض الأسنان:**

        1. **التبييض في العيادة**: يتم في جلسة واحدة تستغرق حوالي ساعة، حيث يستخدم الطبيب مواد تبييض قوية مع ضوء خاص للحصول على نتائج فورية.

        2. **التبييض المنزلي**: يقوم الطبيب بصنع قوالب خاصة لأسنانك تستخدمها في المنزل مع مادة التبييض لمدة أسبوعين.

        3. **شرائط التبييض**: متوفرة في الصيدليات ولكن نتائجها أقل فعالية.

        **من هم المرشحون المناسبون؟**
        - الأشخاص ذوو الأسنان السليمة
        - من يعانون من تصبغات سطحية
        - غير المدخنين

        **متى لا ينصح بالتبييض؟**
        - الحوامل والمرضعات
        - من لديهم حساسية شديدة في الأسنان
        - من يعانون من تسوس نشط أو أمراض اللثة
        - الأطفال تحت 16 سنة

        **مدة النتائج:**
        تدوم نتائج التبييض من 6 أشهر إلى سنتين حسب العناية اليومية والتدخين وتناول المواد الملونة.

        **نصائح بعد التبييض:**
        - تجنب المشروبات الملونة (قهوة، شاي، كولا) لمدة 48 ساعة
        - لا تدخن لمدة أسبوع
        - استخدم معجون أسنان للحساسية إذا لزم الأمر

        استشر طبيب أسنانك لتحديد الطريقة المناسبة لحالتك.
        """,
        "author": "د. دنيا",
        "category": "علاجات تجميلية"
    },
    {
        "id": 3,
        "title": "تقويم الأسنان للكبار: هل لا يزال ممكناً؟",
        "date": "2026-04-12",
        "content": """
        يعتقد الكثيرون أن تقويم الأسنان مخصص للأطفال والمراهقين فقط، لكن الحقيقة مختلفة تماماً.

        **هل يمكن للكبار تركيب تقويم الأسنان؟**
        نعم بالتأكيد! يمكن للكبار في أي عمر تركيب تقويم الأسنان بشرط أن تكون اللثة والأسنان سليمة.

        **أنواع التقويم المناسبة للكبار:**

        1. **التقويم الشفاف (إنفيزلاين)**: 
        - غير مرئي تقريباً
        - يمكن إزالته أثناء الأكل والتنظيف
        - مناسب للحالات البسيطة والمتوسطة

        2. **التقويم الخزفي**: 
        - لون شفاف أو بلون الأسنان
        - أقل وضوحاً من التقويم المعدني

        3. **التقويم المعدني**: 
        - الأقوى والأسرع
        - الأقل تكلفة
        - مناسب للحالات المعقدة

        4. **التقويم اللساني**: 
        - يركب خلف الأسنان
        - غير مرئي تماماً
        - أغلى الأنواع

        **مدة العلاج للكبار:**
        تتراوح مدة التقويم للكبار بين 12-24 شهراً حسب تعقيد الحالة.

        **تحديات تقويم الأسنان للكبار:**
        - قد يستغرق وقتاً أطول من الأطفال
        - احتمالية الحاجة لخلع أسنان
        - قد يحتاج لارتداء المثبت لفترة أطول

        **فوائد تقويم الأسنان للكبار:**
        - تحسين المظهر والثقة بالنفس
        - تحسين عملية المضغ
        - تسهيل عملية تنظيف الأسنان
        - الوقاية من مشاكل اللثة والتسوس

        لا تتردد في استشارة طبيب التقويم في أي عمر. الابتسامة الجميلة تستحق الانتظار!
        """,
        "author": "د. دنيا",
        "category": "تقويم أسنان"
    }
]

# ==================== بيانات المواعيد ====================
if 'appointments' not in st.session_state:
    st.session_state.appointments = []

if 'consultations' not in st.session_state:
    st.session_state.consultations = []

# ==================== CSS للتجميل ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif;
    }
    
    .stApp {
        direction: rtl;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0d6efd, #9d4edd);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .service-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        transition: transform 0.3s;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #20c997, #0dcaf0);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    div.stButton > button {
        font-family: 'Tajawal', sans-serif;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #0d6efd, #9d4edd);
        color: white;
        border: none;
        transition: transform 0.3s;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .blog-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border-right: 4px solid #0d6efd;
    }
    
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== الهيدر ====================
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 2rem; margin:0;">🦷 عيادة د. دنيا لطب الأسنان</h1>
    <p style="font-size: 1rem; margin-top: 0.5rem;">رعاية فموية شاملة بمعايير عالمية في قلب الجزائر</p>
    <p style="font-size: 0.9rem;">✨ ابتسامتك الصحية هي أولويتنا ✨</p>
</div>
""", unsafe_allow_html=True)

# ==================== إنشاء التبويبات ====================
tabs = st.tabs(["🏠 الرئيسية", "🦷 خدماتنا", "📝 المدونة", "💻 العيادة الافتراضية", "📅 احجز موعدك", "👩‍⚕️ من نحن"])

# ==================== التبويب 1: الرئيسية ====================
with tabs[0]:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🌟 مرحباً بكم في عيادة د. دنيا")
        st.markdown("""
        نقدم في عيادة د. دنيا لطب الأسنان رعاية فموية شاملة باستخدام أحدث التقنيات 
        والتجهيزات الطبية، مع التركيز على راحة المريض.
        
        **✨ مميزات عيادتنا:**
        - ✅ أكثر من 10 سنوات خبرة
        - ✅ أحدث التقنيات الطبية
        - ✅ فريق طبي متخصص
        - ✅ بيئة مريحة وآمنة
        - ✅ أسعار تنافسية
        - ✅ تعقيم كامل
        """)
        
        # زر حجز سريع
        if st.button("📅 احجز موعدك الآن", use_container_width=True):
            st.markdown("### 📅 املأ بياناتك أدناه")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=500&h=400&fit=crop", 
                 caption="د. دنيا - استشارية طب الأسنان", use_container_width=True)
    
    # إحصائيات
    st.markdown("---")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown('<div class="stats-card"><h2 style="margin:0;">+5000</h2><p style="margin:0;">مريض راضٍ</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="stats-card"><h2 style="margin:0;">10+</h2><p style="margin:0;">سنوات خبرة</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="stats-card"><h2 style="margin:0;">98%</h2><p style="margin:0;">رضا المرضى</p></div>', unsafe_allow_html=True)
    with col_d:
        st.markdown('<div class="stats-card"><h2 style="margin:0;">24/7</h2><p style="margin:0;">دعم مستمر</p></div>', unsafe_allow_html=True)

# ==================== التبويب 2: خدماتنا ====================
with tabs[1]:
    st.markdown("## 🦷 خدماتنا المتخصصة")
    st.markdown("نقدم مجموعة شاملة من خدمات طب الأسنان بأحدث التقنيات")
    
    services = [
        {"icon": "🦷", "title": "تنظيف وفحص دوري", "desc": "فحص شامل وتنظيف احترافي لإزالة الجير والتصبغات", "price": "من 3000 دج"},
        {"icon": "✨", "title": "تبييض الأسنان", "desc": "تقنية تبييض متطورة وآمنة تعيد لأسنانك بياضها الناصع", "price": "من 15000 دج"},
        {"icon": "😁", "title": "تقويم الأسنان", "desc": "علاج مشاكل إطباق الأسنان باستخدام تقنيات تقويم حديثة", "price": "من 80000 دج"},
        {"icon": "🦷", "title": "زراعة الأسنان", "desc": "زراعة أسنان بتقنيات حديثة ونتائج طبيعية تدوم طويلاً", "price": "من 120000 دج"},
        {"icon": "🩺", "title": "علاج العصب", "desc": "علاج جذور الأسنان بدقة متناهية وبأقل قدر من الألم", "price": "من 8000 دج"},
        {"icon": "👶", "title": "طب أسنان الأطفال", "desc": "رعاية خاصة لأسنان الأطفال في بيئة مرحة وآمنة", "price": "من 2000 دج"},
        {"icon": "🦷", "title": "حشوات تجميلية", "desc": "حشوات بلون الأسنان بتقنيات حديثة", "price": "من 4000 دج"},
        {"icon": "👑", "title": "تيجان وجسور", "desc": "ترميم الأسنان المكسورة أو المفقودة", "price": "من 25000 دج"},
        {"icon": "😷", "title": "جراحة الفم", "desc": "خلع الأسنان المتضررة وجراحة اللثة", "price": "من 5000 دج"}
    ]
    
    for i in range(0, len(services), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(services):
                with cols[j]:
                    st.markdown(f"""
                    <div class="service-card">
                        <div style="font-size: 3rem;">{services[i+j]['icon']}</div>
                        <h3 style="font-size: 1.2rem;">{services[i+j]['title']}</h3>
                        <p style="color: #666; font-size: 0.9rem;">{services[i+j]['desc']}</p>
                        <p style="color: #0d6efd; font-weight: bold;">{services[i+j]['price']}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== التبويب 3: المدونة ====================
with tabs[2]:
    st.markdown("## 📝 المدونة العلمية")
    st.markdown("نصائح ومعلومات طبية حول صحة الفم والأسنان")
    
    # عرض المقالات
    for post in BLOG_POSTS:
        with st.container():
            st.markdown(f"""
            <div class="blog-card">
                <h3>📄 {post['title']}</h3>
                <p style="color: #666; font-size: 0.9rem;">
                    ✍️ {post['author']} | 📅 {post['date']} | 🏷️ {post['category']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📖 اقرأ المقال"):
                st.markdown(post['content'])
            
            st.markdown("---")

# ==================== التبويب 4: العيادة الافتراضية ====================
with tabs[3]:
    st.markdown("## 💻 العيادة الافتراضية")
    st.markdown("استشر د. دنيا من منزلك عبر الإنترنت")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 🎥 مميزات الاستشارة الافتراضية
        
        - **🎬 استشارة فيديو مباشرة** - تواصل مع الطبيب عبر مكالمة فيديو آمنة
        - **⏰ مواعيد مرنة** - اختر الوقت المناسب لك
        - **📋 وصفة طبية إلكترونية** - استلم وصفاتك الطبية عبر البريد
        - **💬 متابعة مستمرة** - استشارات متابعة بعد العلاج
        - **💰 أسعار مخفضة** - استشارات افتراضية بأسعار مناسبة
        - **🌍 متاحة لجميع المرضى** - داخل وخارج الجزائر
        """)
    
    with col2:
        st.markdown("""
        ### 📞 خطوات الحجز
        
        1. اختر الوقت المناسب من التقويم
        2. قم بتعبئة بياناتك الطبية
        3. ستصلك رسالة تأكيد برابط الاستشارة
        4. تواصل مع الطبيب في الوقت المحدد
        
        > **ملاحظة:** الاستشارة الافتراضية تكلف 2000 دج فقط
        """)
    
    st.markdown("---")
    st.markdown("### 📝 احجز استشارتك الافتراضية الآن")
    
    with st.form("virtual_form"):
        col1, col2 = st.columns(2)
        with col1:
            v_name = st.text_input("الاسم الكامل *")
            v_phone = st.text_input("رقم الهاتف *")
        with col2:
            v_email = st.text_input("البريد الإلكتروني")
            v_date = st.date_input("التاريخ المفضل *")
        
        v_time = st.selectbox("الوقت المفضل *", 
                             ["10:00 - 11:00", "11:00 - 12:00", "14:00 - 15:00", "15:00 - 16:00", "17:00 - 18:00"])
        v_symptoms = st.text_area("وصف سريع للمشكلة (اختياري)", height=100)
        
        submitted = st.form_submit_button("💻 احجز استشارتك الافتراضية", use_container_width=True)
        if submitted and v_name and v_phone:
            consultation = {
                "name": v_name,
                "phone": v_phone,
                "email": v_email,
                "date": str(v_date),
                "time": v_time,
                "symptoms": v_symptoms
            }
            st.session_state.consultations.append(consultation)
            st.success(f"✅ شكراً {v_name}! تم استلام طلبك بنجاح. سنقوم بالتواصل معك خلال 24 ساعة لتأكيد موعد الاستشارة.")

# ==================== التبويب 5: حجز موعد ====================
with tabs[4]:
    st.markdown("## 📅 احجز موعدك في العيادة")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("appointment_form"):
            a_name = st.text_input("الاسم الكامل *")
            a_phone = st.text_input("رقم الهاتف *")
            a_email = st.text_input("البريد الإلكتروني")
            
            a_service = st.selectbox("نوع الخدمة *", 
                                    ["استشارة أولية", "تنظيف وفحص", "تبييض الأسنان", 
                                     "تقويم الأسنان", "زراعة الأسنان", "علاج العصب", 
                                     "حشوات تجميلية", "تيجان وجسور", "جراحة الفم"])
            
            a_date = st.date_input("التاريخ المفضل *")
            a_time = st.selectbox("الوقت المفضل *", 
                                 ["09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", 
                                  "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"])
            
            a_notes = st.text_area("ملاحظات إضافية", height=80)
            
            submitted = st.form_submit_button("📅 احجز موعدك الآن", use_container_width=True)
            if submitted and a_name and a_phone and a_service:
                appointment = {
                    "name": a_name,
                    "phone": a_phone,
                    "email": a_email,
                    "service": a_service,
                    "date": str(a_date),
                    "time": a_time,
                    "notes": a_notes
                }
                st.session_state.appointments.append(appointment)
                st.success(f"✅ شكراً {a_name}! تم استلام طلب حجز موعدك بنجاح. سنتصل بك على الرقم {a_phone} لتأكيد الموعد.")
                st.balloons()
    
    with col2:
        st.markdown("""
        ### 🏥 معلومات العيادة
        
        **📍 العنوان:**
        بليدة، الجزائر
        
        **🕐 ساعات العمل:**
        - السبت - الخميس: 9 صباحاً - 8 مساءً
        - الجمعة: 10 صباحاً - 4 عصراً
        - الطوارئ: متاحة 24/7
        
        **📞 للاتصال:**
        - الهاتف: +213 555 12 34 56
        - واتساب: +213 555 12 34 56
        
        **✉️ البريد الإلكتروني:**
        info@drdunia.dz
        
        **📍 موقعنا:**
        بجوار مستشفى بليدة المركزي
        """)
        
        # عرض عدد المواعيد المؤكدة
        st.info(f"📊 عدد المواعيد المؤكدة اليوم: {len(st.session_state.appointments)}")

# ==================== التبويب 6: من نحن ====================
with tabs[5]:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1598256989800-fe5f95da9787?w=500&h=400&fit=crop", 
                 caption="عيادة د. دنيا لطب الأسنان - بيئة حديثة ومريحة", use_container_width=True)
    
    with col2:
        st.markdown("""
        ## 👩‍⚕️ د. دنيا
        
        د. دنيا هي طبيبة أسنان متخصصة حاصلة على:
        - شهادة الدكتوراه في طب الأسنان من جامعة الجزائر
        - دبلوم متخصص في زراعة الأسنان
        - شهادة في تقويم الأسنان التجميلي
        
        مع أكثر من **10 سنوات خبرة** في مجال طب الأسنان التجميلي والعلاجي.
        
        ### 🎯 رؤيتنا
        
        تقديم أفضل رعاية طب أسنان في بيئة مريحة وآمنة، باستخدام أحدث التقنيات والتجهيزات الطبية، 
        مع التركيز على راحة المريض وتجربته الإيجابية.
        
        ### 🌟 قيمنا
        
        - **الجودة:** نستخدم أحدث التقنيات والمواد المعتمدة عالمياً
        - **الشفافية:** نشرح للمريض كل خطوة قبل البدء بالعلاج
        - **الراحة:** نحرص على توفير تجربة مريحة خالية من التوتر
        - **التطوير:** نتابع أحدث المستجدات في عالم طب الأسنان
        """)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات عيادتنا")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🦷 مرضى سعداء", "+5000", "يزداد يومياً")
    with col2:
        st.metric("⭐ تقييم المرضى", "4.9/5", "ممتاز")
    with col3:
        st.metric("👩‍⚕️ سنوات خبرة", "10+", "متواصلة")
    with col4:
        st.metric("🏆 عمليات ناجحة", "+3000", "بنسبة نجاح 98%")
    
    st.markdown("---")
    st.markdown("### 🗣️ آراء المرضى")
    
    testimonials = [
        {"name": "أحمد ر.", "text": "د. دنيا محترفة جداً. تعاملت مع أسناني بخبرة عالية. أنصح بها بشدة.", "rating": "⭐⭐⭐⭐⭐"},
        {"name": "سارة م.", "text": "أجريت عملية تبييض الأسنان والنتائج رائعة. العيادة نظيفة والفريق محترم.", "rating": "⭐⭐⭐⭐⭐"},
        {"name": "محمد ل.", "text": "أفضل عيادة أسنان في بليدة. د. دنيا شرحت لي كل شيء بالتفصيل.", "rating": "⭐⭐⭐⭐⭐"}
    ]
    
    for test in testimonials:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <p style="font-weight: bold;">{test['name']}</p>
            <p>{test['text']}</p>
            <p style="color: #ffc107;">{test['rating']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== الفوتر ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #0d6efd, #9d4edd); border-radius: 20px; color: white;">
    <p style="margin: 0; font-size: 1rem;">© 2026 عيادة د. دنيا لطب الأسنان - جميع الحقوق محفوظة</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">بابتسامة صحية نصنع مستقبل أفضل | بليدة، الجزائر</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">
        📞 +213 555 12 34 56 | ✉️ info@drdunia.dz | 🕐 السبت - الخميس 9ص - 8م
    </p>
</div>
""", unsafe_allow_html=True)

# عرض رسالة ترحيب في الشريط الجانبي
with st.sidebar:
    st.markdown("## 🦷 د. دنيا لطب الأسنان")
    st.markdown("---")
    st.markdown("### 📞 للتواصل السريع")
    st.markdown("""
    - **هاتف:** 0555 12 34 56
    - **واتساب:** 0555 12 34 56
    - **بريد:** info@drdunia.dz
    """)
    st.markdown("---")
    st.markdown("### 🕐 ساعات العمل")
    st.markdown("""
    - **السبت - الخميس:** 9ص - 8م
    - **الجمعة:** 10ص - 4ع
    - **الطوارئ:** 24/7
    """)
    st.markdown("---")
    st.markdown("### 📍 موقعنا")
    st.markdown("بليدة، الجزائر")
    st.markdown("بجوار مستشفى بليدة المركزي")
    
    # عرض عدد الزوار
    if 'visitors' not in st.session_state:
        st.session_state.visitors = 0
    st.session_state.visitors += 1
    st.markdown("---")
    st.markdown(f"👥 زوار اليوم: {st.session_state.visitors}")
