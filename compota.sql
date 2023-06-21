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

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    user_id INTEGER,
    admin BOOLEAN NOT NULL,
    role TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexing roles table by project_id
CREATE INDEX IF NOT EXISTS idx_role_project_id ON roles (project_id);