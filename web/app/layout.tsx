import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "梗应 AI · 这句话该配什么图",
  description: "用一句话搜索最懂你的表情包",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}

