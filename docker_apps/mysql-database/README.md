# Exercise 5 - MySQL database + persistence

Goal: run MySQL, create a database and a `users` table, insert/query data, then make data persistent.

## Run (no persistence)

```bash
docker run --rm -d \
  --name mysql-ex5 \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -p 3306:3306 \
  mysql:8
```

Connect:

```bash
docker exec -it mysql-ex5 mysql -uroot -prootpass
```

SQL to create + fill the table:

```sql
CREATE DATABASE IF NOT EXISTS abd;
USE abd;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  age INT,
  name VARCHAR(100) NOT NULL,
  revenue DECIMAL(10,2)
);

INSERT INTO users (age, name, revenue) VALUES
  (28, 'Alice Dupont', 45000.00),
  (35, 'Bob Martin', 62000.50),
  (42, 'Claire Dubois', 78500.00);

SELECT * FROM users;
```

Restart vs recreate:

```bash
docker stop mysql-ex5 && docker start mysql-ex5
```

The table is still there after a stop/start (same container). If you remove the container and create a new one, data is lost.

## Persist data (named volume)

1. Remove the old container (if running):

```bash
docker rm -f mysql-ex5
```

2. Run with a Docker volume for `/var/lib/mysql`:

```bash
docker volume create mysql_ex5_data

docker run -d \
  --name mysql-ex5 \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -p 3306:3306 \
  -v mysql-data-volume:/var/lib/mysql \
  mysql:8
```

Notes:

- Scripts in `/docker-entrypoint-initdb.d/` run only the first time the database is initialized (i.e., when the volume is empty).
- `create_table.sql` already creates DB/table and inserts rows.

Query:

```bash
docker exec -it mysql-ex5 mysql -uroot -prootpass -e "USE abd; SELECT * FROM users;"
```

## Cleanup

```bash
docker rm -f mysql-ex5
docker volume rm mysql_ex5_data
```
