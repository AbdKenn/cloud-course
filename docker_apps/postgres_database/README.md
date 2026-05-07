# Exercise 6 - Postgres database + persistence

Goal: run Postgres, create a database and a `users` table, insert/query data, then make data persistent.

## Run (no persistence)

```bash
docker run --rm -d \
  --name pg-ex6 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -p 5432:5432 \
  postgres:15
```

Connect with `psql` inside the container:

```bash
docker exec -it pg-ex6 psql -U admin
```

SQL to create + fill the table:

```sql
CREATE DATABASE abd;
\c abd

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  age INT,
  name TEXT NOT NULL,
  revenue NUMERIC(10,2)
);

INSERT INTO users (age, name, revenue) VALUES
  (28, 'Alice Dupont', 45000.00),
  (35, 'Bob Martin', 62000.50),
  (42, 'Claire Dubois', 78500.00);

SELECT * FROM users;
```

Restart vs recreate:

```bash
docker stop pg-ex6 && docker start pg-ex6
```

The table is still there after a stop/start (same container). If you remove the container and create a new one, data is lost.

## Persist data (named volume)

```bash
docker rm -f pg-ex6
docker volume create pg_ex6_data

docker run -d \
  --name pg-ex6 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -p 5432:5432 \
  -v pg_ex6_data:/var/lib/postgresql/data \
  postgres:15
```

Re-run the SQL, then test persistence by removing/recreating the container while keeping the volume:

```bash
docker rm -f pg-ex6
docker run -d --name pg-ex6 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin123 -p 5432:5432 -v pg_ex6_data:/var/lib/postgresql/data postgres:15
```

## Optional: use the provided SQL file

`create_db_users.sql` is another example script (French table/columns). You can run it manually:

```bash
docker exec -i pg-ex6 psql -U admin < create_db_users.sql
```

## Cleanup

```bash
docker rm -f pg-ex6
docker volume rm pg_ex6_data
```
