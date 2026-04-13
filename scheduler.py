import streamlit as st
from datetime import datetime
import pytz
from blog_generator import BlogGenerator
from database import save_post

class BlogScheduler:
    def __init__(self):
        self.last_post_date = None
        
    def generate_daily_post(self):
        """توليد ونشر مقال يومي"""
        try:
            algiers_tz = pytz.timezone('Africa/Algiers')
            now = datetime.now(algiers_tz)
            today_str = now.strftime("%Y-%m-%d")
            
            # التحقق من عدم تكرار النشر
            if self.last_post_date == today_str:
                return False
                
            # التحقق إذا كانت الساعة 6 مساءً أو بعدها
            if now.hour >= 18:
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
                        
                        if 'daily_post' in st.session_state:
                            st.session_state.daily_post = post
                        return True
            return False
            
        except Exception as e:
            st.error(f"خطأ في جدولة المقال: {str(e)}")
            return False
    
    def check_and_generate(self):
        """التحقق من الوقت وتوليد المحتوى إذا لزم الأمر"""
        return self.generate_daily_post()
