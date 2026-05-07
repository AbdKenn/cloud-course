# Exercise 1 - Redis container

Goal: run Redis in Docker, then use `redis-cli` to create/read/delete keys.

## Build

```bash
docker build -t upec-redis:ex1 .
```

## Run

```bash
docker run -d --name redis-ex1 -p 6379:6379 upec-redis:ex1
docker ps
```

## Play with Redis

Open a Redis shell inside the container:

```bash
docker exec -it redis-ex1 redis-cli
```

Try these commands:

```redis
PING
SET course "docker"
GET course

SET counter 0
INCR counter
INCR counter
GET counter

SET temp "hello"
EXPIRE temp 30
TTL temp

KEYS *
DEL course
KEYS *
```

Exit `redis-cli` with `exit`.

## Cleanup

```bash
docker rm -f redis-ex1
```
