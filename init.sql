
WITH RECURSIVE seq(x) AS (
  SELECT 1
  UNION ALL
  SELECT x+1 FROM seq WHERE x < 1000000
)
INSERT INTO users (username, password_hash)
SELECT 
  'user' || x,
  'hash_for_' || x
FROM seq;


WITH RECURSIVE seq(x) AS (
  SELECT 1
  UNION ALL
  SELECT x+1 FROM seq WHERE x < 1000000
)
INSERT INTO messages (user_id, content, timestamp)
SELECT
  abs(random()) % 1000000 + 1,                         
  'This is dummy message #' || x,
  datetime('now', '-' || abs(random()) % 365 || ' days')  
FROM seq;


WITH RECURSIVE seq(x) AS (
  SELECT 1
  UNION ALL
  SELECT x+1 FROM seq WHERE x < 1000000
)
INSERT OR IGNORE INTO reactions (message_id, user_id, reaction_type)
SELECT
  abs(random()) % 1000000 + 1,              
  abs(random()) % 1000000 + 1,              
  CASE WHEN abs(random()) % 2 = 0 THEN
    'thumbs_up' ELSE 'thumbs_down' END
FROM seq;


WITH RECURSIVE seq(x) AS (
  SELECT 1
  UNION ALL
  SELECT x+1 FROM seq WHERE x < 1000000
)
INSERT OR IGNORE INTO message_category (message_id, category_id)
SELECT
  abs(random()) % 1000000 + 1,
  abs(random()) % (SELECT COUNT(*) FROM categories) + 1
FROM seq;