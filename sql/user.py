import db

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    return db.execute(sql, [username, password_hash])

def get_user_password_hash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0][0] if result else None

def get_user_id(username):
    result = db.query("SELECT id FROM users WHERE username = ?", [username])
    return result[0][0] if result else None

def get_user_id_by_username(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0][0] if result else None