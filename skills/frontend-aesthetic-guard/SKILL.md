---
name: frontend-aesthetic-guard
description: Generate beautiful, responsive, production-grade frontend layouts that look genuinely designed — not like generic AI output. Prefer React + Tailwind + shadcn/ui. Enforces visual identity, bold aesthetic direction, accessibility, and system consistency.
---

# Frontend Aesthetic Guard

Use this skill when building or refining frontend UIs that must look intentional, premium, and distinct — not like generic AI output.

## Default Stack
- React
- Tailwind CSS
- shadcn/ui
- lucide-react (icons)

If the project already uses another stack/design system, preserve existing conventions.

---

## Phase 0 — Design Thinking (Before Any Code)

Before touching a single token or component, commit to a bold conceptual direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme and own it. Options include: brutally minimal, maximalist editorial, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, typographic-forward, cinematic dark. These are starting points — design something true to context, not borrowed from a list.
- **Differentiation**: What is the ONE thing someone will remember about this UI?
- **Constraints**: Technical requirements (framework, performance, accessibility, responsive targets).

**CRITICAL**: Commit to a clear direction and execute it with precision. Intentionality beats intensity — refined minimalism and bold maximalism both work when executed well.

---

## Phase 1 — Token Strategy

Define or extract design tokens before styling. Every decision should flow from this foundation.

### Required Tokens
- **Colors**: semantic (background, surface, border, text, muted) + brand accent(s). Use 1–2 dominant colors with a single sharp accent. Avoid timid, evenly-distributed palettes.
- **Typography**: pair a distinctive display font with a refined body font. Never default to Inter, Roboto, Arial, or system-ui. Import from Google Fonts or similar. Establish clear scale contrast between heading and body.
- **Spacing**: consistent scale (e.g., 4px base grid).
- **Radius**: pick a single strategy — sharp (0–2px), soft (6–8px), or pill — and use it everywhere.
- **Shadow/Elevation**: 2–3 levels max. No random shadow values scattered across components.
- **Motion**: define easing + duration defaults before animating anything.

---

## Phase 2 — Visual Direction → Implementation

### Typography
- Pair a distinctive **display font** (Playfair Display, Fraunces, Syne, Cormorant, Cabinet Grotesk, etc.) with a refined **body font** (DM Sans, Outfit, Figtree, etc.).
- Establish strong heading/body contrast — weak hierarchy is immediately visible.
- Use font-style, tracking, and weight as expressive tools, not decoration.

### Color & Theme
- Use CSS variables for all tokens; reference them across components consistently.
- Dominant color + sharp accent outperforms 5 evenly-weighted colors.
- Vary between light and dark themes across generations. Never default to "light with purple gradient."
- Warm neutrals (cream, stone, sand) read more premium than cold grays.

### Spatial Composition
- Use asymmetry, overlap, and grid-breaking elements intentionally.
- Generous negative space OR controlled density — pick one direction.
- Unexpected layout moments (diagonal flow, full-bleed dark section, off-center hero) make interfaces memorable.

### Motion
- Prioritize CSS-only animations where possible.
- Use `IntersectionObserver` for scroll-triggered reveals — staggered `opacity + translateY` is elegant and lightweight.
- One well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.
- Hover states should surprise — not just change color.

### Backgrounds & Texture
- Grain noise overlay (SVG filter or base64) adds depth and premium feel without performance cost.
- Radial gradients as atmospheric accents, not primary design elements.
- Marquee/ticker bars, full-bleed dark sections, and quote callouts break visual monotony.
- Floating UI cards with backdrop-filter create depth in hero sections.

---

## Phase 3 — Component System Rules

