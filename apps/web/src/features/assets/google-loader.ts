let pending: Promise<void> | undefined;

export function loadGoogleMaps() {
  if (typeof google !== "undefined" && google.maps?.Map) return Promise.resolve();
  if (pending) return pending;
  const key = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
  if (!key) return Promise.reject(new Error("Google Maps key is not configured. Use the asset list below."));
  pending = new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    const fail = () => {
      clearTimeout(timer);
      script.remove();
      pending = undefined;
      reject(new Error("Google Maps could not load. Check connectivity and key restrictions; use the asset list below."));
    };
    const timer = setTimeout(fail, 20000);
    Object.assign(window, {
      stormchainMapsReady: () => { clearTimeout(timer); resolve(); },
      gm_authFailure: () => window.dispatchEvent(new Event("stormchain-map-error")),
    });
    script.src = `https://maps.googleapis.com/maps/api/js?${new URLSearchParams({
      key, callback: "stormchainMapsReady", libraries: "maps,marker", v: "weekly", loading: "async",
    })}`;
    script.async = true;
    script.onerror = fail;
    document.head.append(script);
  });
  return pending;
}
