import "./globals.css";
import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";

export const metadata: Metadata = {
  title: "Tanglish Caption AI — Auto Tamil-to-Tanglish Captions for Creators",
  description:
    "Upload your video and get accurate Tanglish captions in minutes. Built for Instagram Reels, YouTube Shorts, and TikTok Tamil creators.",
  keywords: ["tanglish captions", "tamil subtitle generator", "auto captions tamil", "reels captions ai"],
  openGraph: {
    title: "Tanglish Caption AI",
    description: "Auto-generate Tanglish captions for your Tamil videos in seconds.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en" className="dark">
        <body className="bg-background text-white antialiased min-h-screen">
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
