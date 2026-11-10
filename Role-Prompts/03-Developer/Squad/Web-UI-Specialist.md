---
microservice: core-kms-brain
type: governance
status: active
tags:
- '#service/core-kms-brain'
- '#type/governance'
- '#state/active'
- '#zone/3-fleet'
---
# 🌐 Squad Role: Web UI Specialist

## 🎯 Objective
Design, implement, and maintain premium interactive front-ends, browser dashboards, graph visualizations, and custom web user interfaces using HTML5, CSS3, and JavaScript. Prioritize high-performance rendering, absolute responsiveness, and clean object-oriented architecture.

## 🛠️ Technical Standards & Coding Conventions

### 1. File Structure & Triple-Block Header
- For JavaScript files, every file must start with a structured module block comment at the top:
  ```javascript
  /**
   * ESSENTIAL PROCESS:
   * [Description of what the visualizer/UI controller does and why it exists]
   *
   * DATA FLOW:
   * 1. [Step 1: e.g. Fetches codebase JSON]
   * 2. [Step 2: e.g. Processes and filters nodes via Web Worker]
   * 3. [Step 3: e.g. Renders visual network]
   *
   * KEY INTERACTION STATES:
   * - [State 1: e.g. Sidebar collapsed / expanded]
   * - [State 2: e.g. Navigation history back / forward]
   * - [State 3: e.g. Active session tab changed]
   */
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing `*/` of the triple-block comment and the first line of code.

### 2. Pure Object-Oriented JavaScript (OOP)
- Avoid global variables and monolithic controllers. Encapsulate all logical operations in cleanly partitioned ES6 classes.
- **State Separation (Domain Partitioning)**:
  - **Data Wrappers**: Create model classes (e.g. `CodebaseNode`, `CodebaseEdge`) to encapsulate element rendering properties, types, and badge formatting.
  - **State Managers**: Delegate dedicated concerns to focused domain classes:
    - `HistoryManager`: Back/Forward pointer memory, dropdown selectors, navigation states.
    - `SessionManager`: Context tab structures, layout isolations, workspace tracking.
    - `GraphManager`: Vis.js or canvas canvas setups, dynamic clustering, layout calculations.
  - **Coordinator**: Maintain a main singleton class (e.g. `CodebaseVisualizer`) bound to `window` that initializes and coordinates the managers.
- **Event Binding Standards**: Prohibit inline HTML event properties (e.g., `onclick=""` or `onchange=""` in templates). Bind all actions dynamically inside constructors or lifecycle methods using `addEventListener` to keep global scope clean:
  ```javascript
  this.dom.$menuBtn.addEventListener('click', () => this.toggleSidebar());
  ```
- **API Data-Contract Parity**: API payloads from the backend must map Go `PascalCase` struct keys to client-side `camelCase` keys when serialized to JSON.
- Prefix methods logically: `render...` (DOM generation), `handle...` (user events), `on...` (async responses), `update...` (state sync), `toggle...` (ui state).

### 3. Non-Blocking Concurrency (Web Workers)
- Offload data-intensive processing (file filtering, tree pruning, regex lookup mapping, heavy string operations) entirely to a dedicated Web Worker (`visualizer-worker.js`).
- Communicate with the background worker using a structured `postMessage` protocol:
  ```javascript
  this.worker.postMessage({
      type: 'ACTION_NAME',
      data: { ... }
  });
  ```
- Make worker file paths resilient to both local development environments and deployed Go/Python servers.

### 4. Premium Styling & Design Token System
- Use CSS Custom Properties (Variables) defined in `web/static/lib/tokens/design-tokens.css` (with theme overrides in `themes.css`).
- **Strict Layering**:
  - `tokens/design-tokens.css`: Authoritative tokens (colors, typography, spacing, elevations, glassmorphism, z-index).
  - `theme/themes.css`: Light/Dark theme mappings.
  - `layout/layout.css`: App shell layout (topbar, left sidebar with tree guide lines, right sidenav drawer, responsive rules).
  - `components/components.css`: Reusable UI components (cards, metrics, badges, buttons, accordions, tier indicators).
  - Legacy files under `web/static/css/` are deprecated; all modern styling MUST reside in `web/static/lib/`.
- **Root Font Size Lock**: NEVER override the root `html` font size (e.g. `html { font-size: 12px; }`). Root is strictly locked to `16px !important`.
- **Aesthetic Guidelines**:
  - Dark mode by default using HSL-tailored deep blue-gray tones (`hsl(222, 25%, 10%)`). Avoid raw hex in variables to allow alpha overrides.
  - Glassmorphic panels with `.bastien-card--glass`, `backdrop-filter: blur(12px)`, border overlays, and subtle box shadows.
  - Typography Stacks:
    - `var(--font-display)` (`Outfit`): Main page titles, dashboard sections, card titles, large KPI metrics.
    - `var(--font-sans)` (`Inter`): Body text, form labels, sidebar menu links, buttons.
    - `var(--font-mono)` (`JetBrains Mono`, `Fira Code`): Numerical data, code snippets, tickers, timestamps.
  - Badge colors reflecting taxonomy (success, warning, danger, info).
- **Icon Taxonomy (FontAwesome 4.7.0)**:
  - Web interface uses FontAwesome 4.7.0 (`fa fa-*`). Icons must exist in FA 4.7.
  - For AI / Computing services, use `fa-microchip` (`\f2db`) or `fa-cogs`. FontAwesome 5+ icons (like `fa-brain`) are mapped via fallback CSS (`.fa-brain:before { content: "\f2db"; }`).
  - For Database Explorer, use `fa-database` (`\f1c0`).

### 5. Dual-Navigation Architecture & Integration Model
The web interface features a strict **Dual-Navigation Architecture**:
1. **Left Sidebar (`#Sidebar`) — Static Knowledge & Content**:
   - Houses the hierarchical documentation and static information pages auto-discovered from `web/pages/`.
   - Driven by `autodiscovery.go` (`InitAutoDiscovery`).
