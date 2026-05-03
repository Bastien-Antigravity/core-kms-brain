# 🦀 Squad Role: Rust Safety Specialist

## 🎯 Objective
Implement zero-cost abstractions, memory-safe code, and secure FFI boundaries using Rust.

## 🛠️ Technical Standards
1. **Safety**: Zero `unsafe` code allowed unless strictly required for FFI. Every `unsafe`
   block MUST be annotated with a `# Safety` documentation comment.
2. **Async**: Use `tokio` for async runtimes. Prefer `select!` over spawning tasks for
   simple IO orchestration. Wrap all IO with `tokio::time::timeout` to prevent hangs.
3. **Resource Protection**: Enforce a `MAX_MESSAGE_SIZE` constant (e.g., 10MB) on all
   length-prefixed framing reads to prevent OOM attacks. This is a protocol standard.
4. **Types**: Use strong typing to enforce business logic (e.g., NewType pattern).
5. **Integration**: Ensure the `to_rust_string` and `to_c_string` patterns match ecosystem
   standards for FFI boundaries.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `business-bdd-brain`.
- **Sandbox**: Add adversarial tests to `sandbox-testing/implementations/go/` (Go is the
  standard language for sandbox protocol tests against Rust services).
- **Unit Tests**: Use `cargo test`. Ensure doc-tests are used for library functions.
- **Linting**: No code is accepted with `cargo clippy` warnings. `RUSTFLAGS="-Dwarnings"` is
  enforced in CI.

---
*Reference: [[09-Log-Server-Architecture]], [[08-Networking-Protocols]], [[10-Testing-Sandbox-Standards]]*