### Consistency
- Single icon family (lucide-react only — no emoji as icons, no mixed sets).
- Consistent corner radius strategy across all components.
- Consistent elevation/shadow behavior (don't mix flat cards with heavy-shadow cards).
- Predictable interactive states: hover, focus, active, disabled.

### Real UX States (Must Build)
- `loading` — skeleton or spinner
- `empty` — meaningful empty state with action
- `error` — visible, non-scary error feedback
- `disabled` — visually distinct, not just opacity: 0.5
- `hover/focus/active` — intentional, accessible

### Accessibility
- Minimum WCAG AA contrast on all text/surface pairs.
- Visible focus states (never `outline: none` without a custom replacement).
- Legible text over all background surfaces, including images and gradients.

---

## Phase 4 — Responsive Behavior

- Mobile-first layout construction.
- No clipped or overlapping content at any breakpoint.
- Stable spacing and typographic hierarchy across breakpoints.
- Floating/decorative elements should collapse gracefully on mobile.
- Navigation collapses cleanly (hamburger or hidden links — never overflows).

---

## Must-Not Rules (Anti-AI Slop)

1. **No emoji as functional icons.** Use lucide-react or an equivalent icon set.
2. **No mixed icon styles.** One family per project.
3. **No default neon glow** (text glow, border glow, heavy luminous shadows) unless explicitly requested.
4. **No saturated purple/blue/green gradients as default palette.**
5. **No excessive glassmorphism** — one backdrop-filter usage per layout, maximum.
6. **No template sections without brand identity.** Every section should feel like it belongs to this product.
7. **No over-animation.** Motion should serve UX, not demonstrate effort.
8. **No weak visual hierarchy.** Headings and body text must have meaningful scale contrast.
9. **No generic placeholder copy as final output.** Write real-sounding content, even if fictional.
10. **No convergence on overused font choices** (Space Grotesk, Inter, Poppins, Nunito). Vary every generation.

> Neon or cyber aesthetics are allowed only when explicitly requested.

---

## Workflow Summary

1. **Context intake** — goal, existing tokens, audience.
2. **Commit to visual direction** — typography, palette, shape language, motion constraints.
3. **Define tokens** — before writing a single component.
4. **Structure first** — layout and information hierarchy before decoration.
5. **Style pass** — apply tokens consistently, restrained accents, meaningful motion.
6. **Refinement pass** — remove generic patterns, tighten rhythm, enforce consistency.
7. **Quality gate** — run checklist before delivering.

---

## Quality Gate Checklist

- [ ] Distinct brand identity is visible in typography, color, and component shape.
- [ ] No emoji icons; iconography is consistent and from a single family.
- [ ] No default neon/glow aesthetics.
- [ ] All text meets WCAG AA contrast minimum.
- [ ] Focus states are visible and custom if needed.
- [ ] Mobile and desktop layouts are both solid — no overflow, no clipping.
- [ ] All components look like one system, not a mixed kit.
- [ ] Key non-happy-path states are present (loading, empty, error).
- [ ] Motion is purposeful — not decorative noise.
- [ ] Font choice is distinctive and consistent across the system.
- [ ] Color palette is coherent with 1–2 dominant tones and a single accent.

---

## Prompt Macros

### Landing Page
> "Create a high-quality landing page in React + Tailwind + shadcn/ui. Define a token set with distinctive typography (display + body font pair), a warm or dark dominant palette with a single accent, and a clear editorial direction. Avoid AI-generic gradients, neon, emoji icons, and template feel. Build strong section hierarchy, clear CTA flow, scroll-triggered reveals, and responsive behavior. Include floating UI details (cards, marquees, full-bleed sections) for depth. Deliver refined hover/focus states and WCAG AA contrast."

### Dashboard
> "Create a SaaS dashboard UI in React + Tailwind + shadcn/ui with a coherent component system, clear data hierarchy, and production-like states (loading, empty, error). Use lucide-react icons only. Define tokens before building. Avoid generic AI clichés (neon, over-glassmorphism, random gradients). Prioritize information density, readability, and consistent elevation."

### Refinement
> "Refine this existing UI to remove generic AI look. Keep structure and functionality, but improve typography hierarchy, spacing rhythm, token consistency, and brand distinctiveness. Reduce decorative noise, enforce accessibility contrast, tighten responsive fidelity, and replace any emoji icons with lucide-react equivalents."

---

## Output Format

When this skill is used, the output should include:

1. **Visual direction** — 1–2 lines describing the chosen aesthetic.
2. **Token strategy** — palette, font pair, radius/shadow decisions.
3. **Implemented UI** — responsive, with real copy and real UX states.
4. **Quality gate self-check** — brief confirmation of checklist items met.
