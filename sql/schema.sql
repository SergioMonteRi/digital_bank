CREATE TABLE IF NOT EXISTS individual (
    id TEXT PRIMARY KEY,
    monthly_income REAL,
    age INTEGER,
    full_name TEXT,
    phone TEXT,
    email TEXT,
    category TEXT,
    balance REAL
);

CREATE TABLE IF NOT EXISTS company (
    id TEXT PRIMARY KEY,
    monthly_revenue REAL,
    company_name TEXT,
    phone TEXT,
    email TEXT,
    category TEXT,
    balance REAL
);

CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    client_type TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    created_at TEXT NOT NULL
);