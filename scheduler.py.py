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
        try:
            algiers_tz = pytz.timezone('Africa/Algiers')
            now = datetime.now(algiers_tz)
            today_str = now.strftime("%Y-%m-%d")
            
            # التحقق من عدم تكرار النشر
            if self.last_post_date == today_str:
                return
                
            st.info(f"🔄 جاري توليد مقال جديد ليوم {today_str}...")
            
            generator = BlogGenerator()
            post = generator.generate_daily_post()
            
            if post:
                post_id = save_post(
                    title=post['title'],
                    content=post['content'],
                    summary=post['summary'],
                    author=post['author'],
                    category=post['category'],
                    image_url=post['image_url']
                )
                
                if post_id:
                    self.last_post_date = today_str
                    st.success(f"✅ تم نشر مقال جديد: {post['title']}")
                    
                    # تحديث session state
                    if 'daily_post' in st.session_state:
                        st.session_state.daily_post = post
                    return True
            return False
            
        except Exception as e:
            st.error(f"خطأ في جدولة المقال: {str(e)}")
            return False
            
    def run_scheduler(self):
        """تشغيل المجدول"""
        algiers_tz = pytz.timezone('Africa/Algiers')
        
        while self.running:
            try:
                now = datetime.now(algiers_tz)
                # التحقق عند الساعة 6 مساءً (18:00)
                if now.hour == 18 and now.minute == 0 and now.second < 30:
                    self.generate_daily_post()
                    time.sleep(60)  # انتظر دقيقة كاملة
                time.sleep(30)  # تحقق كل 30 ثانية
            except Exception as e:
                time.sleep(60)
            
    def start(self):
        """بدء التشغيل"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()
            return True
        return False
        
    def stop(self):
        """إيقاف التشغيل"""
        self.running = False
        return True
