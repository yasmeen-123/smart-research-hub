const path = require("path");

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enables strict checks in development for better code quality
  reactStrictMode: true,
  
  // NOTE: outputFileTracingRoot is often unnecessary for typical projects 
  // and is removed unless you have a specific monorepo setup.
  
  async rewrites() {
    // 💡 Environment variable for the backend URL
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

    return [
      {
        // 1. Match any path starting with /api/
        source: "/api/:path*",
        
        // 2. Direct it to the backend URL, preserving the path after /api/
        // FIX: Ensuring the path parameter is correctly used in the destination
        destination: `${API_URL}/:path*`, 
      },
    ];
  },
};

module.exports = nextConfig;