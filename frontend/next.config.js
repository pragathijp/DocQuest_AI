/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Proxy API calls to backend during development
  async rewrites() {
    return [
      {
        source: "/upload",
        destination: `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/upload`,
      },
      {
        source: "/query",
        destination: `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/query`,
      },
    ];
  },
};

module.exports = nextConfig;
