"""
Shared fixtures for Diverga Humanization Pipeline v2.0 test suite.
"""

import re
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Root directory fixtures
# ---------------------------------------------------------------------------

DIVERGA_ROOT = Path("/Users/hosung/.claude/plugins/diverga")
HUMANIZER_ROOT = Path("/Users/hosung/humanizer")


@pytest.fixture
def diverga_root() -> Path:
    return DIVERGA_ROOT


@pytest.fixture
def humanizer_root() -> Path:
    return HUMANIZER_ROOT


# ---------------------------------------------------------------------------
# Agent file fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def g5_path(diverga_root: Path) -> Path:
    return diverga_root / "agents" / "g5.md"


@pytest.fixture
def g6_path(diverga_root: Path) -> Path:
    return diverga_root / "agents" / "g6.md"


@pytest.fixture
def f5_path(diverga_root: Path) -> Path:
    return diverga_root / "agents" / "f5.md"


# ---------------------------------------------------------------------------
# Reference file fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def detection_rules_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g5" / "detection-rules.md"


@pytest.fixture
def structural_patterns_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g5" / "structural-patterns.md"


@pytest.fixture
def quantitative_metrics_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g5" / "quantitative-metrics.md"


@pytest.fixture
def balanced_yaml_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g6" / "transformations" / "balanced.yaml"


@pytest.fixture
def aggressive_yaml_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g6" / "transformations" / "aggressive.yaml"


@pytest.fixture
def structural_yaml_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g6" / "transformations" / "structural.yaml"


@pytest.fixture
def academic_exceptions_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "references" / "agents" / "g6" / "academic-exceptions.md"


@pytest.fixture
def pipeline_path(diverga_root: Path) -> Path:
    return (
        diverga_root
        / ".claude"
        / "references"
        / "agents"
        / "research-coordinator"
        / "core"
        / "humanization-pipeline.md"
    )


@pytest.fixture
def checkpoint_definitions_path(diverga_root: Path) -> Path:
    return diverga_root / ".claude" / "checkpoints" / "checkpoint-definitions.yaml"


# ---------------------------------------------------------------------------
# Content reader helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a markdown file (content between first two '---' lines)."""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def read_file_text(path: Path) -> str:
    """Read a file and return its full text content."""
    return path.read_text(encoding="utf-8")


def load_yaml_file(path: Path) -> dict:
    """Load a YAML file, tolerating comment-only preambles before the first key."""
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) or {}


@pytest.fixture
def g5_content(g5_path: Path) -> str:
    return read_file_text(g5_path)


@pytest.fixture
def g6_content(g6_path: Path) -> str:
    return read_file_text(g6_path)


@pytest.fixture
def f5_content(f5_path: Path) -> str:
    return read_file_text(f5_path)


@pytest.fixture
def g5_frontmatter(g5_content: str) -> dict:
    return parse_frontmatter(g5_content)


@pytest.fixture
def g6_frontmatter(g6_content: str) -> dict:
    return parse_frontmatter(g6_content)


@pytest.fixture
def f5_frontmatter(f5_content: str) -> dict:
    return parse_frontmatter(f5_content)


@pytest.fixture
def pipeline_content(pipeline_path: Path) -> str:
    return read_file_text(pipeline_path)


@pytest.fixture
def pipeline_frontmatter(pipeline_content: str) -> dict:
    return parse_frontmatter(pipeline_content)


@pytest.fixture
def detection_rules_content(detection_rules_path: Path) -> str:
    return read_file_text(detection_rules_path)


@pytest.fixture
def structural_patterns_content(structural_patterns_path: Path) -> str:
    return read_file_text(structural_patterns_path)


@pytest.fixture
def quantitative_metrics_content(quantitative_metrics_path: Path) -> str:
    return read_file_text(quantitative_metrics_path)


@pytest.fixture
def checkpoint_definitions(checkpoint_definitions_path: Path) -> dict:
    return load_yaml_file(checkpoint_definitions_path)
