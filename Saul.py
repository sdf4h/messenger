import sqlite3
from datetime import datetime, timedelta

# Создание базы данных для хранения сообщений
def create_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, message TEXT, expiry_time TEXT)''')
    conn.commit()
    conn.close()

# Добавление сообщения в базу данных
def add_message(message_text, life_duration_minutes=1):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    expiry_time = datetime.now() + timedelta(minutes=life_duration_minutes)
    c.execute("INSERT INTO messages (message, expiry_time) VALUES (?, ?)",
              (message_text, expiry_time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# Проверка и удаление устаревших сообщений
def cleanup_expired_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("DELETE FROM messages WHERE expiry_time < ?", (current_time,))
    conn.commit()
    conn.close()
