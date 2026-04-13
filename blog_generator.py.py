import os
import streamlit as st
from groq import Groq
from datetime import datetime
import pytz

class BlogGenerator:
    def __init__(self):
        self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
    def generate_daily_post(self):
        """توليد مقال يومي باستخدام Groq"""
        algiers_tz = pytz.timezone('Africa/Algiers')
        today = datetime.now(algiers_tz).strftime("%Y-%m-%d")
        
        topics = [
            "صحة الفم والأسنان",
            "نصائح يومية للعناية بالأسنان",
            "أحدث تقنيات طب الأسنان",
            "علاج مشاكل اللثة",
            "تبييض الأسنان بأمان",
            "تقويم الأسنان للكبار والصغار",
            "زراعة الأسنان خطوة بخطوة",
            "أهمية الفحص الدوري للأسنان",
            "تسوس الأسنان أسبابه وعلاجه",
            "العناية بأسنان الأطفال"
        ]
        
        prompt = f"""أنت خبير في طب الأسنان وصحة الفم. قم بكتابة مقال طبي دقيق وهادف باللغة العربية بتاريخ {today} حول موضوع: {topics[today.day % len(topics)]}

المتطلبات:
- عنوان جذاب
- مقدمة شيقة
- محتوى علمي دقيق (3-4 فقرات)
- نصائح عملية للقراء
- خاتمة مفيدة
- كن مقنعاً ومفيداً للجمهور العام

قم بتنسيق المقال بهذا الهيكل:
العنوان: [العنوان هنا]
الملخص: [ملخص قصير 2-3 أسطر]
المحتوى: [المقال كاملاً]
الفئة: [صحة الفم، العناية اليومية، علاجات، تقنيات حديثة]
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت خبير في طب الأسنان وصحة الفم. اكتب محتوى دقيق ومفيد باللغة العربية الفصحى."},
                    {"role": "user", "content": prompt}
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # استخراج أجزاء المقال
            lines = content.split('\n')
            title = ""
            summary = ""
            main_content = ""
            category = "صحة الفم"
            
            for line in lines:
                if line.startswith('العنوان:'):
                    title = line.replace('العنوان:', '').strip()
                elif line.startswith('الملخص:'):
                    summary = line.replace('الملخص:', '').strip()
                elif line.startswith('الفئة:'):
                    category = line.replace('الفئة:', '').strip()
                elif line.startswith('المحتوى:'):
                    main_content = line.replace('المحتوى:', '').strip()
                else:
                    if main_content:
                        main_content += "\n" + line
            
            # صور افتراضية للمقالات
            images = [
                "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5",
                "https://images.unsplash.com/photo-1606811841689-23dfddce3e95",
                "https://images.unsplash.com/photo-1609840114035-3c981b782dfe",
                "https://images.unsplash.com/photo-1559839734-2b71ea197ec2"
            ]
            
            return {
                'title': title or f"نصائح طبية ليوم {today}",
                'summary': summary or "تعرف على أهم النصائح الطبية لصحة فمك وأسنانك",
                'content': main_content or content,
                'category': category,
                'image_url': images[today.day % len(images)] + "?w=800&h=500&fit=crop",
                'author': "د. دنيا (المحتوى المُنتج بواسطة الذكاء الاصطناعي)"
            }
            
        except Exception as e:
            st.error(f"خطأ في توليد المحتوى: {str(e)}")
            return None

    def review_and_improve_post(self, post_content):
        """مراجعة وتحسين المقال باستخدام الذكاء الاصطناعي"""
        prompt = f"""قم بمراجعة وتدقيق هذا المقال الطبي حول طب الأسنان. تأكد من:
1. الدقة العلمية
2. صحة المعلومات
3. تحسين اللغة والأسلوب
4. إضافة أي معلومات مفيدة منقوصة

المقال الأصلي:
{post_content}

قم بإرجاع النسخة المحسنة فقط من المقال مع إضافة قسم "📌 ملاحظة: تمت مراجعة هذا المقال من قبل الذكاء الاصطناعي للتأكد من دقته العلمية."
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت خبير طبي متخصص في مراجعة المحتوى الطبي لطب الأسنان."},
                    {"role": "user", "content": prompt}
                ],
                model="mixtral-8x7b-32768",
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"خطأ في مراجعة المحتوى: {str(e)}")
            return post_content