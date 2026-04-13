import os
import streamlit as st
from groq import Groq
from datetime import datetime
import pytz

class BlogGenerator:
    def __init__(self):
        try:
            # محاولة الحصول على مفتاح API من secrets
            api_key = st.secrets.get("GROQ_API_KEY", None)
            if api_key:
                self.client = Groq(api_key=api_key)
            else:
                st.warning("⚠️ لم يتم العثور على مفتاح Groq API. سيتم استخدام محتوى تجريبي.")
                self.client = None
        except Exception as e:
            st.warning(f"⚠️ خطأ في تهيئة Groq: {str(e)}. سيتم استخدام محتوى تجريبي.")
            self.client = None
        
    def generate_daily_post(self):
        """توليد مقال يومي"""
        algiers_tz = pytz.timezone('Africa/Algiers')
        today = datetime.now(algiers_tz)
        today_str = today.strftime("%Y-%m-%d")
        
        # إذا لم يكن هناك عميل Groq، استخدم محتوى تجريبي
        if not self.client:
            return self.get_fallback_post(today_str)
        
        topics = [
            "صحة الفم والأسنان",
            "نصائح يومية للعناية بالأسنان", 
            "أحدث تقنيات طب الأسنان",
            "علاج مشاكل اللثة",
            "تبييض الأسنان بأمان",
            "تقويم الأسنان للكبار والصغار",
            "زراعة الأسنان خطوة بخطوة",
            "أهمية الفحص الدوري للأسنان"
        ]
        
        selected_topic = topics[today.day % len(topics)]
        
        prompt = f"""أنت خبير في طب الأسنان وصحة الفم. اكتب مقالاً طبياً باللغة العربية بتاريخ {today_str} حول: {selected_topic}

المطلوب:
- عنوان جذاب
- مقدمة شيقة (سطرين)
- 3-4 فقرات معلوماتية دقيقة
- نصائح عملية للقراء
- خاتمة مفيدة

استخدم هذا التنسيق بالضبط:
العنوان: [العنوان]
الملخص: [ملخص قصير]
المحتوى: [المقال الكامل]
الفئة: [أحد هذه الخيارات: صحة الفم، العناية اليومية، علاجات، تقنيات حديثة]
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت خبير في طب الأسنان. اكتب بالعربية الفصحى المبسطة."},
                    {"role": "user", "content": prompt}
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            
            # استخراج البيانات
            title = ""
            summary = ""
            main_content = ""
            category = "صحة الفم"
            
            for line in content.split('\n'):
                if line.startswith('العنوان:'):
                    title = line.replace('العنوان:', '').strip()
                elif line.startswith('الملخص:'):
                    summary = line.replace('الملخص:', '').strip()
                elif line.startswith('الفئة:'):
                    category = line.replace('الفئة:', '').strip()
                elif line.startswith('المحتوى:'):
                    main_content = line.replace('المحتوى:', '').strip()
                elif main_content:
                    main_content += "\n" + line
            
            # إذا لم يتم استخراج المحتوى بشكل صحيح
            if not title or not main_content:
                title = f"نصائح طبية ليوم {today_str}"
                summary = "تعرف على أهم المعلومات الطبية لصحة فمك وأسنانك"
                main_content = content
            
            images = [
                "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800",
                "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?w=800",
                "https://images.unsplash.com/photo-1609840114035-3c981b782dfe?w=800"
            ]
            
            return {
                'title': title,
                'summary': summary,
                'content': main_content,
                'category': category,
                'image_url': images[today.day % len(images)],
                'author': "د. دنيا (المحتوى المُنتج بواسطة الذكاء الاصطناعي)"
            }
            
        except Exception as e:
            st.error(f"خطأ في توليد المحتوى: {str(e)}")
            return self.get_fallback_post(today_str)
    
    def get_fallback_post(self, date_str):
        """محتوى تجريبي في حالة فشل الاتصال بـ Groq"""
        return {
            'title': f"نصائح مهمة لصحة الفم والأسنان - {date_str}",
            'summary': "تعرف على أهم النصائح اليومية للحفاظ على صحة أسنانك وفمك",
            'content': """الحفاظ على صحة الفم والأسنان ليس مجرد رفاهية، بل هو ضرورة صحية تؤثر على جودة حياتك بشكل عام.

**أهم النصائح اليومية:**

1. **التنظيف المنتظم**: احرص على تنظيف أسنانك مرتين يومياً على الأقل باستخدام معجون أسنان يحتوي على الفلورايد.

2. **استخدام الخيط الطبي**: لا تهمل استخدام خيط الأسنان يومياً لإزالة بقايا الطعام بين الأسنان.

3. **زيارة الطبيب بانتظام**: قم بزيارة طبيب الأسنان كل 6 أشهر للفحص والتنظيف الدوري.

4. **تجنب السكريات**: قلل من تناول الحلويات والمشروبات الغازية التي تسبب تسوس الأسنان.

تذكر أن الوقاية خير من العلاج، والعناية المبكرة بصحة فمك توفر عليك الكثير من الوقت والجهد والمال.""",
            'category': "صحة الفم",
            'image_url': "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800",
            'author': "د. دنيا (محتوى تعليمي)"
        }
