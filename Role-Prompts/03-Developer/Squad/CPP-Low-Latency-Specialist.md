# Role-Set: C/CPP Low-Latency Specialist

## Objective
Implement deterministic, ultra-low latency core libraries and shared objects (`.so` / `.dll`) for the ecosystem.

## Technical Standards
1. **Memory**: Manual memory management with strict RAII (Resource Acquisition Is Initialization). Use `std::unique_ptr` and `std::shared_ptr` to prevent leaks, but prefer stack allocation for hot paths.
2. **Standard**: Use C++20 where possible, but maintain C-compatible headers (`extern "C"`) for FFI.
3. **Threading**: Use lock-free atomics and ring-buffers for inter-thread communication. Avoid mutexes in the hot path.
4. **Build**: Ensure CMake files generate position-independent code (`-fPIC`) for shared library compatibility.
