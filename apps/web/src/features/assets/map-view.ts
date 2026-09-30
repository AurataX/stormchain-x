// Tilted vector map by default; the button flips between 3D and a flat top-down view.
export const mapOptions = (): google.maps.MapOptions => ({
  mapId: process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID || "DEMO_MAP_ID",
  center: { lat: 17.76, lng: 83.315 }, zoom: 12, tilt: 60, heading: 20,
  colorScheme: google.maps.ColorScheme.LIGHT,
  mapTypeId: "hybrid",
  mapTypeControl: true,
  mapTypeControlOptions: { mapTypeIds: ["hybrid", "roadmap"], position: google.maps.ControlPosition.BOTTOM_LEFT },
  streetViewControl: false, fullscreenControl: false,
  gestureHandling: "cooperative",
});

// Tilt only works on vector maps, so the button appears only once the map reports VECTOR.
export function addViewToggle(map: google.maps.Map) {
  map.addListener("renderingtype_changed", () => build(map));
  build(map);
}

const added = new WeakSet<google.maps.Map>();
function build(map: google.maps.Map) {
  if (added.has(map) || map.getRenderingType() !== google.maps.RenderingType.VECTOR) return;
  added.add(map);
  const button = document.createElement("button");
  button.className = "map-3d";
  let flat = false;
  const show = () => { button.textContent = flat ? "3D view" : "2D view"; };
  button.onclick = () => {
    flat = !flat;
    map.setTilt(flat ? 0 : 60);
    map.setHeading(flat ? 0 : 20);
    show();
  };
  show();
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(button);
}
