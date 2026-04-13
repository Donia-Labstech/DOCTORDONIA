import sqlite3
from datetime import datetime
import pytz
import streamlit as st

def init_db():
    """تهيئة قاعدة البيانات"""
    conn = sqlite3.connect('blog_posts.db')
    c = conn.cursor()
    
    # جدول المقالات
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  summary TEXT,
                  author TEXT,
                  date TEXT,
                  category TEXT,
                  image_url TEXT,
                  views INTEGER DEFAULT 0,
                  is_approved INTEGER DEFAULT 1)''')
    
    # جدول المواعيد
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  email TEXT,
                  service TEXT,
                  date TEXT,
                  time TEXT,
                  status TEXT DEFAULT 'pending',
                  created_at TEXT)''')
    
    # جدول الاستشارات الافتراضية
    c.execute('''CREATE TABLE IF NOT EXISTS virtual_consultations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  email TEXT,
                  preferred_date TEXT,
                  time_slot TEXT,
                  symptoms TEXT,
                  status TEXT DEFAULT 'pending',
                  created_at TEXT)''')
    
    conn.commit()
    conn.close()

def save_post(title, content, summary, author, category, image_url=""):
    """حفظ مقال جديد"""
    try:
        conn = sqlite3.connect('blog_posts.db')
        c = conn.cursor()
        algiers_tz = pytz.timezone('Africa/Algiers')
        date = datetime.now(algiers_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("""INSERT INTO posts 
                     (title, content, summary, author, date, category, image_url) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (title, content, summary, author, date, category, image_url))
        
        post_id = c.lastrowid
        conn.commit()
        conn.close()
        return post_id
    except Exception as e:
        st.error(f"خطأ في حفظ المقال: {str(e)}")
        return None

def get_all_posts():
    """الحصول على جميع المقالات"""
    try:
        conn = sqlite3.connect('blog_posts.db')
        c = conn.cursor()
        c.execute("SELECT * FROM posts ORDER BY date DESC")
        posts = c.fetchall()
        conn.close()
        return posts
    except Exception as e:
        return []

def get_post(post_id):
    """الحصول على مقال محدد"""
    try:
        conn = sqlite3.connect('blog_posts.db')
        c = conn.cursor()
        c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        post = c.fetchone()
        conn.close()
        return post
    except Exception as e:
        return None

def delete_post(post_id):
    """حذف مقال"""
    try:
        conn = sqlite3.connect('blog_posts.db')
        c = conn.cursor()
        c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def save_appointment(name, phone, email, service, date, time):
    """حفظ موعد جديد"""
    try:
        conn = sqlite3.connect('blog_posts.db')
        c = conn.cursor()
        algiers_tz = pytz.timezone('Africa/Algiers')
        created_at = datetime.now(algiers_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("""INSERT INTO appointments 
                     (name, phone, email, service, date, time, status, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (name, phone, email, service, date, time, 'pending', created_at))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الموعد: {str(e)}")
        return False

def save_virtual_consultation(name, phone, email, preferred_date, time_slot, symptoms):
    """حفظ استشارة افتراضية"""
    try:
        conn = sqlite3.connect('blog_posts.db')
        c = conn.cursor()
        algiers_tz = pytz.timezone('Africa/Algiers')
        created_at = datetime.now(algiers_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("""INSERT INTO virtual_consultations 
                     (name, phone, email, preferred_date, time_slot, symptoms, status, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (name, phone, email, preferred_date, time_slot, symptoms, 'pending', created_at))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الاستشارة: {str(e)}")
        return False
