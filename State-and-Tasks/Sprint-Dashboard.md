# ⚡ Live Sprint Dashboard

> [!important] 🛠 Dataview Plugin Required
> If the tables below look like raw code blocks, it means Dataview is not running.
> **How to install:**
> 1. In Obsidian, click the **Settings (Gear Icon)** in the bottom left.
> 2. Go to **Community Plugins**.
> 3. Turn off "Restricted Mode".
> 4. Click **Browse** and search for **Dataview**.
> 5. Click **Install**, then wait, then click **Enable**.
> Once enabled, these tables will immediately render as dynamic databases!

---

## 📝 Active Tasks & Bugs
```dataview
table status, priority
from ""
where type = "task" or type = "bug"
where status = "active"
sort priority desc
```

## 🌐 Ecosystem Microservice States
```dataview
table status, last-updated
from ""
where type = "session-state"
sort last-updated desc
```

## 📐 Core Architecture Nodes
```dataview
table microservice
from ""
where type = "architecture"
sort file.name asc
```

## 📚 Ecosystem Libraries
```dataview
table microservice
from ""
where type = "reference"
sort file.name asc
```
