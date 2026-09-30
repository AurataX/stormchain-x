export const GOOGLE_MOCK = `
class MapMock {
  constructor(container) { this.container = container; container.textContent = 'Mock Google Maps'; }
  fitBounds(bounds) { this.container.dataset.bounds = JSON.stringify(bounds); }
}
class MarkerMock extends EventTarget {
  constructor(options) {
    super(); this.node = document.createElement('button'); this.node.title = options.title;
    this.node.setAttribute('aria-label', options.title);
    this.node.onclick = () => this.dispatchEvent(new Event('gmp-click'));
    this.map = options.map;
  }
  append(node) { this.node.append(node); }
  set map(value) { if (value) value.container.append(this.node); else this.node.remove(); }
}
class LineMock {
  constructor(options) { this.options = options; }
  addListener() {}
  setMap() {}
}
window.google = { maps: {
  Map: MapMock, Polyline: LineMock, ColorScheme: { FOLLOW_SYSTEM: 'FOLLOW_SYSTEM' },
  marker: { AdvancedMarkerElement: MarkerMock }, event: { clearInstanceListeners() {} }
}};
window.stormchainMapsReady();
`;
