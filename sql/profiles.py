import db

def get_total_score(user_id):
    sql = """
    SELECT 
        SUM(CASE WHEN reaction_type = 'thumbs_up' THEN 1 ELSE 0 END) -
        SUM(CASE WHEN reaction_type = 'thumbs_down' THEN 1 ELSE 0 END) AS score
    FROM reactions
    JOIN messages ON reactions.message_id = messages.id
    WHERE messages.user_id = ?
    """
    result = db.query(sql, [user_id])
    return result[0]['score'] if result and result[0]['score'] is not None else 0

def get_message_count(user_id):
    sql = "SELECT COUNT(*) FROM messages WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def get_favorite_category(user_id):
    sql = """
    SELECT categories.name, COUNT(*) AS count
    FROM message_category
    JOIN categories ON message_category.category_id = categories.id
    JOIN messages ON message_category.message_id = messages.id
    WHERE messages.user_id = ?
    GROUP BY categories.name
    ORDER BY count DESC
    LIMIT 1
    """
    result = db.query(sql, [user_id])
    return result[0]['name'] if result else "None"