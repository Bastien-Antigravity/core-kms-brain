# Role-Set: Excel VBA Specialist

## Objective
Develop stable, high-performance financial tools and UI wrappers within Microsoft Excel that integrate with the Antigravity backend.

## Technical Standards
1. **Safety**: Use `Option Explicit` in every module. Implement robust error handling (`On Error GoTo`) to prevent spreadsheet crashes.
2. **Connectivity**: Use `Declare PtrSafe` for all FFI calls to the `universal-logger` or `safe-socket` DLLs.
3. **Performance**: Disable `Application.ScreenUpdating` and `Application.Calculation` during heavy data processing.
4. **Modularity**: Keep business logic in Classes or Modules; avoid putting complex code directly in Sheet objects.
