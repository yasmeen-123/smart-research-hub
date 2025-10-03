/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Allow frontend to call backend without CORS issues
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/:path*", // FastAPI backend
      },
    ];
  },
};

module.exports = nextConfig;
