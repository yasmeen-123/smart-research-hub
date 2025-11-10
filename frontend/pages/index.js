"use client";

import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [file, setFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);

  // ✅ Backend API base URL (No change needed here)
  const API_BASE =
    process.env.NEXT_PUBLIC_API_URL ||
    (typeof window !== "undefined" && window.location.hostname === "localhost"
      ? "http://127.0.0.1:8000"
      : "http://backend:8000");

  console.log("API Base is:", API_BASE);

  // ✅ Load token from localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) setToken(savedToken);
  }, []);

  // ✅ Helper for error messages
  const handleError = (e, fallback = "Network error — cannot reach backend") => {
    console.error("❌ API error:", e);
    alert(e.response?.data?.detail || e.message || fallback);
  };

  // ✅ Validate email and password
  const validateCredentials = () => {
    if (!email.trim() || !password.trim()) {
      alert("Email and password cannot be empty");
      return false;
    }
    return true;
  };

  // ✅ Register User
  const register = async () => {
    if (!validateCredentials()) return;

    try {
      console.log("Registering via:", `${API_BASE}/register`);
      const res = await axios.post(
        `${API_BASE}/register`,
        { email, password },
        { headers: { "Content-Type": "application/json" } }
      );

      const accessToken = res.data.access_token;
      setToken(accessToken);
      localStorage.setItem("token", accessToken);
      alert("✅ Registered successfully! Token saved.");
      console.log("Register response:", res.data);
    } catch (e) {
      handleError(e);
    }
  };

  // ✅ Login User
  const login = async () => {
    if (!validateCredentials()) return;

    try {
      console.log("Logging in via:", `${API_BASE}/login`);
      const res = await axios.post(
        `${API_BASE}/login`,
        { email, password }
        // Removed redundant "Content-Type" header
      );

      const accessToken = res.data.access_token;
      setToken(accessToken);
      localStorage.setItem("token", accessToken);
      alert("✅ Login successful! Token saved.");
      console.log("Login response:", res.data);
    } catch (e) {
      handleError(e);
    }
  };
  
  // 💡 NEW: Logout User function
  const logout = () => {
    setToken("");
    setEmail(""); 
    setPassword(""); 
    setUploadMsg("");
    setResults(null);
    localStorage.removeItem("token");
    alert("👋 Logged out successfully!");
  };

  // ✅ Upload File
  const upload = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }
    if (!token) {
      alert("You must login first");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert("File size exceeds 5MB");
      return;
    }

    const fd = new FormData();
    fd.append("file", file);

    try {
      console.log("Uploading via:", `${API_BASE}/upload`);
      const res = await axios.post(`${API_BASE}/upload`, fd, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });

      setUploadMsg(JSON.stringify(res.data, null, 2));
      alert("Document uploaded and indexed!");
      console.log("Upload response:", res.data);
    } catch (e) {
      handleError(e);
    }
  };

  // ✅ Perform Search
  const doSearch = async () => {
    if (!query.trim()) {
      alert("Query cannot be empty");
      return;
    }
    if (!token) {
      alert("You must login first");
      return;
    }

    try {
      console.log("Searching via:", `${API_BASE}/search`);
      const res = await axios.post(
        `${API_BASE}/search`,
        { query },
        { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
      );

      setResults(res.data);
      console.log("Search response:", res.data);
    } catch (e) {
      handleError(e);
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif", maxWidth: 800, margin: "0 auto" }}>
      <h1>🌐 Smart Research Hub </h1>

      {/* AUTH SECTION */}
      <section style={{ marginTop: 20 }}>
        <h2>Authentication</h2>
        <input placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input
          placeholder="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ marginLeft: 10 }}
        />
        <div style={{ marginTop: 10 }}>
          <button onClick={register}>Register</button>
          <button onClick={login} style={{ marginLeft: 10 }}>
            Login
          </button>
          {/* 💡 NEW: Logout Button */}
          {token && (
            <button onClick={logout} style={{ marginLeft: 10, background: "#ff6666", color: "white" }}>
              Logout
            </button>
          )}
        </div>
        <div style={{ marginTop: 10 }}>
          Token: **{token ? token.slice(0, 40) + "..." : " not logged in"}**
        </div>
      </section>

      {/* UPLOAD SECTION */}
      <section style={{ marginTop: 40 }}>
        <h2>Upload Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={upload} disabled={!token} style={{ marginLeft: 10 }}>
          Upload
        </button>
        <pre style={{ background: "#f4f4f4", padding: 10, marginTop: 10 }}>{uploadMsg}</pre>
      </section>

      {/* SEARCH SECTION */}
      <section style={{ marginTop: 40 }}>
        <h2>Semantic Search</h2>
        <input placeholder="Ask something" value={query} onChange={(e) => setQuery(e.target.value)} />
        <button onClick={doSearch} disabled={!token} style={{ marginLeft: 10 }}>
          Search
        </button>
        <pre style={{ background: "#f4f4f4", padding: 10, marginTop: 20 }}>
          {/* Enhanced display to show the search results clearly */}
          {results ? JSON.stringify(results, null, 2) : "No results yet."}
        </pre>
      </section>
    </div>
  );
}