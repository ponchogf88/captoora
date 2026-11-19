# Implementation Plan for Live‑Updating Farmasi 799 Dashboard

## Goal Description
Create a dashboard that reflects the current status of the 799 photos project in near‑real‑time. The UI must show compact numeric counters and smooth, glass‑styled progress bars ("Glass Moises" aesthetic). The dashboard should refresh automatically every **15 minutes** without requiring manual page reloads. No neon or overly bright colors; minimal text, focusing on visual bars.

## User Review Required
- **Refresh Mechanism**: Do you prefer a full page reload every 15 minutes (simplest) or an Ajax‑based partial update that only refreshes the numeric counters and bars?  
- **Color Palette**: The plan uses muted glass tones (`bg-white/5`, `bg-white/30`, `border-white/20`).  If you have specific brand colors to incorporate, let us know.

## Open Questions
> [!IMPORTANT] **Refresh Preference** – Choose between:
> - **Option A** – Simple `setInterval(() => location.reload(), 900000);` (full reload).
> - **Option B** – Generate a lightweight JSON data file (`dashboard_data.json`) via a background script every 15 minutes and let the page fetch it via `fetch()` to update the UI without a full reload.

> [!IMPORTANT] **Hosting for JSON** – If Option B is selected, where should the generated JSON be stored? Options:
> - In the repo (served via GitHub Pages).
> - In a local folder served by a simple Python HTTP server.
> - Directly on Google Drive with public link (requires CORS handling).

## Proposed Changes
---
### UI Enhancements (Glass Moises styling)
#### [MODIFY] [DASHBOARD_FARMASI_799.html](file:///Users/imac/Library/Mobile%20Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/proyectos/farmasi-799/DASHBOARD_FARMASI_799.html)
- Add Tailwind utility classes to the progress‑bar container:
  ```html
  <div class="relative w-full h-4 bg-white/5 backdrop-blur-sm border border-white/20 rounded-xl overflow-hidden">
    <div class="h-4 bg-white/30 rounded-xl transition-all duration-500" style="width: ${progress}%"></div>
  </div>
  ```
- Replace any bright `bg‑captoora‑limeHover` or `bg‑emerald‑500` classes with the glass classes above.
- Apply subtle shadows: `shadow-[0_2px_8px_rgba(0,0,0,0.2)]` to KPI cards.
- Ensure text colors are muted: `text-gray-300` for secondary info, `text-white` for primary numbers.
- Add a global CSS transition for the whole page opacity to smooth the refresh effect:
  ```css
  html, body { transition: opacity 0.5s; }
  ```

---
### Auto‑Refresh Implementation
#### Option A – Full Page Reload (default)
#### [MODIFY] [DASHBOARD_FARMASI_799.html](file:///Users/imac/Library/Mobile%20Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/proyectos/farmasi-799/DASHBOARD_FARMASI_799.html)
- Insert at the end of the existing `<script>` block (around line 420):
  ```js
  // 15‑minute auto‑refresh (glass‑style fade)
  setInterval(() => {
    document.documentElement.style.opacity = '0';
    setTimeout(() => location.reload(), 500);
  }, 15 * 60 * 1000);
  ```
- This adds a smooth fade‑out before the reload, keeping the glass aesthetic.

#### Option B – JSON‑Based Partial Update (if approved)
1. **Background Data Generator** (Python script) – runs via `cron` every 15 min to read `fuentes_799.json` & `estado_799.json`, recompute aggregates, and write `dashboard_data.json` to the repo.
2. **Frontend Fetch Logic** – replace the static `const data = {...}` block with a `fetch('/dashboard_data.json')` call that updates the DOM (`renderClusters()`, `renderCounters()`).
3. **Cron Setup** – `*/15 * * * * /usr/bin/python3 /path/to/generate_dashboard_data.py`.

---
### Repository Updates
#### [MODIFY] [README.md] (optional)
- Add a short section describing the auto‑refresh behavior and how to adjust the interval.

#### [MODIFY] [.github/workflows/deploy.yml] (if using GitHub Pages & Option B)
- Ensure the workflow pushes the newly generated `dashboard_data.json` after the cron script runs.

---
## Verification Plan
### Automated Tests
- Run `npm run lint` (if a Node tooling setup exists) to ensure Tailwind classes are valid.
- Execute the data‑generation script locally and verify that `dashboard_data.json` matches the embedded `dashboard_json` structure.

### Manual Verification
1. Open the updated dashboard in Chrome.
2. Confirm progress bars display the new glass styling.
3. Wait 15 minutes (or temporarily set the interval to 10 seconds for testing) and verify the fade‑out + reload occurs without errors.
4. If Option B is chosen, open DevTools Network tab; ensure a `GET dashboard_data.json` request is made every 15 minutes and UI updates accordingly.
5. Commit changes, push to GitHub, and confirm the live GitHub Pages preview reflects the new UI.

---
*Once you approve the chosen refresh mechanism (Option A or Option B) and any color tweaks, we will implement the changes and push them to the repository.*
