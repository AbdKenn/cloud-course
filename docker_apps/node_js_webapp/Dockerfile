FROM node:18-alpine

WORKDIR /app

COPY server.js .

RUN npm install express

EXPOSE 3000

CMD ["node", "server.js"]
