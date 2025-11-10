const express = require("express");
const cors = require("cors");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const app = express();
app.use(express.json());

// ✅ Allow frontend origin
app.use(cors({
  origin: "http://localhost:3000",
  credentials: true
}));

// ✅ In-memory user store
const users = [];
const SECRET = "supersecret"; // use env var in production

// ✅ Register route
app.post("/register", async (req, res) => {
  const { email, password } = req.body;

  // Validation
  if (!email || !password) {
    return res.status(422).json({ detail: "Email and password are required" });
  }

  // Check existing user
  const existing = users.find(u => u.email === email);
  if (existing) {
    return res.status(422).json({ detail: "User already registered" });
  }

  // Password rules (example: min 6 chars)
  if (password.length < 6) {
    return res.status(422).json({ detail: "Password must be at least 6 characters" });
  }

  const hashed = await bcrypt.hash(password, 10);
  users.push({ email, password: hashed });

  res.json({ message: "User registered successfully" });
});

// ✅ Login route
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);

  if (!user) {
    return res.status(422).json({ detail: "User not found" });
  }

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) {
    return res.status(422).json({ detail: "Invalid password" });
  }

  const token = jwt.sign({ email }, SECRET, { expiresIn: "1h" });
  res.json({ access_token: token });
});

// ✅ Run server in HTTP for local dev
const PORT = 8000;
app.listen(PORT, () => {
  console.log(`🚀 API running at http://localhost:${PORT}`);
});
