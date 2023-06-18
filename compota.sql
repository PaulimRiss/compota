-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    createdAt TEXT NOT NULL
);
-- Indexing users table by username
CREATE INDEX IF NOT EXISTS idx_username ON users (username);

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    createdAt TEXT NOT NULL
);

-- Indexing projects table by title
CREATE INDEX IF NOT EXISTS idx_project_title ON projects (title);