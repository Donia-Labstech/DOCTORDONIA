import sqlite3
from datetime import datetime
import pytz

def init_db():
    conn = sqlite3.connect('blog_posts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  summary TEXT,
                  author TEXT,
                  date TEXT,
                  category TEXT,
                  image_url TEXT,
                  is_approved INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS scheduled_posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  post_id INTEGER,
                  scheduled_time TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def save_post(title, content, summary, author, category, image_url=""):
    conn = sqlite3.connect('blog_posts.db')
    c = conn.cursor()
    date = datetime.now(pytz.timezone('Africa/Algiers')).strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO posts (title, content, summary, author, date, category, image_url, is_approved) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (title, content, summary, author, date, category, image_url, 1))
    post_id = c.lastrowid
    conn.commit()
    conn.close()
    return post_id

def get_all_posts():
    conn = sqlite3.connect('blog_posts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY date DESC")
    posts = c.fetchall()
    conn.close()
    return posts

def get_post(post_id):
    conn = sqlite3.connect('blog_posts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    conn.close()
    return post

def delete_post(post_id):
    conn = sqlite3.connect('blog_posts.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()