# Test Agent Guidance

Prefer explicit Arrange/Act/Assert tests over shared fixture graphs.

- Keep setup local to the test when only one module needs it.
- Use `scenario.py` helpers only when multiple tests need the same seeded state.
- Compose scenarios from smaller scenario helpers instead of reviving shared `_data.py` modules.
- Seed only the entities a test actually exercises.
- After each refactor, run the narrowest pytest target that can falsify the change.
- Do not add new `_data.py` files under `backend/test`.
