const express = require("express");
const os = require("os");

const app = express();

app.get("/", (req, res) => {
  res.json({
    message: "Hello from Cloud Course Docker JS Server!",
    hostname: os.hostname(),
    platform: os.platform(),
    runtime: "Node.js inside a container"
  });
});

app.get("/time", (req, res) => {
  res.send(`Current server time: ${new Date()}`);
});

app.listen(3000, () => {
  console.log("API running on port 3000");
});
