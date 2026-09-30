import type { Metadata } from "next";
import "./tokens.css";
import "./layout.css";
import "./controls.css";
import "./data.css";
import "./dashboard.css";
import "./cards.css";
import "./compact.css";
import "./map.css";
import "./briefing.css";
import "./polish.css";

export const metadata: Metadata = {
  title: "STORMCHAIN-X console",
  description: "Uncertainty-aware recovery planning on synthetic data",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
