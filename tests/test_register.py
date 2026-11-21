"""The 'not simulated' register is a shipped component, not a
nice-to-have: these tests fail if it disappears or loses an entry."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REQUIRED_ENTRIES = [
    "No real LLM",
    "No tool use or side effects",
    "No multi-turn conversation",
    "No multi-agent interaction",
    "One domain, two twins, one asset",
    "Static dependency states",
    "Whole-document grid staleness",
    "Timestamps are trusted",
    "Declared, not learned, contradictions",
    "Three scripted question styles",
    "Deterministic seeds",
    "No cost or latency model",
]


def test_register_exists_with_every_entry():
    text = (REPO / "NOT_SIMULATED.md").read_text(encoding="utf-8")
    for entry in REQUIRED_ENTRIES:
        assert entry in text, f"register lost its entry: {entry}"


def test_readme_points_at_the_register():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "NOT_SIMULATED.md" in readme
