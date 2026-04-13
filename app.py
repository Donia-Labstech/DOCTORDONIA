import streamlit as st
from datetime import datetime
import pytz
from database import init_db, save_post, get_all_posts, delete_post, save_appointment, save_virtual_consultation
from blog_generator import BlogGenerator
from scheduler import BlogScheduler

# إعداد الصفحة
st.set_page_config(
    page_title="عيادة د. دنيا لطب الأسنان",
    page_icon="🦷",
    layout="wide"
)

# تهيئة قاعدة البيانات
init_db()

# تهيئة المجدول والتحقق من الموعد اليومي
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = BlogScheduler()
    st.session_state.last_check = None

# التحقق من الوقت كل مرة يتم فيها تحميل الصفحة
current_hour = datetime.now(pytz.timezone('Africa/Algiers')).hour
if current_hour >= 18 and st.session_state.get('last_check') != datetime.now().strftime("%Y-%m-%d"):
    st.session_state.scheduler.check_and_generate()
    st.session_state.last_check = datetime.now().strftime("%Y-%m-%d")

# CSS مخصص
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
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
    }
    
    .stats-card {
        background: linear-gradient(135deg, #20c997, #0dcaf0);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
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
    
    .blog-post {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
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

# الهيدر
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 2rem; margin:0;">🦷 عيادة د. دنيا لطب الأسنان</h1>
    <p style="font-size: 1rem; margin-top: 0.5rem;">رعاية فموية شاملة بمعايير عالمية في قلب الجزائر</p>
    <p style="font-size: 0.9rem;">✨ ابتسامتك الصحية هي أولويتنا ✨</p>
</div>
""", unsafe_allow_html=True)

# إنشاء التبويبات
tab_names = ["🏠 الرئيسية", "🦷 خدماتنا", "📝 المدونة الذكية", "💻 العيادة الافتراضية", "📅 احجز موعدك", "👩‍⚕️ من نحن"]
tabs = st.tabs(tab_names)

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
        """)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=500&h=400&fit=crop", 
                 caption="د. دنيا - استشارية طب الأسنان", use_container_width=True)
    
    # إحصائيات
    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class="stats-card">
            <h2 style="font-size: 1.8rem; margin:0;">+5000</h2>
            <p style="margin:0;">مريض راضٍ</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="stats-card">
            <h2 style="font-size: 1.8rem; margin:0;">10+</h2>
            <p style="margin:0;">سنوات خبرة</p>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class="stats-card">
            <h2 style="font-size: 1.8rem; margin:0;">24/7</h2>
            <p style="margin:0;">دعم مستمر</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== التبويب 2: خدماتنا ====================
with tabs[1]:
    st.markdown("## 🦷 خدماتنا المتخصصة")
    st.markdown("نقدم مجموعة شاملة من خدمات طب الأسنان بأحدث التقنيات")
    
    services = [
        {"icon": "🦷", "title": "تنظيف وفحص دوري", "desc": "فحص شامل وتنظيف احترافي لإزالة الجير والتصبغات"},
        {"icon": "✨", "title": "تبييض الأسنان", "desc": "تقنية تبييض متطورة وآمنة تعيد لأسنانك بياضها الناصع"},
        {"icon": "😁", "title": "تقويم الأسنان", "desc": "علاج مشاكل إطباق الأسنان باستخدام تقنيات تقويم حديثة"},
        {"icon": "🦷", "title": "زراعة الأسنان", "desc": "زراعة أسنان بتقنيات حديثة ونتائج طبيعية"},
        {"icon": "🩺", "title": "علاج العصب", "desc": "علاج جذور الأسنان بدقة متناهية"},
        {"icon": "👶", "title": "طب أسنان الأطفال", "desc": "رعاية خاصة لأسنان الأطفال في بيئة مرحة"}
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
                    </div>
                    """, unsafe_allow_html=True)

# ==================== التبويب 3: المدونة الذكية ====================
with tabs[2]:
    st.markdown("## 📝 المدونة الذكية")
    
    algiers_tz = pytz.timezone('Africa/Algiers')
    current_time = datetime.now(algiers_tz)
    st.info(f"🕐 يتم نشر مقال جديد يومياً الساعة 6:00 مساءً بتوقيت الجزائر | الوقت الحالي: {current_time.strftime('%H:%M:%S')}")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🤖 توليد مقال جديد", use_container_width=True):
            with st.spinner("جاري توليد مقال جديد..."):
                generator = BlogGenerator()
                post = generator.generate_daily_post()
                if post:
                    save_post(post['title'], post['content'], post['summary'], 
                             post['author'], post['category'], post['image_url'])
                    st.success("✅ تم نشر المقال بنجاح!")
                    st.rerun()
    
    # عرض المقالات
    posts = get_all_posts()
    
    if posts:
        for post in posts[:5]:
            with st.expander(f"📄 {post['title']} - {post['date']}"):
                st.markdown(f"**✍️ {post['author']}** | **🏷️ {post['category']}**")
                st.markdown("---")
                st.markdown(f"**📝 {post['summary']}**")
                st.markdown("---")
                st.markdown(post['content'])
                
                if st.button(f"🗑️ حذف", key=f"del_{post['id']}"):
                    delete_post(post['id'])
                    st.rerun()
    else:
        st.info("📭 لا توجد مقالات حالياً. اضغط على 'توليد مقال جديد' لبدء النشر.")

# ==================== التبويب 4: العيادة الافتراضية ====================
with tabs[3]:
    st.markdown("## 💻 العيادة الافتراضية")
    st.markdown("استشر د. دنيا من منزلك عبر الإنترنت")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 🎥 مميزات الاستشارة الافتراضية
        
        - **🎬 استشارة فيديو مباشرة** - تواصل مع الطبيب عبر مكالمة فيديو آمنة
        - **⏰ مواعيد مرنة** - اختر الوقت المناسب
        - **📋 وصفة طبية إلكترونية** - استلم وصفاتك عبر البريد
        - **💬 متابعة مستمرة** - استشارات متابعة بعد العلاج
        """)
    
    with col2:
        st.markdown("""
        ### 📞 خطوات الحجز
        
        1. اختر الوقت المناسب
        2. قم بتعبئة بياناتك
        3. ستصلك رسالة تأكيد
        4. تواصل مع الطبيب في الوقت المحدد
        """)
    
    st.markdown("---")
    st.markdown("### 📝 احجز استشارتك الافتراضية")
    
    with st.form("virtual_form"):
        col1, col2 = st.columns(2)
        with col1:
            v_name = st.text_input("الاسم الكامل *")
            v_phone = st.text_input("رقم الهاتف *")
        with col2:
            v_email = st.text_input("البريد الإلكتروني *")
            v_date = st.date_input("التاريخ المفضل *")
        
        v_time = st.selectbox("الوقت المفضل", ["10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "17:00-18:00"])
        v_symptoms = st.text_area("وصف المشكلة")
        
        submitted = st.form_submit_button("💻 احجز الاستشارة", use_container_width=True)
        if submitted and v_name and v_phone and v_email:
            if save_virtual_consultation(v_name, v_phone, v_email, str(v_date), v_time, v_symptoms):
                st.success(f"✅ شكراً {v_name}! تم استلام طلبك وسنقوم بالتواصل معك قريباً.")

# ==================== التبويب 5: حجز موعد ====================
with tabs[4]:
    st.markdown("## 📅 احجز موعدك")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("appointment_form"):
            a_name = st.text_input("الاسم الكامل *")
            a_phone = st.text_input("رقم الهاتف *")
            a_email = st.text_input("البريد الإلكتروني")
            a_service = st.selectbox("نوع الخدمة *", 
                                    ["استشارة أولية", "تنظيف وفحص", "تبييض الأسنان", 
                                     "تقويم الأسنان", "زراعة الأسنان", "علاج العصب"])
            a_date = st.date_input("التاريخ المفضل *")
            a_time = st.selectbox("الوقت المفضل", 
                                 ["09:00-10:00", "10:00-11:00", "11:00-12:00", 
                                  "14:00-15:00", "15:00-16:00", "16:00-17:00"])
            
            submitted = st.form_submit_button("📅 احجز الموعد", use_container_width=True)
            if submitted and a_name and a_phone and a_service:
                if save_appointment(a_name, a_phone, a_email, a_service, str(a_date), a_time):
                    st.success(f"✅ شكراً {a_name}! تم استلام طلب حجز موعدك بنجاح.")
    
    with col2:
        st.markdown("""
        ### 🏥 معلومات العيادة
        
        **📍 العنوان:** بليدة، الجزائر
        
        **🕐 ساعات العمل:**
        - السبت - الخميس: 9 صباحاً - 8 مساءً
        - الجمعة: 10 صباحاً - 4 عصراً
        
        **📞 للاتصال:** +213 XXX XX XX XX
        
        **✉️ البريد:** info@drdunya.dz
        """)

# ==================== التبويب 6: من نحن ====================
with tabs[5]:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1598256989800-fe5f95da9787?w=500&h=400&fit=crop", 
                 caption="عيادة د. دنيا", use_container_width=True)
    
    with col2:
        st.markdown("""
        ## 👩‍⚕️ د. دنيا
        
        د. دنيا هي طبيبة أسنان متخصصة حاصلة على شهادة الدكتوراه في طب الأسنان من جامعة الجزائر، 
        مع أكثر من 10 سنوات خبرة في مجال طب الأسنان التجميلي والعلاجي.
        
        ### 🎯 رؤيتنا
        
        تقديم أفضل رعاية طب أسنان في بيئة مريحة وآمنة، باستخدام أحدث التقنيات.
        
        ### 🌟 قيمنا
        
        - **الجودة:** نستخدم أحدث التقنيات المعتمدة عالمياً
        - **الشفافية:** نشرح للمريض كل خطوة قبل العلاج
        - **الراحة:** نحرص على توفير تجربة خالية من التوتر
        """)
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🦷 مرضى سعداء", "+5000")
    with col2:
        st.metric("⭐ تقييم المرضى", "4.9/5")
    with col3:
        st.metric("👩‍⚕️ سنوات خبرة", "10+")
    with col4:
        st.metric("🏆 عمليات ناجحة", "+3000")

# الفوتر
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0d6efd, #9d4edd); border-radius: 20px; color: white;">
    <p style="margin:0;">© 2026 عيادة د. دنيا لطب الأسنان - جميع الحقوق محفوظة</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">بابتسامة صحية نصنع مستقبل أفضل | بليدة، الجزائر</p>
</div>
""", unsafe_allow_html=True)
