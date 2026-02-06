# Python User Management App – Dockerized

This app is a Flask web application to create and manage users, connected to a PostgreSQL database.

## Steps to run

1. Start PostgreSQL container:

```bash
docker run -d \
  --name users-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=usersdb \
  -p 5432:5432 \
  postgres:15
```


Build the Flask app image:

```bash
docker build -t flask-user-app .
```

Run the Flask app container:

```bash
docker run -d \
  --name flask-user-app \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=usersdb \
  -e POSTGRES_HOST=host.docker.internal \
  -p 5000:5000 \
  flask-user-app
```

Note: host.docker.internal works for connecting to host PostgreSQL from container (on Windows/Mac). On Linux, you might use the host IP or network mode.

Test API:

List users: GET http://localhost:5000/users

Add user: POST http://localhost:5000/users
Body JSON:

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```