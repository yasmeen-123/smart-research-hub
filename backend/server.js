const express = require("express");
const cors = require("cors");
const multer = require("multer");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const https = require("https");
const fs = require("fs");

const app = express();
app.use(express.json());

// ✅ Allow your frontend origin
app.use(cors({
  origin: "http://localhost:3000", // replace with your frontend URL
  credentials: true
}));

// In-memory "users" for demo
const users = [];
const SECRET = "supersecret";

// ✅ Register
app.post("/register", async (req, res) => {
  const { email, password } = req.body;
  const hashed = await bcrypt.hash(password, 10);
  users.push({ email, password: hashed });
  res.json({ message: "User registered" });
});

// ✅ Login
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user) {
    return res.status(400).json({ detail: "User not found" });
  }

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) {
    return res.status(400).json({ detail: "Invalid password" });
  }

  const token = jwt.sign({ email }, SECRET, { expiresIn: "1h" });
  res.json({ access_token: token });
});

// ✅ Upload
const upload = multer({ dest: "uploads/" });
app.post("/upload", upload.single("file"), (req, res) => {
  res.json({ filename: req.file.filename, message: "File uploaded" });
});

// ✅ Search (dummy)
app.post("/search", (req, res) => {
  const { query } = req.body;
  res.json({ results: [`You searched for: ${query}`] });
});

// ✅ HTTPS server (self-signed certs for local dev)
const options = {
  key: fs.readFileSync("key.pem"),   // generate with openssl or mkcert
  cert: fs.readFileSync("cert.pem"),
};

https.createServer(options, app).listen(8000, () => {
  console.log("🚀 API running on http://localhost:8000");
});
