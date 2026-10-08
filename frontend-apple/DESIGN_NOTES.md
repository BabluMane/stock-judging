# Apple HIG Redesign — Design Notes

Branch: `port/frontend-apple/` (copy of `port/frontend/` + redesign).
Status: **For parent review. Do NOT overwrite live frontend yet.**

## What changed

### Typography (`typography.md`)
- SF system stack: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", ...`
- macOS text-style scale: Large Title 26 → Title 2 17 → Headline 13 semibold → Body 13 → Footnote 11
- Tightened letter-spacing on headings (-0.02em), tabular numerals on all data
- No light/thin weights on small text

### Color (`color.md`, `dark-mode.md`)
- True Apple dark: `#000` base, `#1c1c1e` elevated, `#2c2c2e` secondary
- Semantic labels: primary white → secondary 62% → tertiary 42%
- **One accent**: Apple blue `#0a84ff` (was `#5b9dd9` used decoratively)
- Category badges keep meaning, refined hues: green/yellow/blue/red system tones
- Hairline separators `rgba(255,255,255,0.12)` instead of solid `#2a3038` borders

### Layout (`layout.md`)
- Generous whitespace: max-width 1064px, 32px section rhythm
- Cards: 12px radius, subtle shadow, 1px hairline borders
- Tables: no heavy chrome — hairline row separators, cleaner headers

### Liquid Glass (`liquid-glass.md`)
- Glass **only** on top nav (functional layer): `backdrop-filter: blur(24px) saturate(1.4)`
- Content cards stay opaque — no glass on content (per the checklist)
- `prefers-reduced-transparency` falls back to solid

### Micro-interactions
- 120–150ms ease on hover (rows lift 1px, cards brighten borders)
- Filter pills: active state is solid blue with soft glow
- Buttons: subtle lift + shadow on hover
- All disabled under `prefers-reduced-motion`

### Accessibility (`accessibility.md`)
- Visible `:focus-visible` rings (2px accent)
- Contrast: primary text on black exceeds 7:1

## Files changed (vs live frontend)
- `css/styles.css` — full rewrite (all class names preserved, JS untouched)
- `best-today.html` — `var(--text)` → `var(--label)` (3 inline styles)

## Before / after
| Element | Before | After |
|---|---|---|
| Background | `#0f1216` flat | `#000` with `#1c1c1e` elevated cards |
| Accent | `#5b9dd9` muted blue | `#0a84ff` Apple blue, single use |
| Nav | Solid `#171b21` | Translucent glass blur |
| Headings | 22px, no tracking | 26px, -0.02em tracking, SF |
| Badges | 1px borders, muted | Borderless soft fills, semibold |
| Filters | Boxy buttons | Pill segmented control |
| Tables | Heavy `#2a3038` grid | Hairline separators, airier rows |
| Decision panel | Blue gradient wash | Refined deep-blue gradient, larger hero number |

## Verification
- `node --check` clean on all JS
- All 5 category badges render correctly
- No hardcoded colors in JS; all CSS classes referenced exist
- No external fonts or libraries (system stack only)
