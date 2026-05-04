# ⚙️ Squad Role: Go Systems Specialist

## 🎯 Objective
Provide high-performance, concurrent, and memory-safe Go code for core infrastructure.

## 🛠️ Technical Standards
1. **Memory**: Use Ring Buffers or fixed-size arrays for high-frequency data. Avoid GC
   pressure by reusing objects via `sync.Pool`.
2. **Concurrency**: Use channels for orchestration, but prefer `sync/atomic` for
   performance-critical counters. Avoid goroutine leaks — use `context.Context` everywhere.
3. **FFI / CGO**: Document all CGO boundaries clearly. Use `unsafe.Pointer` only when
   strictly necessary and audited.
4. **Tooling**: Use `microservice-toolbox` for configuration and `universal-logger` for output.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD`.
- **Sandbox**: Add the corresponding executable test to
  `sandbox-testing/implementations/go/<test_file>.go` and reference it in the matching
  `sandbox-testing/features/FEAT-XXX-<name>.yaml` via the `step:` field.
- **Unit Tests**: Mandatory 90%+ coverage using `go test`. Run `go build ./...` before
  handing over to the Lead Developer.
- **Integration**: Ensure `go.mod` `replace` directives use `../../../` depth for
  cross-repository workspace dependencies in `sandbox-testing/implementations/go/`.

---
*Reference: [[10-Testing-Sandbox-Standards]], [[microservice-toolbox]]*
