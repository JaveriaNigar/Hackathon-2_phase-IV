// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";
import Header from '@/components/Header';
import { isAuthenticated } from '@/lib/auth';
import { redirect } from 'next/navigation';
import CursorEffectWrapper from '@/components/CursorEffectWrapper';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: "Todo App - AI Interface",
  description: "A modern AI-style todo app with futuristic interface",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className="h-screen flex flex-col overflow-hidden antialiased"
      >
        <CursorEffectWrapper>
          <Header />
          <main className="flex-1 overflow-y-auto bg-background">
            {children}
          </main>
          <Footer />
        </CursorEffectWrapper>
      </body>
    </html>
  );
}