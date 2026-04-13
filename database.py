import streamlit as st
from datetime import datetime
import pytz
import json
import os

# استخدام JSON file بدلاً من SQLite لتجنب مشاكل التثبيت
DATA_FILE = 'blog_posts.json'
APPOINTMENTS_FILE = 'appointments.json'
CONSULTATIONS_FILE = 'consultations.json'

def load_data(filename, default):
    """تحميل البيانات من ملف JSON"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default

def save_data(filename, data):
    """حفظ البيانات في ملف JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"خطأ في الحفظ: {str(e)}")
        return False

def init_db():
    """تهيئة قاعدة البيانات (إنشاء الملفات إذا لم توجد)"""
    if not os.path.exists(DATA_FILE):
        save_data(DATA_FILE, [])
    if not os.path.exists(APPOINTMENTS_FILE):
        save_data(APPOINTMENTS_FILE, [])
    if not os.path.exists(CONSULTATIONS_FILE):
        save_data(CONSULTATIONS_FILE, [])
    return True

def save_post(title, content, summary, author, category, image_url=""):
    """حفظ مقال جديد"""
    try:
        posts = load_data(DATA_FILE, [])
        algiers_tz = pytz.timezone('Africa/Algiers')
        
        post = {
            'id': len(posts) + 1,
            'title': title,
            'content': content,
            'summary': summary,
            'author': author,
            'date': datetime.now(algiers_tz).strftime("%Y-%m-%d %H:%M:%S"),
            'category': category,
            'image_url': image_url,
            'views': 0
        }
        
        posts.insert(0, post)  # إضافة في البداية
        save_data(DATA_FILE, posts)
        return post['id']
    except Exception as e:
        st.error(f"خطأ في حفظ المقال: {str(e)}")
        return None

def get_all_posts():
    """الحصول على جميع المقالات"""
    return load_data(DATA_FILE, [])

def delete_post(post_id):
    """حذف مقال"""
    try:
        posts = load_data(DATA_FILE, [])
        posts = [p for p in posts if p['id'] != post_id]
        save_data(DATA_FILE, posts)
        return True
    except:
        return False

def save_appointment(name, phone, email, service, date, time):
    """حفظ موعد جديد"""
    try:
        appointments = load_data(APPOINTMENTS_FILE, [])
        algiers_tz = pytz.timezone('Africa/Algiers')
        
        appointment = {
            'id': len(appointments) + 1,
            'name': name,
            'phone': phone,
            'email': email,
            'service': service,
            'date': date,
            'time': time,
            'status': 'pending',
            'created_at': datetime.now(algiers_tz).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        appointments.append(appointment)
        save_data(APPOINTMENTS_FILE, appointments)
        return True
    except:
        return False

def save_virtual_consultation(name, phone, email, preferred_date, time_slot, symptoms):
    """حفظ استشارة افتراضية"""
    try:
        consultations = load_data(CONSULTATIONS_FILE, [])
        algiers_tz = pytz.timezone('Africa/Algiers')
        
        consultation = {
            'id': len(consultations) + 1,
            'name': name,
            'phone': phone,
            'email': email,
            'preferred_date': preferred_date,
            'time_slot': time_slot,
            'symptoms': symptoms,
            'status': 'pending',
            'created_at': datetime.now(algiers_tz).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        consultations.append(consultation)
        save_data(CONSULTATIONS_FILE, consultations)
        return True
    except:
        return False
