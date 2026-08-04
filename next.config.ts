import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/LFB-Research-Site',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
