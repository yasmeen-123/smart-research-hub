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

// --- Configuration and In-Memory Store ---
// 💡 FIX: Use a counter to simulate auto-incrementing database IDs
let nextUserId = 1;
// 💡 FIX: Add 'id' to the user object to match the Python backend structure
const users = []; 
const SECRET = "supersecret"; // use env var in production

// --- Middleware: Protects Routes ---
const authMiddleware = (req, res, next) => {
    // Expecting: Authorization: Bearer <token>
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ detail: "Authentication token missing or malformed" });
    }

    const token = authHeader.split(' ')[1];

    try {
        // Verify token and decode the payload
        const payload = jwt.verify(token, SECRET);
        
        // 💡 FIX: Attach the decoded payload (user info) to the request
        req.user = payload; 
        
        next();
    } catch (error) {
        // Handles expired token, invalid signature, etc.
        console.error("JWT Verification Error:", error.message);
        return res.status(401).json({ detail: "Invalid or expired token" });
    }
};

// --- Routes ---

// ✅ Register route (FIXED: Added User ID)
app.post("/register", async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password || password.length < 6) {
        return res.status(422).json({ detail: "Email, password (min 6 chars) are required" });
    }

    const existing = users.find(u => u.email === email);
    if (existing) {
        return res.status(422).json({ detail: "User already registered" });
    }

    const hashed = await bcrypt.hash(password, 10);
    
    // Store user with a unique ID
    const newUser = { id: nextUserId++, email, password: hashed };
    users.push(newUser);

    // 💡 Generate a token immediately upon successful registration
    const token = jwt.sign({ email: newUser.email, id: newUser.id }, SECRET, { expiresIn: "1h" });

    res.json({ access_token: token, token_type: "bearer" });
});

// ✅ Login route (FIXED: Added User ID to JWT payload)
app.post("/login", async (req, res) => {
    const { email, password } = req.body;
    // 💡 Use a full user object lookup
    const user = users.find(u => u.email === email);

    if (!user) {
        return res.status(401).json({ detail: "Invalid credentials" });
    }

    const valid = await bcrypt.compare(password, user.password);
    if (!valid) {
        return res.status(401).json({ detail: "Invalid credentials" });
    }

    // Include the user ID in the token payload
    const token = jwt.sign({ email: user.email, id: user.id }, SECRET, { expiresIn: "1h" });
    
    res.json({ access_token: token, token_type: "bearer" });
});

// ✅ Protected route example (NEW)
app.get("/user/me", authMiddleware, (req, res) => {
    // The user's ID and email are available on req.user
    const { id, email } = req.user;
    
    // In a real app, you might look up the user data from the DB here
    const user = users.find(u => u.id === id); 
    
    if (!user) {
        return res.status(404).json({ detail: "User not found" });
    }

    // Return the user data (excluding the hashed password)
    res.json({ id: user.id, email: user.email });
});


// ✅ Run server
const PORT = 8000;
app.listen(PORT, () => {
    console.log(`🚀 API running at http://localhost:${PORT}`);
});