# Test Agent Guidance

Prefer explicit Arrange/Act/Assert tests over shared fixture graphs.

When reducing slow test setup, refactor scenario dependencies from the leaves inward.

- Start with the scenario used directly by the test file you are editing.
- Remove imports of other scenarios when the current scenario only needs a small subset of their seeded entities.
- Duplicate only the entities and fields that the current test module actually uses, even if that creates some local redundancy.
- Keep each scenario self-sufficient: a reader should be able to understand all seeded state for that test module without opening another scenario file.
- Preserve act/assert behavior while changing arrange steps; if names must change, keep the test intent identical.
- After localizing one scenario, run that module's narrowest pytest target before moving to the next dependency edge.

- Keep setup local to the test when only one module needs it.
- Use `scenario.py` helpers only when multiple tests need the same seeded state.
- Compose scenarios from smaller scenario helpers instead of reviving shared `_data.py` modules.
- Seed only the entities a test actually exercises.
- After each refactor, run the narrowest pytest target that can falsify the change.
- Do not add new `_data.py` files under `backend/test`.
