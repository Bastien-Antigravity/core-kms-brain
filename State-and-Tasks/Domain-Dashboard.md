# 🌐 Domain Ontology Matrix

This dashboard groups documentation and states based on **Transversal Themes** rather than what folder they physically live in. 

---

## 🔭 Domain: Observability
Includes all metrics, logging systems, and tracing mechanisms.
```dataview
table microservice, type
from ""
where contains(tags, "domain/observability")
```

## 📡 Domain: Networking & Transport
Includes everything related to sockets, TCP wrappers, and port topologies.
```dataview
table microservice, type
from ""
where contains(tags, "domain/networking")
```

## 🏗️ Domain: Architecture Systems
Rules governing repo structures, CI deployment, and internal designs.
```dataview
table microservice, type
from ""
where contains(tags, "domain/architecture")
```
