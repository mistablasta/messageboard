import db

def insert_message(user_id, content, categories):
    sql = "INSERT INTO messages (user_id, content) VALUES (?, ?)"
    db.execute(sql, [user_id, content])
    message_id = db.last_insert_id()
    
    sql = "INSERT INTO message_category (message_id, category_id) VALUES (?, ?)"
    for category_id in categories:
        db.execute(sql, [message_id, category_id])

def get_messages_by_user(user_id):
    sql = """
    SELECT 
        messages.id, 
        users.username, 
        messages.content, 
        messages.timestamp,
        (SELECT COUNT(*) FROM reactions 
         WHERE reactions.message_id = messages.id 
         AND reactions.reaction_type = 'thumbs_up') AS thumbs_up_count,
        (SELECT COUNT(*) FROM reactions 
         WHERE reactions.message_id = messages.id 
         AND reactions.reaction_type = 'thumbs_down') AS thumbs_down_count,
        (SELECT GROUP_CONCAT(DISTINCT categories.name) 
         FROM message_category
         JOIN categories ON message_category.category_id = categories.id
         WHERE message_category.message_id = messages.id) as categories
    FROM messages
    JOIN users ON messages.user_id = users.id
    WHERE users.id = ?
    ORDER BY messages.timestamp DESC
    """
    return db.query(sql, [user_id])

def get_all_messages():
    sql = """
    SELECT 
        messages.id, 
        users.username, 
        messages.content, 
        messages.timestamp,
        (SELECT COUNT(*) FROM reactions 
         WHERE reactions.message_id = messages.id 
         AND reactions.reaction_type = 'thumbs_up') AS thumbs_up_count,
        (SELECT COUNT(*) FROM reactions 
         WHERE reactions.message_id = messages.id 
         AND reactions.reaction_type = 'thumbs_down') AS thumbs_down_count,
        (SELECT GROUP_CONCAT(DISTINCT categories.name) 
         FROM message_category
         JOIN categories ON message_category.category_id = categories.id
         WHERE message_category.message_id = messages.id) as categories
    FROM messages
    JOIN users ON messages.user_id = users.id
    ORDER BY messages.timestamp DESC
    """
    return db.query(sql)

def search_messages(query):
    sql = """
    SELECT 
        messages.id, 
        users.username, 
        messages.content, 
        messages.timestamp,
        (SELECT COUNT(*) FROM reactions 
         WHERE reactions.message_id = messages.id 
         AND reactions.reaction_type = 'thumbs_up') AS thumbs_up_count,
        (SELECT COUNT(*) FROM reactions 
         WHERE reactions.message_id = messages.id 
         AND reactions.reaction_type = 'thumbs_down') AS thumbs_down_count,
        (SELECT GROUP_CONCAT(DISTINCT categories.name) 
         FROM message_category
         JOIN categories ON message_category.category_id = categories.id
         WHERE message_category.message_id = messages.id) as categories
    FROM messages
    JOIN users ON messages.user_id = users.id
    WHERE messages.content LIKE ? 
       OR EXISTS (
           SELECT 1 FROM message_category
           JOIN categories ON message_category.category_id = categories.id
           WHERE message_category.message_id = messages.id
           AND categories.name LIKE ?
       )
    ORDER BY messages.timestamp DESC
    """
    return db.query(sql, [f"%{query}%", f"%{query}%"])

def get_message_by_id_and_user(message_id, user_id):
    sql = "SELECT * FROM messages WHERE id = ? AND user_id = ?"
    return db.query(sql, [message_id, user_id])

def update_message(message_id, user_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ? AND user_id = ?"
    db.execute(sql, [content, message_id, user_id])

def delete_message(message_id, user_id):
    sql = "DELETE FROM message_category WHERE message_id = ?"
    db.execute(sql, [message_id])
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