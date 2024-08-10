import sqlite3


def get_users_count():
    conn = sqlite3.connect('data/users_db.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_top_active_users():
    conn = sqlite3.connect('data/users_db.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT name, photo_count + video_count AS total_count FROM users ORDER BY total_count DESC LIMIT 5")
    results = cursor.fetchall()
    conn.close()
    return results


def get_average_counts():
    conn = sqlite3.connect('data/users_db.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(photo_count), AVG(video_count) FROM users")
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result
    else:
        return None


def get_first_20_users():
    conn = sqlite3.connect('data/users_db.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 20")
    results = cursor.fetchall()
    conn.close()
    return results


def get_user_by_name(name):
    conn = sqlite3.connect('data/users_db.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT id, photo_count, video_count FROM users WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result
