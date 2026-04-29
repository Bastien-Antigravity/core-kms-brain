---
title: "Obsidian App Configuration Guide"
type: architecture
status: active
microservice: ecosystem-wide
tags:
  - onboarding
  - configuration
  - automation
---

# ⚙️ Obsidian App Configuration Guide

To ensure the **Bastien-Antigravity** Obsidian Brain functions correctly, follow these configuration steps within your Obsidian Application.

## 1. Core Plugin Settings
- **Files & Links**:
    - *Default location for new notes*: Same folder as current file.
    - *New link format*: Relative path to file (or shortest path when possible).
    - *Use [[Wikilinks]]*: **ON**.
- **Appearance**:
    - *Base color scheme*: Your choice (Dark Recommended).
    - *Font*: Inter (Interface), JetBrains Mono (Monospaced).

## 2. Community Plugins (Required)
Install and enable the following from the Community Plugins browser:

### 🧩 Dataview
- **Status**: MANDATORY.
- **Purpose**: Powers all dynamic tables and dashboards (Master MOC, Sprint Dashboard).
- **Settings**: Enable `Enable JavaScript Queries` and `Enable Inline JavaScript Queries`.

## 3. Workplace Automation (Clean Sidebar)
We use a custom CSS snippet to hide technical folders that do not contain documentation.

### Activation Steps:
1. Go to **Settings > Appearance**.
2. Scroll to the bottom to **CSS Snippets**.
3. Click the "Folder" icon to open the snippets folder.
4. Ensure `hide_empty_folders.css` is present.
5. **Turn ON** the toggle for `hide_empty_folders`.

### How to Update:
If you add many new folders and want to hide the empty ones again, run the following command in your terminal:
```powershell
python obsidian-brain/05-Scripts/hide_empty_folders.py
```

## 4. Search & Exclusions
If you want to exclude certain folders from Global Search (but keep them in the Explorer):
- Go to **Settings > Files & Links > Excluded Files**.
- Add patterns like `node_modules/` or `.git/`.

---
> [!IMPORTANT] Reloading
> If a Dataview query doesn't update immediately, you can force a refresh by switching to another note and back, or by restarting Obsidian.
