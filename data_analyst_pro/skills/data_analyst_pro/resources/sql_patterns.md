# Advanced SQL Patterns Reference

A comprehensive SQL reference covering advanced patterns beyond basic queries.
Compatible with PostgreSQL, MySQL, and SQLite (where supported).

---

## Window Functions

### Running Totals & Moving Averages
```sql
-- Running total
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total,
    AVG(amount) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as seven_day_avg,
    AVG(amount) OVER (
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as thirty_day_avg
FROM daily_metrics
ORDER BY date;
```

### Ranking Functions
```sql
-- Multiple ranking types compared
SELECT 
    department,
    employee_name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num,
    RANK()       OVER (PARTITION BY department ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dense_rank,
    NTILE(4)     OVER (PARTITION BY department ORDER BY salary DESC) as quartile,
    PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary) as percentile
FROM employees;
```

### Lead/Lag Analysis
```sql
-- Period-over-period comparison
SELECT 
    month,
    revenue,
    LAG(revenue, 1)  OVER (ORDER BY month) as prev_month,
    LAG(revenue, 12) OVER (ORDER BY month) as prev_year,
    ROUND((revenue - LAG(revenue, 1) OVER (ORDER BY month)) * 100.0 / 
        NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0), 2) as mom_growth,
    ROUND((revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0 / 
        NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2) as yoy_growth
FROM monthly_revenue;
```

### First/Last Value
```sql
-- First and last values per group
SELECT DISTINCT
    category,
    FIRST_VALUE(product) OVER (PARTITION BY category ORDER BY revenue DESC) as top_product,
    LAST_VALUE(product) OVER (
        PARTITION BY category ORDER BY revenue DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as bottom_product,
    FIRST_VALUE(revenue) OVER (PARTITION BY category ORDER BY revenue DESC) as max_revenue,
    LAST_VALUE(revenue) OVER (
        PARTITION BY category ORDER BY revenue DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as min_revenue
FROM products;
```

---

## Common Table Expressions (CTEs)

### Recursive CTEs (Hierarchical Data)
```sql
-- Organization hierarchy with depth tracking
WITH RECURSIVE org_tree AS (
    -- Base case: top-level managers
    SELECT 
        id, name, manager_id, 
        1 as depth,
        name::text as path,
        ARRAY[id] as breadcrumb
    FROM employees 
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT 
        e.id, e.name, e.manager_id,
        t.depth + 1,
        t.path || ' → ' || e.name,
        t.breadcrumb || e.id
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
    WHERE t.depth < 10  -- Safety limit
)
SELECT * FROM org_tree ORDER BY path;
```

### Date Series Generation
```sql
-- Fill gaps in time-series data (PostgreSQL)
WITH RECURSIVE dates AS (
    SELECT DATE '2024-01-01' as date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM dates WHERE date < DATE '2024-12-31'
)
SELECT 
    d.date,
    COALESCE(m.value, 0) as value,
    COALESCE(m.count, 0) as count
FROM dates d
LEFT JOIN daily_metrics m ON d.date = m.date
ORDER BY d.date;
```

### Multi-Step CTEs
```sql
-- Layered analysis with CTEs
WITH 
-- Step 1: Calculate user metrics
user_metrics AS (
    SELECT 
        user_id,
        COUNT(*) as order_count,
        SUM(amount) as total_spend,
        MIN(created_at) as first_order,
        MAX(created_at) as last_order
    FROM orders
    GROUP BY user_id
),
-- Step 2: Segment users
user_segments AS (
    SELECT *,
        CASE 
            WHEN total_spend > 10000 THEN 'VIP'
            WHEN total_spend > 1000 THEN 'Regular'
            WHEN order_count = 1 THEN 'One-time'
            ELSE 'Low-value'
        END as segment,
        EXTRACT(DAY FROM NOW() - last_order) as days_since_last
    FROM user_metrics
),
-- Step 3: Aggregate by segment
segment_summary AS (
    SELECT 
        segment,
        COUNT(*) as users,
        ROUND(AVG(total_spend), 2) as avg_spend,
        ROUND(AVG(order_count), 1) as avg_orders,
        ROUND(AVG(days_since_last), 0) as avg_recency
    FROM user_segments
    GROUP BY segment
)
SELECT * FROM segment_summary ORDER BY avg_spend DESC;
```

