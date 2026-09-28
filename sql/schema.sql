CREATE TABLE IF NOT EXISTS individual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_income REAL,
    age INTEGER,
    full_name TEXT,
    phone TEXT,
    email TEXT,
    category TEXT,
    balance REAL
);

CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_revenue REAL,
    company_name TEXT,
    phone TEXT,
    email TEXT,
    category TEXT,
    balance REAL
);