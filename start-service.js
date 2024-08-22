import express from "express";
import { activeWindow, openWindows, openWindowsSync } from "get-windows";
import { WebSocketServer } from "ws";

const app = express();
const port = 3001;
const wss = new WebSocketServer({ port: 3002 });

const SENDS_WINDOW_DATA_INTERVAL_IN_MS = 100;

wss.on("connection", (ws) => {
  console.log("WebSocket client connected");

  const sendWindowData = async () => {
    try {
      let start = performance.now();
      const windows = openWindowsSync();
      let end = performance.now();
      console.log("openWindows() method await time: ", end - start);
      console.log("windows", windows);
      ws.send(JSON.stringify(windows));
      setTimeout(sendWindowData, SENDS_WINDOW_DATA_INTERVAL_IN_MS);
    } catch (error) {
      console.error("Failed to get windows:", error);
      ws.close();
    }
  };

  sendWindowData();

  ws.on("close", () => {
    console.log("WebSocket client disconnected");
  });
});

app.get("/windows", async (req, res) => {
  try {
    let start = performance.now();
    const windows = await openWindows();
    let end = performance.now();
    console.log("openWindows() await time: ", end - start);
    console.log("windows", windows);
    res.json(windows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Microservice listening at http://localhost:${port}`);
});
