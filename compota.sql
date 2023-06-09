-- Generate users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    phone_number TEXT,
    email TEXT
);
-- Indexing users table by username
CREATE INDEX IF NOT EXISTS idx_username ON users (username);