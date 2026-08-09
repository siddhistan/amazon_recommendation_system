-- Amazon Reviews Analytics Database
-- Schema definition

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    product_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    profile_name TEXT,
    helpfulness_numerator INTEGER,
    helpfulness_denominator INTEGER,
    score INTEGER NOT NULL,
    review_time INTEGER,
    summary TEXT,
    review_text TEXT
);