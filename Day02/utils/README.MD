
### commands

```bash
# requirement : make execd (if psql not installed in your machine)
psql -U bfaure -d piscineds -h localhost -W
```

### Generate .env

```bash
cat > .env <<EOF
POSTGRES_DB=piscineds
POSTGRES_USER=${USER}
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_HOST=localhost
EOF
```

### SQL Test psql connection

```bash
CREATE TABLE users_test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
);


INSERT INTO users_test (name, age) VALUES ('Alice', 25);
INSERT INTO users_test (name, age) VALUES ('Bob', 30);
INSERT INTO users_test (name, age) VALUES ('Charlie', 28);


SELECT * FROM users_test;
```

```bash
# Log option
SHOW log_statement;

# Display all columns
SELECT * FROM data_2022_oct;
```

```bash
# Display column name and types
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'data_2022_oct';

# count rows
SELECT COUNT(*) FROM data_2022_oct;
```

```bash
# Display column name 
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'data_2023_jan';

# Count rows
SELECT COUNT(*) 
FROM data_2023_jan;
```

```bash
# JOIN CUSTOMER
SELECT 
    (SELECT COUNT(*) FROM data_2022_oct) AS sum1,
    (SELECT COUNT(*) FROM data_2022_nov) AS sum2,
    (SELECT COUNT(*) FROM data_2022_dec) AS sum3,
    (SELECT COUNT(*) FROM data_2023_jan) AS sum4,
    (
        (SELECT COUNT(*) FROM data_2022_oct) +
        (SELECT COUNT(*) FROM data_2022_nov) +
        (SELECT COUNT(*) FROM data_2022_dec) +
        (SELECT COUNT(*) FROM data_2023_jan)
    ) AS total_rows,
    (SELECT COUNT(*) FROM customers) AS customers_count;
```

```bash
# Display 100 row ordered
SELECT * FROM items
ORDER BY product_id ASC
LIMIT 100;

# Display rows with non-empty 'category_code' column
SELECT * FROM items_clean
WHERE category_code IS NOT NULL AND category_code <> '';
```

```bash
# Count rows for each 'event_type' enum
SELECT event_type, COUNT(*)
FROM customers
GROUP BY event_type
ORDER BY COUNT(*) DESC;
```
