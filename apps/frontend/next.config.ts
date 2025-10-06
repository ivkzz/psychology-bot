import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standalone output для оптимизации Docker образа
  // Создает минимальный самодостаточный build
  output: "standalone",
};

export default nextConfig;
