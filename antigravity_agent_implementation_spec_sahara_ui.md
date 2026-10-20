# IMPLEMENTATION SPEC & AGENT PROMPT: Sahara Warm-Minimalist Spatial UI

> **How to use:** Copy the prompt block below directly into your AI coding agent (Antigravity, Cursor, Windsurf, or Claude Code) along with your repository. It provides strict design tokens, Tailwind configuration, component architecture, and styling rules.

---

## Direct Agent Prompt (Copy & Paste)

```markdown
You are implementing a high-fidelity frontend redesign for our web application based on the "Sahara" warm-minimalist zero-gravity aesthetic. 

Follow these exact architectural and visual guidelines:

### 1. Visual Direction & Aesthetic
- Style: Warm Minimalist, Editorial Tech, Sun-baked Simplicity meets Zero-G Physics.
- Tone: Highly professional, disciplined, enterprise-grade engineering (NOT gamified, toy-like, or sci-fi cliché).
- Geometry: Clean 8px corner radii (`rounded-lg`), subtle hairline borders (`border-[#E8DFD5]`), warm alabaster backgrounds, and rich terracotta accent accents.

### 2. Design Tokens & Palette
Configure Tailwind CSS or your CSS variables with the following palette:
- Base Background (Canvas): `#FAF8F5` (warm cream/alabaster)
- Surface High / Card Background: `#F4EFEA` and `#FFFFFF`
- Surface Border / Divider: `#E8DFD5` (1px subtle border)
- Brand Accent / Primary: `#C2652A` (Sun-baked Terracotta)
- Brand Accent Hover: `#A9531F`
- Text Primary (Headings): `#26211C` (Deep warm espresso)
- Text Secondary (Body): `#6B6258` (Muted warm taupe)
- Text Muted / Micro-copy: `#968D82`
- Code Block Surface: `#1C1917` (Deep stone with warm undertones)
- Status Green / Dot: `#16A34A` / Status Warm: `#C2652A`

### 3. Typography
- Headings: Clean geometric sans or editorial serif/sans blend (e.g. `font-family: 'Manrope', sans-serif`).
  - Hero Display: 3.5rem to 4.25rem, tracking tight (`tracking-tight`), leading snug (`leading-[1.1]`).
  - Editorial italic accent: Use an elegant serif or italicized serif (`font-serif italic font-normal text-[#C2652A]`) for standout conceptual terms like *"Spatial computing"*.
- Body: `Manrope` or system sans, 15px - 16px, `leading-relaxed`, color `#6B6258`.
- Monospace / Telemetry: `JetBrains Mono` or `ui-monospace`, 12px - 13px with uppercase tracking for status badges.

### 4. Layout Architecture to Build
Construct the page with the following sections:

1. **Top Navigation Bar:**
   - Left: Logo icon + Wordmark ("Aura") + Live Status Badge (`● ZERO-G ENGINE: 0.00G ACTIVE` in soft terracotta chip).
   - Center: Floating pill container with links: "Overview", "Spatial Canvas", "Physics Engine", "Components", "Documentation".
   - Right: "Connect Cloud" link + "Launch Studio" primary button (`bg-[#C2652A] text-white rounded-lg hover:bg-[#A9531F]`) + Profile icon.

2. **Hero Header:**
   - Pill tag: `● AURA 2.4 RUNTIME • ZERO-G SPATIAL HYPERVISOR`
   - Headline: "Interface without friction. *Spatial computing* for the modern web."
   - Paragraph: Concise explanation of zero-gravity coordinate systems, physics state machines, and optical glassmorphic depth.
   - Action row: Primary CTA ("Deploy to Orbit"), secondary outline button ("Explore Interactive Canvas"), and interactive copyable CLI snippet pill (`npx aura-spatial init --gravity=0`).
   - Micro trust banner: "Engineered for next-gen spatial WebXR, vision-grade workspaces, and zero-latency canvases".

3. **Interactive Spatial Hypervisor / Canvas Simulator:**
   - Enclosed workbench with simulated coordinate system background.
   - Three floating floating-inspector cards:
     - **Card A (Coordinate Axes):** Real-time pitch, yaw, depth gauges with a mini harmonic resonance curve SVG/canvas.
     - **Card B (Zero-G Dynamics):** Interactive sliders for Damping Coefficient (0.82), Orbital Drag Friction (0.04), and Magnetic Snap Radius (120px) + "Emit Velocity Vector Impulse" terracotta button.
     - **Card C (Refraction Shader):** Sliders for Gaussian Kernel, Specular Highlight, Chromatic Shift + active caustic shading pill.

4. **Technical Pillars (3-Column Grid):**
   - 3 clean white cards with 1px `#E8DFD5` border, warm badge, clear heading, technical description, and arrow link:
     - Card 1: Sub-millimeter Inertia / Mathematical Gravity Wells
     - Card 2: Luminance Refraction / Dynamic Optical Depth
     - Card 3: 0.4KB Footprint / Zero-Runtime Overhead

5. **Code & Telemetry Split Screen:**
   - Left: Mac-style syntax editor window (`SpaceStage.tsx`, TypeScript/React 19) showing `@aura/spatial` usage with `<SpatialProvider gravity={0.00}>`.
   - Right: Live Telemetry panel with real-time frame budget (1.42ms / 16.6ms), active kinematic nodes (48 Swarm Entities), client GPU load, and symplectic collision status. Bottom multi-bar physics dispatch thread meter (120 Hz).

6. **Key Performance Metrics Strip:**
   - 4-column minimal stat callouts:
     - `99.99%` Framerate Stability
     - `0.00g` Baseline Friction
     - `140+` Glass Primitives
     - `<2ms` Loop Latency

7. **Bottom Action Box & System Telemetry Footer:**
   - Polished card with dual actions: "Start Free Sandbox" and "Read Whitepaper".
   - Footer bar showing: `● NODE LATENCY: 4.2ms` • `● ACTIVE NODES: 1,048 Swarm` • `● PRECISION: 64-bit Float` alongside standard legal links.
```

---

## Tailwind CSS Config Supplement

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        sahara: {
          50: '#FAF8F5',
          100: '#F4EFEA',
          200: '#E8DFD5',
          300: '#D5C4B5',
          500: '#C2652A',
          600: '#A9531F',
          800: '#6B6258',
          900: '#26211C',
        }
      },
      fontFamily: {
        sans: ['Manrope', 'sans-serif'],
        serif: ['Newsreader', 'Playfair Display', 'serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
      },
      borderRadius: {
        'sahara': '8px'
      }
    }
  }
}
```
