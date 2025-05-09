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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE reactions (
    id INTEGER PRIMARY KEY,
    message_id INTEGER,
    user_id INTEGER,
    reaction_type TEXT CHECK(reaction_type IN ('thumbs_up', 'thumbs_down')),
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (message_id, user_id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE message_category (
    message_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (message_id, category_id)
);


INSERT INTO categories (name) VALUES ('Random');
INSERT INTO categories (name) VALUES ('Serious');
INSERT INTO categories (name) VALUES ('School');
INSERT INTO categories (name) VALUES ('Fashion');
INSERT INTO categories (name) VALUES ('TV');
INSERT INTO categories (name) VALUES ('Video Games');
INSERT INTO categories (name) VALUES ('Books');
INSERT INTO categories (name) VALUES ('News');

CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_reactions_message_id ON reactions(message_id);
CREATE INDEX idx_reactions_user_id ON reactions(user_id);
CREATE INDEX idx_msgcat_category_id ON message_category(category_id);
CREATE INDEX idx_msgcat_message_id ON message_category(message_id);