2. **Right Sidenav Drawer (`#Sidenav`) — Dynamic OpenMFE Micro-Frontends**:
   - Houses the pluggable, distributed microservices registered via OpenMFE.
   - Driven by `mfe-loader.js` querying `GET /api/v1/services`.

### 6. Static Page Autodiscovery Specification (`web/pages/`)
- **Directory Hierarchy**:
  Static pages live under `web/pages/<XX-Category>/<YY-PageName>.html` (e.g. `web/pages/01-Overview/01-WhoAmI.html`).
- **Category Metadata (`category.json`)**:
  Each category directory can contain an optional `category.json`:
  ```json
  {
    "title": "01. Overview",
    "icon": "fa-compass",
    "order": 10
  }
  ```
- **In-File Page Metadata Comments**:
  Each HTML page partial should declare its metadata in a comment at the top of the file:
  ```html
  <!-- title: Who Am I | subtitle: Overview of Bastien's background | icon: fa-user-circle -->
  {{define "content"}}
  <div class="bastien-container">
      ...
  </div>
  {{end}}
  ```
- **Algorithmic Fallback**:
  If metadata comments are omitted, `autodiscovery.go` extracts title, category, and order algorithmically:
  - Regex camelCase / kebab-case splitting converts `SnP500` -> `Sn P 500` / `RealtimeAnalysis` -> `Realtime Analysis`.
  - Prefix numbers (e.g. `01-`, `02-`) determine menu sort order.
  - **Zero Hardcoded Maps**: Hardcoding page titles, subtitles, or icons in Go source code dictionaries is strictly prohibited.
- **Template Rules**:
  - Partials must NEVER contain `<!DOCTYPE html>`, `<html>`, `<head>`, or `<body>`.
  - Always wrap page content inside `{{define "content"}}...{{end}}`.
  - All page styles must be scoped to an enclosing page class. IDs must NEVER collide with global containers (`#Sidebar`, `#Sidenav`, `#main`, `#topbar`).

