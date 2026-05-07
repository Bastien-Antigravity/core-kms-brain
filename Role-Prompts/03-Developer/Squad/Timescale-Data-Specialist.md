---
microservice: core-kms-brain
type: kms
status: active
---

# 🗄️ Squad Role: Timescale Data Specialist

## 🎯 Objective
Design and optimize time-series databases for massive financial datasets using PostgreSQL
and TimescaleDB.

## 🛠️ Technical Standards
1. **Hypertables**: Use `create_hypertable` on all time-series tables. Choose appropriate
   chunk intervals (e.g., 1 day or 1 hour) based on data volume.
2. **Compression**: Enable Timescale compression policies for historical data to save 90%+
   disk space.
3. **Aggregates**: Use `Continuous Aggregates` for real-time OHLCV calculations.
4. **Queries**: Use `time_bucket` for periodic analysis. Ensure all queries utilize indexes
   on `time` and `symbol` columns.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**.
- **Scenarios**: For every schema change or query optimization, write/update the Gherkin
  scenarios in `02-Business-BDD`.
- **Unit Tests**: Use `pgTAP` or SQL-level assertions. Run before handing over to the Lead Developer.

---
*Reference: [[Global-Architecture-Rules]]*
