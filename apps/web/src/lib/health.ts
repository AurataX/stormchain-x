import type { Assessment } from "./types";

export type Health = "operational" | "partial" | "failed" | "unknown";

export function health(type: string, assessment?: Assessment): Health {
  const report = type === "road" ? assessment?.passability : assessment;
  if (!report || report.flags.includes("UNKNOWN")) return "unknown";
  const [top] = Object.entries(report.probabilities).sort((a, b) => b[1] - a[1])[0];
  if (top === "OPERATIONAL" || top === "OPEN") return "operational";
  return top === "PARTIALLY_OPERATIONAL" ? "partial" : "failed";
}

export function describe(type: string, value: Health) {
  if (type === "road") {
    return { operational: "Road access open", partial: "Road access limited",
      failed: "Road access blocked", unknown: "Road access not reported" }[value];
  }
  return { operational: "Operational", partial: "Partially operational",
    failed: "Damaged or failed", unknown: "Waiting for inspection" }[value];
}

export function ago(iso: string) {
  const minutes = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  if (minutes < 90) return `${minutes} min ago`;
  return minutes < 2880 ? `${Math.round(minutes / 60)} h ago` : `${Math.round(minutes / 1440)} d ago`;
}

export const money = (cents: number) => `$${(cents / 100).toLocaleString("en-US")}`;
