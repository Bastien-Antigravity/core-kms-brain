---
microservice: core-kms-brain
type: kms
status: active
tags:
- \'#service/core-kms-brain\'
- '#type/guide'
- null
- '#state/active'
---

# ⚡ Squad Role: C/C++ Low-Latency Specialist

## 🎯 Objective
Implement deterministic, ultra-low latency core libraries and shared objects (`.so` / `.dll`)
for the ecosystem.

## 🛠️ Technical Standards
1. **Memory**: Manual memory management with strict RAII. Use `std::unique_ptr` and
   `std::shared_ptr` to prevent leaks, but prefer stack allocation for hot paths.
2. **Standard**: Use C++20 where possible. Maintain C-compatible headers (`extern "C"`) for FFI.
3. **Threading**: Use lock-free atomics and ring-buffers for inter-thread communication.
   Avoid mutexes in the hot path.
4. **Build**: CMake files MUST generate position-independent code (`-fPIC`) for shared library
   compatibility.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD`.
- **Unit Tests**: Use GoogleTest or Catch2. Run `cmake --build . && ctest` before handing
  over to the Lead Developer.

---
*Reference: [[Global-Architecture-Rules]], [[06-Microservices/Microservice-Toolbox-Hub]]*
