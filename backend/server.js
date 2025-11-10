const express = require("express");
const cors = require("cors");
const multer = require("multer");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const https = require("https");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

// ✅ Allow your frontend origin
app.use(cors({
  origin: "http://localhost:3000", // update if frontend runs elsewhere
  credentials: true
}));

// ✅ In-memory user store (temporary)
const users = [];
const SECRET = "supersecret"; // use env var in production

// ✅ Register route
app.post("/register", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password)
    return res.status(400).json({ detail: "Email and password required" });

  const existing = users.find(u => u.email === email);
  if (existing)
    return res.status(400).json({ detail: "User already registered" });

  const hashed = await bcrypt.hash(password, 10);
  users.push({ email, password: hashed });

  res.json({ message: "User registered" });
});

// ✅ Login route
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);

  if (!user)
    return res.status(400).json({ detail: "User not found" });

  const valid = await bcrypt.compare(password, user.password);
  if (!valid)
    return res.status(400).json({ detail: "Invalid password" });

  const token = jwt.sign({ email }, SECRET, { expiresIn: "1h" });
  res.json({ access_token: token });
});

// ✅ Upload route
const upload = multer({ dest: path.join(__dirname, "uploads") });

app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file)
    return res.status(400).json({ detail: "No file uploaded" });

  res.json({ filename: req.file.filename, message: "File uploaded" });
});

// ✅ Search (dummy endpoint)
app.post("/search", (req, res) => {
  const { query } = req.body;
  res.json({ results: [`You searched for: ${query}`] });
});

// ✅ HTTPS server setup
const keyPath = path.join(__dirname, "key.pem");
const certPath = path.join(__dirname, "cert.pem");

if (!fs.existsSync(keyPath) || !fs.existsSync(certPath)) {
  console.error("❌ Missing SSL certificate or key. Run:");
  console.error("   openssl req -nodes -new -x509 -keyout key.pem -out cert.pem");
  process.exit(1);
}

const options = {
  key: fs.readFileSync(keyPath),
  cert: fs.readFileSync(certPath),
};

https.createServer(options, app).listen(8000, () => {
  console.log("🚀 API running at https://localhost:8000");
});
