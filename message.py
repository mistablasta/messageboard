import db

def insert_message(username, content):
    # Query to get the user_id from the users table based on username
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if not result:
        raise ValueError("User does not exist")  # Handle if user is not found

    user_id = result[0][0]  # Extract user_id

    # Now insert into messages using the user_id
    sql = "INSERT INTO messages (user_id, content) VALUES (?, ?)"
    return db.execute(sql, [user_id, content])

def get_all_messages():
    sql = """
    SELECT messages.id, users.username, messages.content, messages.timestamp 
    FROM messages 
    JOIN users ON messages.user_id = users.id 
    ORDER BY messages.timestamp DESC
    """
    return db.query(sql)

def search_messages(query):
    sql = "SELECT user_id, content, timestamp FROM messages WHERE content LIKE ? ORDER BY timestamp DESC"
    return db.query(sql, ["%" + query + "%"])

def get_message_by_id_and_user(message_id, user_id):
    sql = "SELECT id, content FROM messages WHERE id = ? AND user_id = ?"
    return db.query(sql, [message_id, user_id])

def update_message(message_id, user_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ? AND user_id = ?"
    return db.execute(sql, [content, message_id, user_id])

def delete_message(message_id, user_id):
    sql = "DELETE FROM messages WHERE id = ? AND user_id = ?"
    return db.execute(sql, [message_id, user_id])