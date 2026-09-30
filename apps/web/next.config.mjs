export default {
  reactStrictMode: true,
  // The page HTML names hashed assets, so it must revalidate or a redeploy looks stale.
  headers: async () => [
    { source: "/", headers: [{ key: "Cache-Control", value: "no-cache, must-revalidate" }] },
  ],
};
