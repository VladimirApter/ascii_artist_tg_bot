import sqlite3


def create_table():
    conn = sqlite3.connect('data/ads_db.sql')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()


def register_user(user_id):
    conn = sqlite3.connect('data/ads_db.sql')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM ads WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("PRAGMA table_info(ads);")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns if column[1] != 'id']

        if column_names:
            placeholders = ', '.join(['0'] * len(column_names))
            cursor.execute(f"INSERT INTO ads (id, {', '.join(column_names)}) VALUES (?, {placeholders})", (user_id,))
        else:
            cursor.execute("INSERT INTO ads (id) VALUES (?)", (user_id,))

    conn.commit()
    conn.close()


def update_ads(ads):
    unique_ads = {ad.id: ad for ad in ads}.values()

    conn = sqlite3.connect('data/ads_db.sql')
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info(ads);")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    for ad in unique_ads:
        column_name = f'ad_{ad.id}'

        if column_name not in column_names:
            cursor.execute(f"ALTER TABLE ads ADD COLUMN {column_name} INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


def increment_user_ad_views(user_id, ad_id):
    conn = sqlite3.connect('data/ads_db.sql')
    cursor = conn.cursor()

    column_name = f'ad_{ad_id}'
    cursor.execute(f"UPDATE ads SET {column_name} = {column_name} + 1 WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()
