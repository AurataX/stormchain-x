import { test, expect } from "@playwright/test";
import { GOOGLE_MOCK } from "./google-mock";

test("briefing shows a saved-fact citation and keeps the plan visible", async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await page.route("https://maps.googleapis.com/maps/api/js?*", (route) =>
    route.fulfill({ contentType: "application/javascript", body: GOOGLE_MOCK }));
  await page.route("**/api/v1/briefings", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({
      answer: "The saved synthetic plan includes road repair.",
      citation_ids: ["plan-v1"],
      sources: { "plan-v1": '{"actions":[{"id":"road-main"}]}' },
      plan_version: 1, model: "gemini-3.5-flash", synthetic: true,
    }),
  }));
  await page.goto("/");
  await page.getByRole("tab", { name: "Plan" }).click();
  const panel = page.getByRole("region", { name: "Recovery plan" });
  if (await panel.getByRole("button", { name: "Generate plan" }).isVisible()) {
    await panel.getByRole("button", { name: "Generate plan" }).click();
  }
  await panel.getByRole("button", { name: "Ask Gemini" }).click();
  await expect(panel.getByRole("status")).toContainText("road repair");
  await panel.getByText("Saved facts cited (1)").click();
  await expect(panel).toContainText("plan-v1");
  await expect(panel).toContainText("Solver");
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
