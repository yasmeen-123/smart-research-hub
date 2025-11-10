const path = require("path");

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  outputFileTracingRoot: path.join(__dirname, ".."), 
  
  // 💡 FIX: Add 127.0.0.1 to allowedDevOrigins
  allowedDevOrigins: ["http://127.0.0.1:3000"], 
  
  async rewrites() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${API_URL}/:path*`, 
      },
    ];
  },
};

module.exports = nextConfig;