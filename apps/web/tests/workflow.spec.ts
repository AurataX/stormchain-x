import { test, expect } from "@playwright/test";
import { GOOGLE_MOCK } from "./google-mock";

test("persist road evidence and recalculate the stale plan", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.route("https://maps.googleapis.com/maps/api/js?*", (route) =>
    route.fulfill({ contentType: "application/javascript", body: GOOGLE_MOCK }));
  await page.goto("/");
  await page.getByRole("button", { name: "Coastal Access Road", exact: true }).click();
  const form = page.getByRole("form", { name: "Report evidence" });
  await form.getByRole("combobox", { name: "Observed state", exact: true }).selectOption("DAMAGED");
  await form.getByRole("combobox", { name: "Road access", exact: true }).selectOption("BLOCKED");
  const notes = form.getByRole("textbox", { name: "Notes", exact: true });
  await notes.focus();
  await page.keyboard.type("Synthetic browser verification: road remains blocked.");
  await form.getByRole("button", { name: "Submit report" }).click();
  await expect(form.getByRole("status")).toContainText("Saved at");
  await expect(page.getByText("Stale: evidence changed since this plan.")).toBeVisible();
  await page.getByRole("button", { name: "Recalculate" }).click();
  await expect(page.getByRole("button", { name: "Recalculate" })).toBeEnabled({ timeout: 20000 });
  await expect(page.getByText("Stale: evidence changed since this plan.")).toHaveCount(0);
  await page.getByText("Compare with previous version", { exact: true }).click();
  await expect(page.getByRole("region", { name: "Recovery plan" })).toContainText("Solver");
});