---

## Pivot / Unpivot Patterns

### Cross-Tab (PostgreSQL)
```sql
-- Pivot: rows to columns
SELECT *
FROM crosstab(
    'SELECT month, category, SUM(amount) 
     FROM sales 
     GROUP BY month, category 
     ORDER BY month, category',
    'SELECT DISTINCT category FROM sales ORDER BY category'
) AS ct (
    month date,
    electronics numeric,
    clothing numeric,
    food numeric
);
```

### Manual Pivot (Works Everywhere)
```sql
-- Universal pivot using CASE
SELECT 
    DATE_TRUNC('month', date) as month,
    SUM(CASE WHEN category = 'Electronics' THEN amount ELSE 0 END) as electronics,
    SUM(CASE WHEN category = 'Clothing' THEN amount ELSE 0 END) as clothing,
    SUM(CASE WHEN category = 'Food' THEN amount ELSE 0 END) as food,
    SUM(amount) as total
FROM sales
GROUP BY DATE_TRUNC('month', date)
ORDER BY month;
```

### Dynamic Grouping
```sql
-- Bucket continuous values into categories
SELECT 
    CASE 
        WHEN age < 18 THEN 'Under 18'
        WHEN age BETWEEN 18 AND 24 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        WHEN age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END as age_group,
    COUNT(*) as users,
    ROUND(AVG(spend), 2) as avg_spend,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct
FROM users
GROUP BY 1
ORDER BY MIN(age);
```

---

## Advanced Joins

### Self-Join (Finding Pairs)
```sql
-- Find products bought together
SELECT 
    a.product as product_a,
    b.product as product_b,
    COUNT(*) as frequency
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product < b.product
GROUP BY a.product, b.product
ORDER BY frequency DESC
LIMIT 20;
```

### Anti-Join (Missing Records)
```sql
-- Find users who never ordered
SELECT u.id, u.name, u.email, u.created_at
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- Alternative with NOT EXISTS
SELECT u.id, u.name, u.email
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

### Lateral Join (Correlated Subquery)
```sql
-- Top 3 products per category (PostgreSQL)
SELECT c.name as category, p.*
FROM categories c
CROSS JOIN LATERAL (
    SELECT product_name, revenue
    FROM products
    WHERE category_id = c.id
    ORDER BY revenue DESC
    LIMIT 3
) p;
```

---

## JSON Querying

### PostgreSQL JSONB
```sql
-- Extract JSON fields
SELECT 
    data->>'name' as name,
    data->>'email' as email,
    (data->'address'->>'city') as city,
    (data->>'age')::int as age
FROM users
WHERE data->>'status' = 'active'
AND (data->>'age')::int > 25;

-- Query JSON arrays
SELECT 
    id,
    jsonb_array_elements_text(data->'tags') as tag
FROM posts
WHERE data->'tags' @> '["featured"]';
```

### MySQL JSON
```sql
-- MySQL JSON functions
SELECT 
    JSON_EXTRACT(data, '$.name') as name,
    JSON_EXTRACT(data, '$.address.city') as city,
    JSON_LENGTH(data, '$.tags') as tag_count
FROM users
WHERE JSON_EXTRACT(data, '$.status') = '"active"';
```

---

## Performance Patterns

### Efficient Pagination
```sql
-- Keyset pagination (faster than OFFSET for large tables)
SELECT * FROM products
WHERE id > :last_seen_id  -- Use the last ID from previous page
ORDER BY id
LIMIT 20;

