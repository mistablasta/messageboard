CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE reactions (
    id INTEGER PRIMARY KEY,
    message_id INTEGER,
    user_id INTEGER,
    reaction_type TEXT CHECK(reaction_type IN ('thumbs_up', 'thumbs_down')),
    FOREIGN KEY (message_id) REFERENCES messages(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE (message_id, user_id)
);