import sqlite3


def create_table():
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(50),
                        photo_count INTEGER,
                        video_count INTEGER,
                        first_time BOOLEAN)''')
    conn.commit()
    conn.close()


def register_user(user_id, user_name):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (id, name, photo_count, video_count, first_time) VALUES (?, ?, ?, ?, ?)",
                       (user_id, user_name, 0, 0, True))
        conn.commit()
    conn.close()


def update_user_data(user_id, photo_count=0, video_count=0, first_time=False):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET photo_count = photo_count + ?, video_count = video_count + ?, first_time = ? WHERE id = ?",
                   (photo_count, video_count, first_time, user_id))
    conn.commit()
    conn.close()


def is_user_first_time(user_id):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT first_time FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None


def print_users_table():
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
