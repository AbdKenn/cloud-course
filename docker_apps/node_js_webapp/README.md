# Exercise 2 - Node.js webapp in Docker

Goal: build and run a simple Node/Express API in a container.

## Build

```bash
docker build -t upec-node:ex2 .
```

## Run

```bash
docker run --rm -d --name node-ex2 -p 3000:3000 upec-node:ex2
docker logs -f node-ex2
```

## Use the app

In another terminal:

```bash
curl http://localhost:3000/
curl http://localhost:3000/time
```

## Inspect from inside the container

```bash
docker exec -it node-ex2 sh
node -v
exit
```

## Cleanup

```bash
docker rm -f node-ex2
```
