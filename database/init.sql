-- Runs once on first start of the Postgres container (empty data volume).
-- The backend also calls create_all() on startup, so this is a safe reference schema.
CREATE TABLE IF NOT EXISTS expenses (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(120)   NOT NULL,
    amount       NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    category     VARCHAR(50)    NOT NULL,
    expense_date DATE           NOT NULL DEFAULT CURRENT_DATE,
    created_at   TIMESTAMPTZ    NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_expenses_category ON expenses (category);
