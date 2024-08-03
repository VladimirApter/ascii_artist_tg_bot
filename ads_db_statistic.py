import sqlite3


def get_total_ad_views(ad_id):
    conn = sqlite3.connect('ads_db.sql')
    cursor = conn.cursor()

    column_name = f'ad_{ad_id}'
    cursor.execute(f"SELECT SUM({column_name}) FROM ads")
    total_views = cursor.fetchone()[0]

    conn.close()
    return total_views if total_views is not None else 0


def get_user_ad_views(user_id, ad_id):
    conn = sqlite3.connect('ads_db.sql')
    cursor = conn.cursor()

    column_name = f'ad_{ad_id}'
    cursor.execute(f"SELECT {column_name} FROM ads WHERE id = ?", (user_id,))
    user_views = cursor.fetchone()

    conn.close()
    return user_views[0] if user_views is not None else 0


def get_average_ad_views(ad_id):
    conn = sqlite3.connect('ads_db.sql')
    cursor = conn.cursor()

    column_name = f'ad_{ad_id}'
    cursor.execute(f"SELECT AVG({column_name}) FROM ads")
    average_views = cursor.fetchone()[0]

    conn.close()
    return average_views if average_views is not None else 0
