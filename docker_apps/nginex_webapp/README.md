# Exercise 4 - Nginx web app + local file edit

Goal: serve a custom `index.html` with Nginx, and see changes when you edit the file on your machine.

## Run (recommended: bind mount your local website)

From this folder (so `website/index.html` exists):

```bash
docker run --rm -d \
  --name nginx-ex4 \
  -p 8080:80 \
  -v "$(pwd)/website:/usr/share/nginx/html:ro" \
  nginx:alpine
```

Open: http://localhost:8080

## Edit locally: what happens?

1) Edit `website/index.html` on your host.
2) Refresh the browser.

You should see the new content immediately, because the container serves files from the bind-mounted folder.

## Optional: build your own image (no live editing)

If you bake the file into an image, edits on the host will NOT affect a running container.

Example Dockerfile idea:

```Dockerfile
FROM nginx:alpine
COPY website/ /usr/share/nginx/html/
EXPOSE 80
```

Then:

```bash
docker build -t upec-nginx:ex4 .
docker run --rm -d --name nginx-ex4-img -p 8080:80 upec-nginx:ex4
```

## Cleanup

```bash
docker rm -f nginx-ex4
```
