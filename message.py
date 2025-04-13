import db
import user

def insert_message(user_id, content):
    sql = "INSERT INTO messages (user_id, content) VALUES (?, ?)"
    db.execute(sql, [user_id, content])

def get_all_messages():
    sql = """
    SELECT messages.id, users.username, messages.content, messages.timestamp,
           COALESCE(SUM(CASE WHEN reactions.reaction_type = 'thumbs_up' THEN 1 ELSE 0 END), 0) as thumbs_up_count,
           COALESCE(SUM(CASE WHEN reactions.reaction_type = 'thumbs_down' THEN 1 ELSE 0 END), 0) as thumbs_down_count
    FROM messages
    JOIN users ON messages.user_id = users.id
    LEFT JOIN reactions ON messages.id = reactions.message_id
    GROUP BY messages.id
    ORDER BY messages.timestamp DESC
    """
    return db.query(sql)

def search_messages(query):
    sql = """
        SELECT messages.id, messages.content, messages.timestamp, users.username,
            COALESCE(SUM(CASE WHEN reactions.reaction_type = 'thumbs_up' THEN 1 ELSE 0 END), 0) AS thumbs_up_count,
            COALESCE(SUM(CASE WHEN reactions.reaction_type = 'thumbs_down' THEN 1 ELSE 0 END), 0) AS thumbs_down_count
        FROM messages
        JOIN users ON messages.user_id = users.id
        LEFT JOIN reactions ON messages.id = reactions.message_id
        WHERE messages.content LIKE ?
        GROUP BY messages.id
        ORDER BY messages.timestamp DESC
    """
    return db.query(sql, [f"%{query}%"])

def get_message_by_id_and_user(message_id, user_id):
    sql = "SELECT * FROM messages WHERE id = ? AND user_id = ?"
    return db.query(sql, [message_id, user_id])

def update_message(message_id, user_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ? AND user_id = ?"
    db.execute(sql, [content, message_id, user_id])

def delete_message(message_id, user_id):
    sql = "DELETE FROM reactions WHERE message_id = ?"
    db.execute(sql, [message_id])
    sql = "DELETE FROM messages WHERE id = ? AND user_id = ?"
    db.execute(sql, [message_id, user_id])

#Reactions

def add_reaction(message_id, user_id, reaction_type):
    existing_reaction = db.query("SELECT * FROM reactions WHERE message_id = ? AND user_id = ?", [message_id, user_id])

    if existing_reaction:
        db.execute("UPDATE reactions SET reaction_type = ? WHERE message_id = ? AND user_id = ?", [reaction_type, message_id, user_id])
    else:
        db.execute("INSERT INTO reactions (message_id, user_id, reaction_type) VALUES (?, ?, ?)", [message_id, user_id, reaction_type])

def get_reaction_counts(message_id):
    sql = """
    SELECT reaction_type, COUNT(*) 
    FROM reactions 
    WHERE message_id = ? 
    GROUP BY reaction_type
    """
    return db.query(sql, [message_id])