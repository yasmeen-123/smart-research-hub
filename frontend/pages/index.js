"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [file, setFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);

  // ✅ Backend API base URL
  // Make sure your backend URL works when opened in browser
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "https://stunning-space-sniffle-q776vr4j4gpg295x-8000.app.github.dev/";
    console.log("API Base is:", API_BASE);
  // ✅ Register User
  const register = async () => {
    try {
      console.log("Registering via:", `${API_BASE}/register`);

      const res = await axios.post(`${API_BASE}/register`, {
        email,
        password,
      });
      alert("Registered and logged in successfully!");
      console.log("✅ Register success:", res.data);
    } catch (e) {
      console.error("❌ Register error:", e);
      alert(e.response?.data?.detail || "Network error — cannot reach backend");
    }
  };

  // ✅ Login User
  const login = async () => {
    try {
      console.log("Logging in via:", `${API_BASE}/login`);

      const res = await axios.post(`${API_BASE}/login`, {
        email,
        password,
      });
      setToken(res.data.access_token);
      alert("Login successful!");
      console.log("✅ Login success:", res.data);
    } catch (e) {
      console.error("❌ Login error:", e);
      alert(e.response?.data?.detail || e.message);
    }
  };

  // ✅ Upload File
  const upload = async () => {
    if (!file) {
      alert("Select a file first");
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
      setUploadMsg(JSON.stringify(res.data));
      console.log("✅ Upload success:", res.data);
    } catch (e) {
      console.error("❌ Upload error:", e);
      alert(e.response?.data?.detail || e.message);
    }
  };

  // ✅ Perform Search
  const doSearch = async () => {
    try {
      console.log("Searching via:", `${API_BASE}/search`);

      const res = await axios.post(
        `${API_BASE}/search`,
        { query },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setResults(res.data);
      console.log("✅ Search results:", res.data);
    } catch (e) {
      console.error("❌ Search error:", e);
      alert(e.response?.data?.detail || e.message);
    }
  };

  return (
    <div
      style={{
        padding: 24,
        fontFamily: "sans-serif",
        maxWidth: 800,
        margin: "0 auto",
      }}
    >
      <h1>🌐 Smart Research Hub — MVP</h1>

      {/* ================= AUTH SECTION ================= */}
      <section style={{ marginTop: 20 }}>
        <h2>Authentication</h2>
        <input
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ marginRight: 10 }}
        />
        <input
          placeholder="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <div style={{ marginTop: 10 }}>
          <button onClick={register}>Register</button>
          <button onClick={login} style={{ marginLeft: 10 }}>
            Login
          </button>
        </div>
        <div style={{ marginTop: 10 }}>
          Token: {token ? token.slice(0, 40) + "..." : " not logged in"}
        </div>
      </section>

      {/* ================= UPLOAD SECTION ================= */}
      <section style={{ marginTop: 40 }}>
        <h2>Upload Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button
          onClick={upload}
          disabled={!token}
          style={{ marginLeft: 10 }}
        >
          Upload
        </button>
        <div style={{ marginTop: 10 }}>{uploadMsg}</div>
      </section>

      {/* ================= SEARCH SECTION ================= */}
      <section style={{ marginTop: 40 }}>
        <h2>Semantic Search</h2>
        <input
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ marginRight: 10 }}
        />
        <button onClick={doSearch} disabled={!token}>
          Search
        </button>
        <pre style={{ background: "#f4f4f4", padding: 10, marginTop: 20 }}>
          {results ? JSON.stringify(results, null, 2) : "No results yet."}
        </pre>
      </section>
    </div>
  );
}
