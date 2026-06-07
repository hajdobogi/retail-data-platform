CREATE TABLE IF NOT EXISTS orders (
    order_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    region TEXT NOT NULL,
    category TEXT NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0),
    revenue NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    source TEXT NOT NULL DEFAULT 'simulated-pos'
);

CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders (created_at);
CREATE INDEX IF NOT EXISTS idx_orders_region ON orders (region);
CREATE INDEX IF NOT EXISTS idx_orders_category ON orders (category);

CREATE OR REPLACE VIEW hourly_sales AS
SELECT
    date_trunc('hour', created_at) AS hour,
    region,
    category,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    SUM(revenue) AS revenue
FROM orders
GROUP BY 1, 2, 3;

GRANT SELECT ON orders, hourly_sales TO retail_user;