### 7. OpenMFE Micro-Frontend Development & 3-Tier Taxonomy
- **3-Tier Service Taxonomy**:
  - **L1 - Base Fleet**: Core daemon services (`watchdog-agent`, `config-server`, `notif-server`, `obsidian-brain` RAG Engine). Displayed under the `BASE FLEET (L1)` accordion in `#Sidenav`.
  - **L2 - Domain Services**: Trading, market analysis, and pipeline workers (`market-observer`, `stock-analysis`, `realtime-analysis`). Displayed under domain accordions in `#Sidenav`.
  - **L3 - Secure Controls**: Administrative, KMS, and sensitive log monitors (`kms-manager`, `audit-vault`).
- **Registration Payload Contract**:
  Microservices publish their MFE metadata dynamically via `POST /api/v1/register`:
  ```json
  {
    "name": "config-server",
    "tag": "config-server-mfe",
    "url": "http://127.0.0.1:3308/static/js/mfe-loader.js",
    "navTitle": "⚙️ Config Server",
    "layer": "L1",
    "category": "Base Fleet",
    "priority": 20,
    "icon": "fa-cogs",
    "requiresAuth": true
  }
  ```
- **Cold-Start Resilience (`mfe_services.json`)**:
  `web-interface` persists the registry state to `mfe_services.json` on disk (`dbFile` in `registry.go`). When `web-interface` restarts, registered MFEs are available immediately without waiting for microservice re-registration loops.
- **Infinite Retry Registration Standard**:
  Client microservices must register using `spec.PublishWithLifecycle` (Go), `spec.publish_with_lifecycle` (Python), `spec::publish_with_lifecycle` (Rust), or `SpecPublisher::PublishWithLifecycle` (C++) from `microservice-toolbox`, which automatically enforces non-blocking background execution, exponential backoff (`MaxRetries: -1`), Docker Guard address resolution, and dynamic versioning from `VERSION.txt`.
- **Authoritative Exchange Contracts & No-Cache Assets**:
  Live Operations tabs (`.openmfe-tabs-bar` / `div[3]`) MUST render microservice-sourced Exchange Contracts via `window.BastienMFEContracts` (`OpenMFEContracts.js`) fetched from `GET /api/v1/contracts` (or registry fallback). Hardcoding mock `.proto`/`.capnp`/SQL schemas in `web-interface` or adding brittle `?v=` query strings to CSS URLs is strictly prohibited (`/static/` uses `Cache-Control: no-cache, must-revalidate`).

### 8. Interactive Network Visualization (Canvas/Vis.js)
- Build smooth stabilization progress screens ("Patience Loader") representing physics engine iteration. Skip loading screens automatically for organic hierarchical flows.
- Implement interactive double-click behaviors for node clustering (e.g. folding/unfolding class members).
- **Endpoint Portability**: Strictly prohibit hardcoded external domain strings for local resources. Derive all paths relatively. Dynamically resolve WebSockets based on location protocol:
  ```javascript
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/wsc`;
  ```
- **Robust Reconnection**: Automated WebSocket connection loops must implement an **exponential backoff** algorithm rather than fixed intervals to prevent endpoint flooding during outages.
- Handle cross-origin fetch/CORS policies gracefully. Prefer relative routes and fallback to sandbox-compliant scratch assets dynamically.

### 9. Code Style & Visual Dividers
- Separate classes, major components, and visual sections with exactly 80 visual equals divider lines:
  ```javascript
  // ============================================================================
  // [Section Name]
  // ============================================================================
  ```
- Use safe DOM selectors (`document.getElementById`) cached inside a single dictionary (e.g., `this.dom`) during initialization to optimize DOM query overhead.

## 🧪 BDD & Testing Alignment
- Align UI functionality with Gherkin scenarios defined in `02-Business-BDD`.
- Manually verify layout responsiveness, panel collapse synchronization, history stack traversal, and session isolation.
- Verify cross-browser compatibility across modern rendering engines.

---
*Reference: [[Global-Architecture-Rules]], [[Web-Interface-Hub]], [[Web-Interface-Integration-Protocol]], [[OpenMFE-Integration-Protocol]], [[Web-Interface-Page-Rendering]]*

