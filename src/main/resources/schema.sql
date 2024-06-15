CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    role INTEGER DEFAULT 0 NOT NULL,
    state INTEGER DEFAULT 0 NOT NULL,
    request_time TEXT DEFAULT NULL,
    CHECK (role >= -1 AND role <= 2)  -- -1: Banned, 0: Unauthorized User, 1: Normal User, 2: Admin
);