-- vs. traditional (slow for large offsets)
SELECT * FROM products
ORDER BY id
LIMIT 20 OFFSET 10000;  -- Must scan 10000 rows first
```

### Conditional Aggregation
```sql
-- Multiple metrics in one pass (avoids multiple table scans)
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') as completed,
    COUNT(*) FILTER (WHERE status = 'cancelled') as cancelled,
    SUM(amount) FILTER (WHERE status = 'completed') as revenue,
    AVG(amount) FILTER (WHERE status = 'completed') as avg_order,
    COUNT(DISTINCT user_id) as unique_customers,
    COUNT(*) FILTER (WHERE is_first_order) as new_customers
FROM orders
GROUP BY DATE(created_at)
ORDER BY date;
```

### Sampling
```sql
-- Random sample (PostgreSQL)
SELECT * FROM large_table
TABLESAMPLE BERNOULLI(1);  -- ~1% of rows

-- Deterministic sample
SELECT * FROM large_table
WHERE id % 100 = 0;  -- Every 100th row
```

---

## Data Quality Queries

### Find All Anomalies
```sql
-- Comprehensive data quality check
WITH quality AS (
    SELECT
        COUNT(*) as total_rows,
        COUNT(*) - COUNT(DISTINCT id) as duplicate_ids,
        SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) as null_emails,
        SUM(CASE WHEN email !~ '^[^@]+@[^@]+\.[^@]+$' THEN 1 ELSE 0 END) as invalid_emails,
        SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) as negative_amounts,
        SUM(CASE WHEN created_at > NOW() THEN 1 ELSE 0 END) as future_dates,
        SUM(CASE WHEN LENGTH(TRIM(name)) = 0 THEN 1 ELSE 0 END) as empty_names
    FROM users
)
SELECT 
    'Total Rows' as check, total_rows as value FROM quality
UNION ALL SELECT 'Duplicate IDs', duplicate_ids FROM quality
UNION ALL SELECT 'Null Emails', null_emails FROM quality
UNION ALL SELECT 'Invalid Emails', invalid_emails FROM quality
UNION ALL SELECT 'Negative Amounts', negative_amounts FROM quality
UNION ALL SELECT 'Future Dates', future_dates FROM quality
UNION ALL SELECT 'Empty Names', empty_names FROM quality;
```

### Schema Comparison
```sql
-- Compare column info across tables (PostgreSQL)
SELECT 
    table_name,
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name IN ('users', 'orders', 'products')
ORDER BY table_name, ordinal_position;
```

---

## Useful Shortcuts

### Quick Date Ranges
```sql
-- PostgreSQL
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'     -- Last 7 days
WHERE created_at >= CURRENT_DATE - INTERVAL '1 month'    -- Last month
WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE)    -- This month
WHERE created_at >= DATE_TRUNC('year', CURRENT_DATE)     -- This year
WHERE EXTRACT(DOW FROM created_at) IN (0, 6)             -- Weekends

-- MySQL
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
WHERE created_at >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
```

### NULL Handling
```sql
-- COALESCE chain
SELECT COALESCE(preferred_name, first_name, email, 'Unknown') as display_name
FROM users;

-- NULLIF (returns NULL if equal → prevents division by zero)
SELECT revenue / NULLIF(orders, 0) as avg_order_value
FROM daily_stats;
```

### String Patterns
```sql
-- Standard patterns
WHERE email LIKE '%@gmail.com'             -- Ends with
WHERE name ILIKE '%smith%'                 -- Case-insensitive (PostgreSQL)
WHERE phone ~ '^\+?[0-9]{10,15}$'         -- Regex (PostgreSQL)
WHERE REGEXP_LIKE(phone, '^[0-9]{10}$')    -- Regex (MySQL 8+)
```

---

*Advanced SQL Patterns — Part of the Data Analyst Pro skill*
