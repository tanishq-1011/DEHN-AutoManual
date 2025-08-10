// server.js
import express from "express";
import cors from "cors";
import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3456;

// CORS (you can tighten this later to your frontend origin)
app.use(cors());
app.use(express.json());

// Health-Check
app.get("/health", (req, res) => {
  res.json({ ok: true });
});

// Devices endpoint (serves ./dehn.data.json)
app.get("/api/devices", async (req, res) => {
  try {
    const filePath = path.join(__dirname, "dehn-data.json");
    const raw = await fs.readFile(filePath, "utf-8");
    const data = JSON.parse(raw); // validate JSON before sending
    // light caching: change to 'no-store' during dev if you want
    res.set("Cache-Control", "public, max-age=60");
    res.json(data);
  } catch (err) {
    console.error("Failed to read dehn.data.json:", err);
    res.status(500).json({ error: "Could not load device data" });
  }
});

// Chat endpoint
app.post("/api/chat", async (req, res) => {
  console.log("Empfangene Nachricht:", req.body.message);
  try {
    const filePath = path.join(__dirname, "groq_response Bilingual.txt");
    const content = await fs.readFile(filePath, "utf-8");
    await new Promise((resolve) => setTimeout(resolve, 3000));
    res.json({ reply: content });
  } catch (err) {
    console.error("Fehler beim Lesen der Textdatei:", err);
    res.status(500).json({ error: "Fehler beim Laden der Antwortdatei" });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server läuft auf http://127.0.0.1:${PORT}`);
});
