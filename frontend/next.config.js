/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  outputFileTracingRoot: __dirname,

  // 👇 Add this block to remove the cross-origin warning
  experimental: {
    allowedDevOrigins: ["http://127.0.0.1:3000", "http://localhost:3000"],
  },

  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${
          process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000"
        }/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
