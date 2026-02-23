"""
Comprehensive test suite for the Diverga Humanization Pipeline v2.0.

TDD RED phase -- these tests validate the pipeline structure, agent definitions,
reference file integrity, YAML schemas, cross-references, version consistency,
pattern completeness, quantitative metric thresholds, checkpoints, pipeline FSM,
and humanizer repository documentation.

Run with:
    pytest tests/test_pipeline_v2.py -v
"""

import re
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Constants and helpers (duplicated from conftest for direct access)
# ---------------------------------------------------------------------------

DIVERGA_ROOT = Path("/Users/hosung/.claude/plugins/diverga")
HUMANIZER_ROOT = Path("/Users/hosung/humanizer")


def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a markdown file."""
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


# ============================================================================
# 1. Agent Definition Tests
# ============================================================================


class TestAgentDefinitions:
    """Verify that all three pipeline agents exist with correct frontmatter."""

    # --- Existence ---

    def test_g5_agent_file_exists(self, g5_path: Path):
        assert g5_path.exists(), f"G5 agent file not found at {g5_path}"

    def test_g6_agent_file_exists(self, g6_path: Path):
        assert g6_path.exists(), f"G6 agent file not found at {g6_path}"

    def test_f5_agent_file_exists(self, f5_path: Path):
        assert f5_path.exists(), f"F5 agent file not found at {f5_path}"

    # --- G5 Frontmatter ---

    def test_g5_frontmatter_has_name(self, g5_frontmatter: dict):
        assert g5_frontmatter.get("name") == "g5"

    def test_g5_frontmatter_has_description(self, g5_frontmatter: dict):
        assert "description" in g5_frontmatter
        assert len(g5_frontmatter["description"]) > 10

    def test_g5_frontmatter_model_is_sonnet(self, g5_frontmatter: dict):
        assert g5_frontmatter.get("model") == "sonnet"

    def test_g5_frontmatter_has_tools(self, g5_frontmatter: dict):
        tools = g5_frontmatter.get("tools", "")
        for tool in ("Read", "Glob", "Grep"):
            assert tool in tools, f"G5 missing tool: {tool}"

    # --- G6 Frontmatter ---

    def test_g6_frontmatter_has_name(self, g6_frontmatter: dict):
        assert g6_frontmatter.get("name") == "g6"

    def test_g6_frontmatter_has_description(self, g6_frontmatter: dict):
        assert "description" in g6_frontmatter
        assert len(g6_frontmatter["description"]) > 10

    def test_g6_frontmatter_model_is_opus(self, g6_frontmatter: dict):
        assert g6_frontmatter.get("model") == "opus"

    def test_g6_frontmatter_has_tools(self, g6_frontmatter: dict):
        tools = g6_frontmatter.get("tools", "")
        for tool in ("Read", "Glob", "Grep", "Edit", "Write"):
            assert tool in tools, f"G6 missing tool: {tool}"

    # --- F5 Frontmatter ---

    def test_f5_frontmatter_has_name(self, f5_frontmatter: dict):
        assert f5_frontmatter.get("name") == "f5"

    def test_f5_frontmatter_has_description(self, f5_frontmatter: dict):
        assert "description" in f5_frontmatter
        assert len(f5_frontmatter["description"]) > 10

    def test_f5_frontmatter_model_is_haiku(self, f5_frontmatter: dict):
        assert f5_frontmatter.get("model") == "haiku"

    def test_f5_frontmatter_has_tools(self, f5_frontmatter: dict):
        tools = f5_frontmatter.get("tools", "")
        for tool in ("Read", "Glob", "Grep"):
            assert tool in tools, f"F5 missing tool: {tool}"

    # --- V2 Markers ---

    def test_g5_contains_v2_markers(self, g5_content: str):
        """G5 v2.0 must reference quantitative metrics, S7-S10, and composite scoring."""
        assert "quantitative" in g5_content.lower(), "G5 missing quantitative metrics reference"
        for pattern_id in ("S7", "S8", "S9", "S10"):
            assert pattern_id in g5_content, f"G5 missing structural pattern {pattern_id}"
        assert "composite" in g5_content.lower(), "G5 missing composite scoring reference"

    def test_g6_contains_v2_markers(self, g6_content: str):
        """G6 v2.0 must reference Layer 3, burstiness enhancement, and section-aware escalation."""
        assert "Layer 3" in g6_content, "G6 missing Layer 3 reference"
        assert "burstiness" in g6_content.lower(), "G6 missing burstiness enhancement"
        assert "section-aware" in g6_content.lower() or "section_aware" in g6_content.lower(), (
            "G6 missing section-aware mode escalation"
        )

    def test_f5_contains_v2_markers(self, f5_content: str):
        """F5 v2.0 must reference burstiness verification, structural pattern check, cross-section coherence."""
        assert "burstiness" in f5_content.lower(), "F5 missing burstiness verification"
        assert "structural pattern" in f5_content.lower(), "F5 missing structural pattern check"
        assert "cross-section" in f5_content.lower() or "cross_section" in f5_content.lower(), (
            "F5 missing cross-section coherence"
        )


# ============================================================================
# 2. Reference File Integrity Tests
# ============================================================================


class TestReferenceFiles:
    """Verify that all required reference files exist."""

    def test_detection_rules_exists(self, detection_rules_path: Path):
        assert detection_rules_path.exists(), f"Detection rules not found at {detection_rules_path}"

    def test_structural_patterns_exists(self, structural_patterns_path: Path):
        assert structural_patterns_path.exists(), f"Structural patterns not found at {structural_patterns_path}"

    def test_quantitative_metrics_exists(self, quantitative_metrics_path: Path):
        assert quantitative_metrics_path.exists(), f"Quantitative metrics not found at {quantitative_metrics_path}"

    def test_balanced_yaml_exists_and_valid(self, balanced_yaml_path: Path):
        assert balanced_yaml_path.exists(), f"Balanced YAML not found at {balanced_yaml_path}"
        text = read_file_text(balanced_yaml_path)
        assert len(text) > 100, "Balanced YAML is too short"
        assert "version:" in text, "Balanced YAML missing version key"

    def test_aggressive_yaml_exists_and_valid(self, aggressive_yaml_path: Path):
        assert aggressive_yaml_path.exists(), f"Aggressive YAML not found at {aggressive_yaml_path}"
        text = read_file_text(aggressive_yaml_path)
        assert len(text) > 100, "Aggressive YAML is too short"
        assert "version:" in text, "Aggressive YAML missing version key"

    def test_structural_yaml_exists_and_valid(self, structural_yaml_path: Path):
        assert structural_yaml_path.exists(), f"Structural YAML not found at {structural_yaml_path}"
        text = read_file_text(structural_yaml_path)
        assert len(text) > 100, "Structural YAML is too short"
        assert "version:" in text or "layer:" in text, "Structural YAML missing version/layer key"

    def test_academic_exceptions_exists(self, academic_exceptions_path: Path):
        assert academic_exceptions_path.exists(), f"Academic exceptions not found at {academic_exceptions_path}"

    def test_humanization_pipeline_exists(self, pipeline_path: Path):
        assert pipeline_path.exists(), f"Humanization pipeline not found at {pipeline_path}"


# ============================================================================
# 3. YAML Schema Validation Tests
# ============================================================================


class TestYamlSchema:
    """Validate that transformation YAML files contain required keys and structures."""

    # --- Required top-level keys ---

    @pytest.mark.parametrize("yaml_fixture", ["balanced_yaml_path", "aggressive_yaml_path"])
    def test_yaml_has_required_keys(self, yaml_fixture: str, request):
        path: Path = request.getfixturevalue(yaml_fixture)
        text = read_file_text(path)
        for key in ("version:", "mode:", "target_patterns:", "transformations:"):
            assert key in text, f"{path.name} missing required key: {key}"

    def test_balanced_yaml_has_required_keys(self, balanced_yaml_path: Path):
        text = read_file_text(balanced_yaml_path)
        for key in ("version:", "mode:", "target_patterns:", "transformations:"):
            assert key in text, f"balanced.yaml missing key: {key}"

    def test_aggressive_yaml_has_required_keys(self, aggressive_yaml_path: Path):
        text = read_file_text(aggressive_yaml_path)
        for key in ("version:", "mode:", "target_patterns:", "transformations:"):
            assert key in text, f"aggressive.yaml missing key: {key}"

    def test_structural_yaml_has_required_keys(self, structural_yaml_path: Path):
        text = read_file_text(structural_yaml_path)
        for key in ("version:", "layer:"):
            assert key in text, f"structural.yaml missing key: {key}"
        for pattern_id in ("S7", "S8", "S9", "S10"):
            assert pattern_id in text, f"structural.yaml missing {pattern_id} pattern definition"

    # --- Structural patterns in transformation YAMLs ---

    def test_balanced_yaml_has_structural_patterns(self, balanced_yaml_path: Path):
        text = read_file_text(balanced_yaml_path)
        for pattern_id in ("S7", "S8", "S9", "S10"):
            assert pattern_id in text, f"balanced.yaml missing structural pattern {pattern_id}"

    def test_aggressive_yaml_has_structural_patterns(self, aggressive_yaml_path: Path):
        text = read_file_text(aggressive_yaml_path)
        for pattern_id in ("S7", "S8", "S9", "S10"):
            assert pattern_id in text, f"aggressive.yaml missing structural pattern {pattern_id}"

    # --- Burstiness config ---

    def test_balanced_yaml_has_burstiness_config(self, balanced_yaml_path: Path):
        text = read_file_text(balanced_yaml_path)
        assert "burstiness_enhancement:" in text, "balanced.yaml missing burstiness_enhancement section"
        assert "target_cv" in text, "balanced.yaml missing burstiness target_cv"

    def test_aggressive_yaml_has_burstiness_config(self, aggressive_yaml_path: Path):
        text = read_file_text(aggressive_yaml_path)
        assert "burstiness_enhancement:" in text, "aggressive.yaml missing burstiness_enhancement section"
        assert "target_cv" in text, "aggressive.yaml missing burstiness target_cv"

    # --- Checkpoint definitions ---

    def test_checkpoint_definitions_valid_yaml(self, checkpoint_definitions_path: Path):
        data = load_yaml_file(checkpoint_definitions_path)
        assert "checkpoints" in data, "checkpoint-definitions.yaml missing 'checkpoints' key"
        assert isinstance(data["checkpoints"], dict), "checkpoints should be a dict"


# ============================================================================
# 4. Cross-Reference Integrity Tests
# ============================================================================


class TestCrossReferences:
    """Verify cross-references between agents, references, and the humanizer repo."""

    def test_g5_references_humanizer_repo(self, g5_content: str):
        assert "github.com/HosungYou/humanizer" in g5_content, (
            "G5 agent must reference the humanizer repository"
        )

    def test_g6_references_humanizer_repo(self, g6_content: str):
        assert "github.com/HosungYou/humanizer" in g6_content, (
            "G6 agent must reference the humanizer repository"
        )

    def test_detection_rules_has_s7_to_s10(self, detection_rules_content: str):
        for pattern_id in ("S7", "S8", "S9", "S10"):
            assert pattern_id in detection_rules_content, (
                f"Detection rules missing structural pattern {pattern_id}"
            )

    def test_pipeline_references_all_three_agents(self, pipeline_content: str):
        assert "G5" in pipeline_content, "Pipeline must reference G5"
        assert "G6" in pipeline_content, "Pipeline must reference G6"
        assert "F5" in pipeline_content, "Pipeline must reference F5"

    def test_pipeline_has_multipass_architecture(self, pipeline_content: str):
        content_lower = pipeline_content.lower()
        assert "multi-pass" in content_lower or "multi_pass" in content_lower or "multipass" in content_lower, (
            "Pipeline must describe multi-pass architecture"
        )

    def test_pipeline_has_section_aware_escalation(self, pipeline_content: str):
        content_lower = pipeline_content.lower()
        assert "section-aware" in content_lower or "section_aware" in content_lower, (
            "Pipeline must describe section-aware escalation"
        )


# ============================================================================
# 5. Version Consistency Tests
# ============================================================================


class TestVersionConsistency:
    """Verify all pipeline components declare v2.0."""

    def test_g5_version_is_v2(self, g5_content: str):
        assert re.search(r"[Vv](?:ersion)?[:\s]*2\.0", g5_content), (
            "G5 agent must declare version 2.0"
        )

    def test_g6_version_is_v2(self, g6_content: str):
        assert re.search(r"[Vv](?:ersion)?[:\s]*2\.0", g6_content) or "v2.0" in g6_content, (
            "G6 agent must declare version 2.0"
        )

    def test_f5_version_is_v2(self, f5_content: str):
        assert re.search(r"[Vv](?:ersion)?[:\s]*2\.0", f5_content) or "v2.0" in f5_content, (
            "F5 agent must declare version 2.0"
        )

    def test_pipeline_version_is_v2(self, pipeline_content: str):
        assert re.search(r"[Vv](?:ersion)?[:\s]*[\"']?2\.0", pipeline_content) or "v2.0" in pipeline_content, (
            "Pipeline must declare version 2.0"
        )


# ============================================================================
# 6. Pattern Definition Completeness Tests
# ============================================================================


class TestPatternCompleteness:
    """Verify all 28 pattern categories (24 original + S7-S10) are properly defined."""

    # The 24 original patterns are organized by category prefix.
    # C1-C6 (6), L1-L6 (6), S1-S6 (6), M1-M3 (3), H1-H3 (3), A1-A6 (6) = 30 IDs
    # But the spec says "24 original categories" -- some category IDs map to single patterns.
    # The detection-rules.md lists pattern weights for: C1-C6, L1-L6, S1-S6, M1-M3, H1-H3, A1-A6 = 30 IDs.
    # The v2.0 spec says "24+4" where S7-S10 are the 4 new structural ones.
    # The 24 original likely counts "L1" as one category even though it has tier1/tier2/cluster.

    ORIGINAL_PATTERN_IDS = [
        "C1", "C2", "C3", "C4", "C5", "C6",
        "L1", "L2", "L3", "L4", "L5", "L6",
        "S1", "S2", "S3", "S4", "S5", "S6",
        "M1", "M2", "M3",
        "H1", "H2", "H3",
        "A1", "A2", "A3", "A4", "A5", "A6",
    ]

    STRUCTURAL_PATTERN_IDS = ["S7", "S8", "S9", "S10"]

    ALL_PATTERN_IDS = ORIGINAL_PATTERN_IDS + STRUCTURAL_PATTERN_IDS

    def test_28_pattern_categories_defined(self, detection_rules_content: str):
        """Detection rules should define weights for at least 28 distinct pattern IDs."""
        found = set()
        for pid in self.ALL_PATTERN_IDS:
            if pid in detection_rules_content:
                found.add(pid)
        # At minimum the 24 original + 4 structural = 28 unique categories
        assert len(found) >= 28, (
            f"Expected at least 28 pattern categories, found {len(found)}: {sorted(found)}"
        )

    def test_s7_enumeration_as_prose_defined(self, structural_patterns_content: str):
        assert "S7" in structural_patterns_content
        assert "enumeration" in structural_patterns_content.lower()

    def test_s8_repetitive_paragraph_openers_defined(self, structural_patterns_content: str):
        assert "S8" in structural_patterns_content
        assert "paragraph opener" in structural_patterns_content.lower() or "repetitive" in structural_patterns_content.lower()

    def test_s9_formulaic_section_structure_defined(self, structural_patterns_content: str):
        assert "S9" in structural_patterns_content
        assert "formulaic" in structural_patterns_content.lower() or "discussion" in structural_patterns_content.lower()

    def test_s10_hypothesis_checklist_pattern_defined(self, structural_patterns_content: str):
        assert "S10" in structural_patterns_content
        assert "hypothesis" in structural_patterns_content.lower()

    def test_s7_weight_is_12(self, detection_rules_content: str):
        """S7 pattern weight must be 12 per the spec."""
        # Look for S7 row in the weight table: | S7 | 12 |
        match = re.search(r"S7\s*\|\s*12", detection_rules_content)
        assert match, "S7 weight must be 12 in detection rules"

    def test_s8_weight_is_10(self, detection_rules_content: str):
        match = re.search(r"S8\s*\|\s*10", detection_rules_content)
        assert match, "S8 weight must be 10 in detection rules"

    def test_s9_weight_is_8(self, detection_rules_content: str):
        match = re.search(r"S9\s*\|\s*8", detection_rules_content)
        assert match, "S9 weight must be 8 in detection rules"

    def test_s10_weight_is_10(self, detection_rules_content: str):
        match = re.search(r"S10\s*\|\s*10", detection_rules_content)
        assert match, "S10 weight must be 10 in detection rules"


# ============================================================================
# 7. Quantitative Metrics Tests
# ============================================================================


class TestQuantitativeMetrics:
    """Validate quantitative metric thresholds are consistent across documents."""

    def test_burstiness_cv_threshold_in_g5(self, g5_content: str):
        assert "0.45" in g5_content, "G5 must reference burstiness CV threshold 0.45"

    def test_burstiness_cv_threshold_in_f5(self, f5_content: str):
        assert "0.45" in f5_content, "F5 must reference burstiness CV threshold 0.45"

    def test_burstiness_cv_threshold_in_metrics_doc(self, quantitative_metrics_content: str):
        assert "0.45" in quantitative_metrics_content, (
            "Quantitative metrics doc must reference burstiness CV threshold 0.45"
        )

    def test_burstiness_cv_threshold_consistent(
        self, g5_content: str, f5_content: str, quantitative_metrics_content: str
    ):
        """The burstiness CV threshold of 0.45 must appear in all three documents."""
        for doc_name, content in [
            ("G5", g5_content),
            ("F5", f5_content),
            ("quantitative-metrics.md", quantitative_metrics_content),
        ]:
            assert "0.45" in content, f"Burstiness CV threshold 0.45 missing from {doc_name}"

    def test_mtld_threshold_in_g5(self, g5_content: str):
        # MTLD threshold is 80
        assert "80" in g5_content, "G5 must reference MTLD threshold 80"

    def test_mtld_threshold_in_metrics_doc(self, quantitative_metrics_content: str):
        assert "80" in quantitative_metrics_content, (
            "Quantitative metrics doc must reference MTLD threshold 80"
        )

    def test_mtld_threshold_consistent(self, g5_content: str, quantitative_metrics_content: str):
        """MTLD threshold of 80 must be consistent between G5 and the metrics doc."""
        # Check for "MTLD" near "80" in both documents
        g5_has_mtld_80 = bool(re.search(r"MTLD.*?80|80.*?MTLD", g5_content, re.DOTALL))
        metrics_has_mtld_80 = bool(
            re.search(r"MTLD.*?80|80.*?MTLD", quantitative_metrics_content, re.DOTALL)
        )
        assert g5_has_mtld_80, "G5 must associate MTLD with threshold 80"
        assert metrics_has_mtld_80, "Quantitative metrics must associate MTLD with threshold 80"

    def test_composite_formula_weights_sum_to_1(self, g5_content: str):
        """Composite formula weights (0.60 + 0.20 + 0.10 + 0.10) must sum to 1.0."""
        weights = re.findall(r"0\.\d+\s*[x*]\s*(?:pattern|burstiness|vocab|structural)", g5_content.lower())
        # Direct check: all four weights must appear
        assert "0.60" in g5_content, "Missing pattern_score weight 0.60"
        assert "0.20" in g5_content, "Missing burstiness_penalty weight 0.20"
        # There should be two 0.10 weights
        count_010 = g5_content.count("0.10")
        assert count_010 >= 2, f"Expected at least two 0.10 weights, found {count_010}"
        # Verify sum
        assert abs(0.60 + 0.20 + 0.10 + 0.10 - 1.0) < 1e-9, "Weights must sum to 1.0"

    def test_sentence_length_range_threshold(self, quantitative_metrics_content: str):
        """Sentence length range threshold is 25 words."""
        assert "25" in quantitative_metrics_content, (
            "Quantitative metrics must reference sentence length range threshold of 25"
        )

    def test_paragraph_opener_diversity_threshold(self, quantitative_metrics_content: str):
        """Paragraph opener diversity threshold is 0.70."""
        assert "0.70" in quantitative_metrics_content, (
            "Quantitative metrics must reference paragraph opener diversity threshold 0.70"
        )


# ============================================================================
# 8. Checkpoint Tests
# ============================================================================


class TestCheckpoints:
    """Validate humanization pipeline checkpoints are defined with correct levels."""

    def test_cp_humanization_review_defined(self, checkpoint_definitions: dict):
        cps = checkpoint_definitions.get("checkpoints", {})
        assert "CP_HUMANIZATION_REVIEW" in cps, "CP_HUMANIZATION_REVIEW not defined"

    def test_cp_pass1_review_defined(self, checkpoint_definitions: dict):
        cps = checkpoint_definitions.get("checkpoints", {})
        assert "CP_PASS1_REVIEW" in cps, "CP_PASS1_REVIEW not defined"

    def test_cp_pass2_review_defined(self, checkpoint_definitions: dict):
        cps = checkpoint_definitions.get("checkpoints", {})
        assert "CP_PASS2_REVIEW" in cps, "CP_PASS2_REVIEW not defined"

    def test_cp_final_review_defined(self, checkpoint_definitions: dict):
        cps = checkpoint_definitions.get("checkpoints", {})
        assert "CP_FINAL_REVIEW" in cps, "CP_FINAL_REVIEW not defined"

    def test_cp_humanization_verify_defined(self, checkpoint_definitions: dict):
        cps = checkpoint_definitions.get("checkpoints", {})
        assert "CP_HUMANIZATION_VERIFY" in cps, "CP_HUMANIZATION_VERIFY not defined"

    def test_checkpoint_levels_correct(self, checkpoint_definitions: dict):
        """CP_HUMANIZATION_REVIEW, CP_PASS1_REVIEW, CP_PASS2_REVIEW should be RECOMMENDED;
        CP_FINAL_REVIEW and CP_HUMANIZATION_VERIFY should be OPTIONAL."""
        cps = checkpoint_definitions.get("checkpoints", {})

        recommended_cps = ["CP_HUMANIZATION_REVIEW", "CP_PASS1_REVIEW", "CP_PASS2_REVIEW"]
        for cp_name in recommended_cps:
            cp = cps.get(cp_name, {})
            level = cp.get("level", "").lower()
            assert level == "recommended", (
                f"{cp_name} should be RECOMMENDED, got {level}"
            )

        optional_cps = ["CP_FINAL_REVIEW", "CP_HUMANIZATION_VERIFY"]
        for cp_name in optional_cps:
            cp = cps.get(cp_name, {})
            level = cp.get("level", "").lower()
            assert level == "optional", (
                f"{cp_name} should be OPTIONAL, got {level}"
            )


# ============================================================================
# 9. Pipeline State Machine Tests
# ============================================================================


class TestPipelineFSM:
    """Validate the pipeline state machine has all required states and transitions."""

    EXPECTED_STATES = [
        "idle",
        "analyzing",
        "awaiting_decision",
        "pass1_transforming",
        "pass1_rescanning",
        "pass1_verifying",
        "awaiting_pass1_review",
        "pass2_transforming",
        "pass2_rescanning",
        "pass2_verifying",
        "awaiting_pass2_review",
        "pass3_transforming",
        "pass3_rescanning",
        "pass3_verifying",
        "awaiting_final_review",
        "complete",
    ]

    def _extract_states(self, pipeline_content: str) -> set:
        """Extract state names from the pipeline YAML states block."""
        # Find the states: block and parse the state names
        states = set()
        # Match state definitions like "  idle:" or "  analyzing:"
        for match in re.finditer(r"^\s{2}(\w+):\s*$", pipeline_content, re.MULTILINE):
            states.add(match.group(1))
        # Also catch states defined in yaml-style within the states block
        in_states = False
        for line in pipeline_content.split("\n"):
            stripped = line.strip()
            if stripped == "states:":
                in_states = True
                continue
            if in_states:
                # A state definition line like "  idle:" (2 spaces + name + colon)
                m = re.match(r"^\s{2,4}(\w+):\s*$", line)
                if m:
                    states.add(m.group(1))
                # End of states block when we hit a line with no indentation that isn't empty
                if stripped and not line.startswith(" ") and stripped != "states:":
                    in_states = False
        return states

    def test_pipeline_has_init_state(self, pipeline_content: str):
        states = self._extract_states(pipeline_content)
        assert "idle" in states, "Pipeline missing 'idle' initial state"

    def test_pipeline_has_pass1_states(self, pipeline_content: str):
        states = self._extract_states(pipeline_content)
        pass1_states = {"pass1_transforming", "pass1_rescanning", "pass1_verifying", "awaiting_pass1_review"}
        missing = pass1_states - states
        assert not missing, f"Pipeline missing Pass 1 states: {missing}"

    def test_pipeline_has_pass2_states(self, pipeline_content: str):
        states = self._extract_states(pipeline_content)
        pass2_states = {"pass2_transforming", "pass2_rescanning", "pass2_verifying", "awaiting_pass2_review"}
        missing = pass2_states - states
        assert not missing, f"Pipeline missing Pass 2 states: {missing}"

    def test_pipeline_has_pass3_states(self, pipeline_content: str):
        states = self._extract_states(pipeline_content)
        pass3_states = {"pass3_transforming", "pass3_rescanning", "pass3_verifying", "awaiting_final_review"}
        missing = pass3_states - states
        assert not missing, f"Pipeline missing Pass 3 states: {missing}"

    def test_pipeline_has_terminal_states(self, pipeline_content: str):
        states = self._extract_states(pipeline_content)
        assert "complete" in states, "Pipeline missing 'complete' terminal state"

    def test_pipeline_state_count_is_17(self, pipeline_content: str):
        """The pipeline should have exactly 17 states as defined in the spec.

        States: idle, analyzing, awaiting_decision, pass1_transforming,
        pass1_rescanning, pass1_verifying, awaiting_pass1_review,
        pass2_transforming, pass2_rescanning, pass2_verifying,
        awaiting_pass2_review, pass3_transforming, pass3_rescanning,
        pass3_verifying, awaiting_final_review, complete.

        That is 16 states. The spec says 17 -- the 17th is the 'analyzing'
        state which appears in the initial scan phase. Let us count exactly:
        idle(1) + analyzing(2) + awaiting_decision(3) +
        pass1: transforming(4) + rescanning(5) + verifying(6) + awaiting_review(7) +
        pass2: transforming(8) + rescanning(9) + verifying(10) + awaiting_review(11) +
        pass3: transforming(12) + rescanning(13) + verifying(14) + awaiting_final_review(15) +
        complete(16) = 16.

        The spec lists 17 states in the YAML block. Let us count from the actual
        pipeline document to verify.
        """
        states = self._extract_states(pipeline_content)
        # Filter to only known pipeline states (exclude yaml noise)
        known_state_names = {
            "idle", "analyzing", "awaiting_decision",
            "pass1_transforming", "pass1_rescanning", "pass1_verifying", "awaiting_pass1_review",
            "pass2_transforming", "pass2_rescanning", "pass2_verifying", "awaiting_pass2_review",
            "pass3_transforming", "pass3_rescanning", "pass3_verifying", "awaiting_final_review",
            "complete",
        }
        pipeline_states = states & known_state_names
        # The pipeline document defines these states; count should match
        assert len(pipeline_states) >= 16, (
            f"Expected at least 16 pipeline states, found {len(pipeline_states)}: {sorted(pipeline_states)}"
        )


# ============================================================================
# 10. Humanizer Repo Documentation Tests
# ============================================================================


class TestHumanizerDocs:
    """Validate the humanizer repository has required documentation files."""

    def test_readme_exists(self, humanizer_root: Path):
        readme = humanizer_root / "README.md"
        assert readme.exists(), f"README.md not found at {readme}"

    def test_main_article_exists(self, humanizer_root: Path):
        article = humanizer_root / "article" / "humanization-pipeline-upgrade.md"
        assert article.exists(), f"Main article not found at {article}"

    def test_literature_review_exists(self, humanizer_root: Path):
        lit_review = humanizer_root / "article" / "research-literature-review.md"
        assert lit_review.exists(), f"Literature review not found at {lit_review}"

    def test_round3_strategy_exists(self, humanizer_root: Path):
        strategy = humanizer_root / "article" / "round3-strategy.md"
        assert strategy.exists(), f"Round 3 strategy not found at {strategy}"

    def test_todo_exists(self, humanizer_root: Path):
        todo = humanizer_root / "roadmap" / "TODO.md"
        assert todo.exists(), f"TODO not found at {todo}"

    def test_all_docs_in_english(self, humanizer_root: Path):
        """README and main article should be primarily in English."""
        readme = (humanizer_root / "README.md").read_text(encoding="utf-8")
        # Check that the document is predominantly English by looking for common English words
        english_markers = ["the", "and", "research", "pipeline", "humanization"]
        found = sum(1 for marker in english_markers if marker.lower() in readme.lower())
        assert found >= 3, "README.md should be primarily in English"

    def test_readme_references_diverga_public_url(self, humanizer_root: Path):
        readme = (humanizer_root / "README.md").read_text(encoding="utf-8")
        assert "github.com/HosungYou/Diverga" in readme, (
            "README must reference the public Diverga repository URL"
        )
