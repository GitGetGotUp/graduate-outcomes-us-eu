-- sql/schema.sql
CREATE TABLE IF NOT EXISTS stg_bls_unemp (
    series_id TEXT,
    year      INT,
    period    TEXT,
    value     NUMERIC,
    footnotes TEXT,
    date      DATE
);
