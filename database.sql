CREATE TABLE urls (
    id bigint PRIMARY KEY,
    name varchar UNIQUE,
    created_at timestamp
);
