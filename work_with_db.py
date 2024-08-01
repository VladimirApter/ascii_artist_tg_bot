import sqlite3

import ads_config


def create_table():
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(50),
                        photo_count INTEGER,
                        video_count INTEGER,
                        first_time BOOLEAN,
                        media_between_ads_count INTEGER,
                        last_showed_ad_index INTEGER)''')
    conn.commit()
    conn.close()


def register_user(user_id, user_name):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (id, name, photo_count, video_count, first_time, media_between_ads_count, last_showed_ad_index) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user_id, user_name, 0, 0, True, 0, len(ads_config.ADS_BEARER.ads_group) - 1))
        conn.commit()
    conn.close()


def update_user_data(user_id, photo_count=0, video_count=0):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET photo_count = photo_count + ?, video_count = video_count + ?, first_time = ? WHERE id = ?",
                   (photo_count, video_count, False, user_id))
    conn.commit()
    conn.close()


def get_user_column_value(user_id, column_name):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column_name} FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None


def set_user_column_value(user_id, column_name, value):
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {column_name} = ? WHERE id = ?", (value, user_id))
    conn.commit()
    conn.close()


def print_users_table():
    conn = sqlite3.connect('users_data.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()


class BdTableColumns:
    first_time = 'first_time'
    media_between_ads_count = 'media_between_ads_count'
    last_showed_ad_index = 'last_showed_ad_index'
