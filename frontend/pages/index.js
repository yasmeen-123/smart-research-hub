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

  // Backend API base URL
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

  // ✅ Register User
  const register = async () => {
    try {
      const res = await axios.post(`${API_BASE}/register`, { email, password });
      alert("Registered and logged in");
      console.log("Register success:", res.data);
    } catch (e) {
      console.error("Register error:", e);
      alert(e.response?.data?.detail || "Network error — cannot reach backend");
    }
  };

  // ✅ Login User
  const login = async () => {
    try {
      const res = await axios.post(`${API_BASE}/login`, { email, password });
      setToken(res.data.access_token);
      alert("Logged in");
      console.log("Login success:", res.data);
    } catch (e) {
      console.error("Login error:", e);
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
      const res = await axios.post(`${API_BASE}/upload`, fd, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });
      setUploadMsg(JSON.stringify(res.data));
      console.log("Upload success:", res.data);
    } catch (e) {
      console.error("Upload error:", e);
      alert(e.response?.data?.detail || e.message);
    }
  };

  // ✅ Perform Search
  const doSearch = async () => {
    try {
      const res = await axios.post(
        `${API_BASE}/search`,
        { query },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setResults(res.data);
      console.log("Search results:", res.data);
    } catch (e) {
      console.error("Search error:", e);
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
      <h1>Smart Research Hub — MVP</h1>

      {/* Auth Section */}
      <section style={{ marginTop: 20 }}>
        <h2>Auth</h2>
        <input
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          placeholder="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={register}>Register</button>
        <button onClick={login}>Login</button>
        <div>
          Token: {token ? token.slice(0, 40) + "..." : "not logged in"}
        </div>
      </section>

      {/* Upload Section */}
      <section style={{ marginTop: 20 }}>
        <h2>Upload Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={upload} disabled={!token}>
          Upload
        </button>
        <div>{uploadMsg}</div>
      </section>

      {/* Search Section */}
      <section style={{ marginTop: 20 }}>
        <h2>Semantic Search</h2>
        <input
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={doSearch} disabled={!token}>
          Search
        </button>
        <pre>
          {results ? JSON.stringify(results, null, 2) : "No results yet."}
        </pre>
      </section>
    </div>
  );
}
