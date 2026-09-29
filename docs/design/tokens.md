# Design tokens

| Role | Dark | Light |
|---|---|---|
| Canvas | #0C0E14 | #F6F7F9 |
| Surface | #161922 | #FFFFFF |
| Border | #303544 | #D8DEE7 |
| Primary text | #F4F6FA | #17202D |
| Secondary text | #ABB5C6 | #526077 |
| Brand / focus | #69B7FF | #175CD3 |
| Operational | #52D6B0 | #08745A |
| Partial | #F4BE63 | #875300 |
| Failed / damaged | #FF8585 | #B42318 |
| Unknown | #BCADF4 | #6941A5 |

Blue is the sole brand accent; semantic state colors communicate evidence,
never decoration. Confirm actual contrast at implementation, including map layers.
Use text and distinct shapes/dashed outlines alongside every state color.

Typography: locally served Geist Sans or a system sans fallback, weights
400/500/600, tabular numerals. Minimum body 14px; compact labels 12px.
Use restrained headings, no oversized marketing headlines inside operations.

Spacing: 4/8/12/16/24/32px. Inputs radius 8, panels 12, dialogs 16.
Hairline borders and subtle inset highlights; shadows only on floating panels.

Lucide icons, 1.5px stroke, 16/20/24px, currentColor. Label icon-only controls
accessibly. All values live in one future CSS token file; no component hex codes.
