# thsensor

Simple smart sensor based on Raspberry Pi Pico 2 W, written in MicroPython.

## Testing

- Tests run with **pytest** via `uv run pytest`.
- Every test function follows the **AAA pattern** (Arrange / Act / Assert),
  with the three sections separated by `# Arrange`, `# Act`, `# Assert`
  comments and **exactly one assertion per test** (a single `pytest.raises`
  block counts as that assertion).
- Test function names follow the **given-when-then** naming scheme:
  `test_when_<condition>_then_<expected>` or, when setup context matters,
  `test_given_<context>_when_<condition>_then_<expected>`.
- Mirror the `src/` layout under `tests/` (e.g. `src/models/base.py` ->
  `tests/models/base/`).
