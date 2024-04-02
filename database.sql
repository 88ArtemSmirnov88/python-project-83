CREATE TABLE IF NOT EXISTS urls (
    id SERIAL,
    name VARCHAR UNIQUE,
    created_at TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL,
    url_id INTEGER,
    status_code INTEGER,
    h1 VARCHAR,
    title VARCHAR,
    description VARCHAR,
    created_at TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (url_id) REFERENCES urls (id) ON DELETE CASCADE ON UPDATE CASCADE
);
