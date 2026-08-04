import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "语言纤维束 LFB — 开放研究计划",
  description: "探索从向量表示到结构表示的 AI 结构层接口。",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
