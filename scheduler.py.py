import threading
import time
from datetime import datetime
import pytz
import streamlit as st
from blog_generator import BlogGenerator
from database import save_post

class BlogScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_post_date = None
        
    def generate_daily_post(self):
        """توليد ونشر مقال يومي"""
        algiers_tz = pytz.timezone('Africa/Algiers')
        now = datetime.now(algiers_tz)
        today_str = now.strftime("%Y-%m-%d")
        
        # التحقق من عدم نشر مقال اليوم مسبقاً
        if self.last_post_date == today_str:
            return
            
        st.success(f"🔄 جاري توليد مقال جديد ليوم {today_str} الساعة {now.strftime('%H:%M')}...")
        
        generator = BlogGenerator()
        post = generator.generate_daily_post()
        
        if post:
            # حفظ المقال في قاعدة البيانات
            post_id = save_post(
                title=post['title'],
                content=post['content'],
                summary=post['summary'],
                author=post['author'],
                category=post['category'],
                image_url=post['image_url']
            )
            
            self.last_post_date = today_str
            st.success(f"✅ تم نشر مقال جديد بنجاح: {post['title']}")
            
            # إضافة إلى session state لتحديث الواجهة
            if 'daily_post' in st.session_state:
                st.session_state.daily_post = post
                
    def run_scheduler(self):
        """تشغيل المجدول لفحص الوقت كل دقيقة"""
        algiers_tz = pytz.timezone('Africa/Algiers')
        
        while self.running:
            now = datetime.now(algiers_tz)
            # التحقق إذا كانت الساعة 6 مساءً (18:00)
            if now.hour == 18 and now.minute == 0:
                self.generate_daily_post()
                # الانتظار لمدة 60 ثانية لتجنب التكرار
                time.sleep(60)
            time.sleep(30)  # التحقق كل 30 ثانية
            
    def start(self):
        """بدء تشغيل المجدول"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()
            return True
        return False
        
    def stop(self):
        """إيقاف المجدول"""
        self.running = False
        return True