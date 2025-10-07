/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  outputFileTracingRoot: __dirname,

  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "https://stunning-space-sniffle-q776vr4j4gpg295x-8000.app.github.dev/"}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
