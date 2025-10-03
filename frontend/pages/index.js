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

  const API_BASE = "http://localhost:8000";

  async function register() {
    try {
      const res = await axios.post(`${API_BASE}/register`, { email, password });
      setToken(res.data.access_token);
      alert("Registered and logged in");
    } catch (e) {
      alert(e.response?.data?.detail || e.message);
    }
  }

  async function login() {
    try {
      const res = await axios.post(`${API_BASE}/login`, { email, password });
      setToken(res.data.access_token);
      alert("Logged in");
    } catch (e) {
      alert(e.response?.data?.detail || e.message);
    }
  }

  async function upload() {
    if (!file) return alert("Select a file");
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await axios.post(`${API_BASE}/upload`, fd, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`
        }
      });
      setUploadMsg(JSON.stringify(res.data));
    } catch (e) {
      alert(e.response?.data?.detail || e.message);
    }
  }

  async function doSearch() {
    try {
      const res = await axios.post(`${API_BASE}/search`, { query }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResults(res.data);
    } catch (e) {
      alert(e.response?.data?.detail || e.message);
    }
  }

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif", maxWidth: 800, margin: "0 auto" }}>
      <h1>Smart Research Hub — MVP</h1>

      <section style={{ marginTop: 20 }}>
        <h2>Auth</h2>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button onClick={register}>Register</button>
        <button onClick={login}>Login</button>
        <div>Token: {token ? token.slice(0,40) + "..." : "not logged in"}</div>
      </section>

      <section style={{ marginTop: 20 }}>
        <h2>Upload Document</h2>
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <button onClick={upload} disabled={!token}>Upload</button>
        <div>{uploadMsg}</div>
      </section>

      <section style={{ marginTop: 20 }}>
        <h2>Semantic Search</h2>
        <input placeholder="Ask something..." value={query} onChange={e=>setQuery(e.target.value)} />
        <button onClick={doSearch} disabled={!token}>Search</button>
        <pre>{results ? JSON.stringify(results, null, 2) : "No results yet."}</pre>
      </section>
    </div>
  );
}
