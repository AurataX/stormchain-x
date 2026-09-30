# Component and animation sources

Atelier references shadcn/ui, Radix, Motion, Aceternity, ReactBits, Magic UI,
Kokonut UI, Bklit, Anime.js, GSAP, Lenis, Rive, and Lottie.
Their inclusion in Atelier is not a requirement to install them all.

Phase 4 shortlist:

- shadcn/ui + Radix for accessible dialog, tabs, select, and tooltips.
- Lucide for one consistent icon family.
- Google Maps JavaScript API for geographic assets and dependency overlays (user-selected).
- Native CSS for routine transitions; Motion for necessary layout continuity.
- Native tables and SVG for small comparisons before adding a chart package.

Before importing a registry component, inspect its actual source, dependencies,
license, accessibility, and bundle impact. Record its URL and version here.
Never claim a registry was queried or component installed without evidence.

Aceternity/ReactBits/Magic UI effects, GSAP/Lenis scrolling, 3D, and animated
illustrations currently have no operational purpose. Reconsider only against
a concrete interaction requirement. No dependency is installed during Phase 1.

Current Phase 4 map uses the [Google advanced marker API](https://developers.google.com/maps/documentation/javascript/advanced-markers/start)
and [polylines](https://developers.google.com/maps/documentation/javascript/shapes),
loaded once on the `weekly` service channel with `maps,marker`. `DEMO_MAP_ID` is
the sample fallback; an optional configured map ID replaces it. Service use is subject
to Google's platform terms; this is not a bundled open-source map renderer.
`@types/google.maps` 3.66.4 (MIT) supplies compile-time types. MapLibre was removed.
`@playwright/test` 1.63.0 (Apache-2.0) runs checks with installed Chrome.
