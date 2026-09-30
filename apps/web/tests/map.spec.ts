import { test, expect } from "@playwright/test";
import { GOOGLE_MOCK } from "./google-mock";

test("advanced marker selection survives rerenders without duplicates", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.route("https://maps.googleapis.com/maps/api/js?*", (route) =>
    route.fulfill({ contentType: "application/javascript", body: GOOGLE_MOCK }));
  await page.goto("/");
  const marker = page.getByRole("button", { name: /^Central Hospital:/ });
  await marker.click();
  await expect(page.getByRole("region", { name: "Asset inspector" })).toContainText("Central Hospital");
  await expect(page.locator(".map-marker.is-selected")).toHaveCount(1);
  await page.getByRole("button", { name: /^North Hospital:/ }).click();
  await expect(page.getByRole("region", { name: "Asset inspector" })).toContainText("North Hospital");
  await expect(page.locator(".map-marker")).toHaveCount(7);
});

test("network failure leaves useful asset list", async ({ page }) => {
  await page.route("https://maps.googleapis.com/maps/api/js?*", (route) => route.abort());
  await page.goto("/");
  await expect(page.locator(".mapbox").getByRole("alert")).toContainText("Google Maps could not load");
  await expect(page.getByRole("button", { name: "Central Hospital", exact: true })).toBeVisible();
});

test("authorization failure is explicit", async ({ page }) => {
  await page.route("https://maps.googleapis.com/maps/api/js?*", (route) =>
    route.fulfill({ contentType: "application/javascript", body: GOOGLE_MOCK + "window.gm_authFailure();" }));
  await page.goto("/");
  await expect(page.locator(".mapbox").getByRole("alert")).toContainText("authorization failed");
});
