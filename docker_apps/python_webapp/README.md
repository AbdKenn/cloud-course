# Exercise 3 - Python (Flask) webapp in Docker

Goal: build and run a simple Flask API in a container.

## Build

```bash
docker build -t upec-python:ex3 .
```

## Run

```bash
docker run --rm -d --name python-ex3 -p 5000:5000 upec-python:ex3
docker logs -f python-ex3
```

## Use the app

```bash
curl http://localhost:5000/
curl http://localhost:5000/course
```

## Cleanup

```bash
docker rm -f python-ex3
```
