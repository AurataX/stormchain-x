import { test, expect } from "@playwright/test";
import { GOOGLE_MOCK } from "./google-mock";

for (const width of [360, 768, 1280]) {
  for (const colorScheme of ["light", "dark"] as const) {
    test(`${width}px ${colorScheme}: layout and selection`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.emulateMedia({ colorScheme, reducedMotion: "reduce" });
      await page.route("https://maps.googleapis.com/maps/api/js?*", (route) =>
        route.fulfill({ contentType: "application/javascript", body: GOOGLE_MOCK }));
      await page.goto("/");
      await expect(page.locator(".map")).toContainText("Mock Google Maps");
      const markers = page.locator(".map .map-marker");
      await expect(markers).toHaveCount(7);
      await expect(page.locator(".map")).toHaveAttribute("data-bounds", /83\./);
      await page.getByRole("button", { name: "Central Hospital", exact: true }).click();
      if (width < 1100) await page.getByRole("tab", { name: "Evidence" }).click();
      await expect(page.getByRole("region", { name: "Asset inspector" })).toBeVisible();
      await expect(page.getByRole("form", { name: "Report evidence" })).toBeVisible();
      await expect(page.getByRole("combobox", { name: "Source", exact: true })).toHaveValue(/.+/);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      await page.screenshot({ path: `test-results/selected-${width}-${colorScheme}.png`, fullPage: true });
    });
  }
}
