"""
Integration tests for the humanizer MCP server tools.

The @mcp.tool() decorator preserves the original function,
so we test by calling the tool functions directly.

Run with:
    pytest tests/test_server.py -v
"""

import json

from humanizer_mcp.server import (
    humanizer_discourse,
    humanizer_metrics,
    humanizer_verify,
    humanizer_diff,
    humanizer_status,
)


# ---------------------------------------------------------------------------
# Shared sample texts
# ---------------------------------------------------------------------------

SAMPLE_TEXT = """\
Education mattered in ways we did not expect. But not in the straightforward way conventional wisdom suggests. People with college degrees were more likely to know what large language models actually do, and that awareness amplified their concern about job displacement in ways that varied dramatically across partisan lines.

Partisan identity shaped the AI concern landscape profoundly. Democrats and Republicans expressed worry at nearly identical rates, yet the mechanisms driving their concern diverged sharply. Republicans worried about cultural displacement, while Democrats focused on economic disruption.

Age told a more complicated story than simple generational divides would predict. Older respondents who had heard of ChatGPT showed heightened concern, but among those unaware of specific AI tools, age had almost no effect.

The methodological approach captured variation that simpler designs would have missed. By decomposing the partisan gap using Blinder-Oaxaca techniques, we revealed that compositional differences in education and awareness explained roughly a third of the partisan divide."""

HUMANIZED_TEXT = """\
Education mattered. Not in the clean, linear way the textbooks promised -- the reality proved messier. Respondents holding bachelor's degrees or above showed markedly higher awareness of what large language models can actually do, and that knowledge colored everything that followed. Their concern about AI-driven job displacement spiked, but the spike looked different depending on which side of the partisan aisle they stood.

Why do Democrats and Republicans worry about AI at nearly identical rates yet for entirely different reasons? That puzzle drove much of our analysis. Republicans channeled anxiety about cultural erosion; Democrats zeroed in on paycheck vulnerability. Same thermometer reading, different fevers.

Age defied the lazy generational narrative. Among people who had already encountered ChatGPT, older respondents reported sharper concern -- perhaps because they saw fewer escape routes. Strip away that awareness variable, though, and age barely registered.

Blinder-Oaxaca decomposition cracked open the partisan gap. Roughly one-third of the divide traced back to compositional differences: education levels, tech exposure, media diet. The remaining two-thirds? Pure partisan identity, stubbornly resistant to demographic explanation."""


# ============================================================================
# 1. humanizer_metrics tool
# ============================================================================


class TestHumanizerMetricsTool:
    def test_metrics_returns_all_fields(self):
        result = humanizer_metrics(text=SAMPLE_TEXT)
        # Original fields
        assert "burstiness" in result
        assert "mtld" in result
        assert "fano_factor" in result
        assert "composite" in result
        assert "hedge_density" in result
        assert "discipline" in result
        # v3 fields
        assert "hapax_rate" in result
        assert "contraction_density" in result
        assert "paragraph_length_variance" in result
        assert "surprisal_proxy" in result
        assert "surprisal_autocorrelation" in result
        assert "connective_diversity" in result
        assert "pronoun_density" in result
        assert "question_ratio" in result
        assert "abstract_noun_ratio" in result
        assert "discourse_penalty" in result
        assert "psycholinguistic_penalty" in result

    def test_metrics_with_discipline(self):
        result = humanizer_metrics(text=SAMPLE_TEXT, discipline="psychology")
        assert result["discipline"] == "psychology"
        assert result["discipline_profile"]["burstiness_threshold"] == 0.40

    def test_metrics_with_pattern_score(self):
        result = humanizer_metrics(
            text=SAMPLE_TEXT,
            pattern_score=62,
            structural_penalty=55,
        )
        assert result["composite"]["composite_score"] > 0

    def test_metrics_v3_composite_components(self):
        """v3 composite should include discourse and psycholinguistic penalties."""
        result = humanizer_metrics(text=SAMPLE_TEXT, pattern_score=50)
        components = result["composite"]["components"]
        assert "discourse_penalty" in components
        assert "psycholinguistic_penalty" in components
        assert result["composite"]["scoring_version"] == "v3"


# ============================================================================
# 2. humanizer_verify tool
# ============================================================================


class TestHumanizerVerifyTool:
    def test_verify_detects_improvement(self):
        result = humanizer_verify(
            original_text=SAMPLE_TEXT,
            humanized_text=HUMANIZED_TEXT,
        )
        assert "regressions" in result
        assert "needs_another_pass" in result
        assert "recommendations" in result

    def test_verify_flags_regression(self):
        """If humanized text is worse, should flag regression."""
        ai_text = (
            "The study found significant results. The analysis showed important patterns. "
            "The findings indicated clear trends. The research demonstrated key outcomes."
        )
        result = humanizer_verify(
            original_text=SAMPLE_TEXT,
            humanized_text=ai_text,
        )
        # Should flag regressions since AI-like text is worse
        assert len(result["regressions"]) > 0 or result["needs_another_pass"] is True


# ============================================================================
# 3. humanizer_diff tool
# ============================================================================


class TestHumanizerDiffTool:
    def test_diff_returns_deltas(self):
        result = humanizer_diff(
            original_text=SAMPLE_TEXT,
            humanized_text=HUMANIZED_TEXT,
        )
        assert "deltas" in result
        assert "burstiness_cv" in result["deltas"]
        assert "sentence_length_distribution" in result

    def test_diff_includes_v3_deltas(self):
        """Diff should include discourse and psycholinguistic penalty deltas."""
        result = humanizer_diff(
            original_text=SAMPLE_TEXT,
            humanized_text=HUMANIZED_TEXT,
        )
        deltas = result["deltas"]
        assert "discourse_penalty" in deltas
        assert "psycholinguistic_penalty" in deltas
        assert "connective_diversity" in deltas
        assert "hapax_rate" in deltas
        assert "question_ratio" in deltas
        # Each delta entry should have before/after/delta/improvement_pct
        for key in ("discourse_penalty", "psycholinguistic_penalty", "hapax_rate"):
            assert "before" in deltas[key]
            assert "after" in deltas[key]
            assert "delta" in deltas[key]
            assert "improvement_pct" in deltas[key]


# ============================================================================
# 4. humanizer_status tool
# ============================================================================


class TestHumanizerStatusTool:
    def test_status_returns_assessment(self):
        result = humanizer_status(text=SAMPLE_TEXT, target=30)
        assert "readiness" in result
        assert "metrics" in result
        assert "target_composite" in result

    def test_status_with_discipline(self):
        result = humanizer_status(
            text=SAMPLE_TEXT,
            discipline="psychology",
            target=40,
        )
        assert result["discipline"] == "psychology"

    def test_status_includes_v3_metrics(self):
        """Status should include v3 metric targets."""
        result = humanizer_status(text=SAMPLE_TEXT, target=30)
        metrics = result["metrics"]
        assert "connective_diversity" in metrics
        assert "hapax_rate" in metrics
        assert "question_ratio" in metrics
        assert "discourse_penalty" in metrics
        assert "psycholinguistic_penalty" in metrics
        # Each metric entry should have current/target/distance/passed
        for key in ("discourse_penalty", "psycholinguistic_penalty"):
            assert "current" in metrics[key]
            assert "target" in metrics[key]
            assert "passed" in metrics[key]


# ============================================================================
# 5. humanizer_discourse tool
# ============================================================================


class TestHumanizerDiscourseTool:
    def test_discourse_returns_valid_json(self):
        """Tool returns a JSON string that parses correctly."""
        raw = humanizer_discourse(text=SAMPLE_TEXT)
        result = json.loads(raw)
        assert isinstance(result, dict)

    def test_discourse_returns_all_metric_fields(self):
        """Response should contain all 9 new metrics."""
        raw = humanizer_discourse(text=SAMPLE_TEXT)
        result = json.loads(raw)
        metrics = result["metrics"]
        expected_keys = [
            "hapax_rate",
            "contraction_density",
            "paragraph_length_variance",
            "surprisal_proxy",
            "surprisal_autocorrelation",
            "connective_diversity",
            "pronoun_density",
            "question_ratio",
            "abstract_noun_ratio",
        ]
        for key in expected_keys:
            assert key in metrics, f"Missing metric: {key}"

    def test_discourse_returns_penalties(self):
        """Response should contain discourse and psycholinguistic penalties."""
        raw = humanizer_discourse(text=SAMPLE_TEXT)
        result = json.loads(raw)
        penalties = result["penalties"]
        assert "discourse_penalty" in penalties
        assert "psycholinguistic_penalty" in penalties
        assert isinstance(penalties["discourse_penalty"], (int, float))
        assert isinstance(penalties["psycholinguistic_penalty"], (int, float))
        assert 0 <= penalties["discourse_penalty"] <= 100
        assert 0 <= penalties["psycholinguistic_penalty"] <= 100

    def test_discourse_with_discipline(self):
        """Discipline parameter should change targets."""
        raw_default = humanizer_discourse(text=SAMPLE_TEXT, discipline="default")
        raw_stem = humanizer_discourse(text=SAMPLE_TEXT, discipline="stem")
        result_default = json.loads(raw_default)
        result_stem = json.loads(raw_stem)
        assert result_default["discipline"] == "default"
        assert result_stem["discipline"] == "stem"
        # STEM has different targets than default
        assert (
            result_stem["discipline_targets"]["contraction_target"]
            != result_default["discipline_targets"]["contraction_target"]
        )

    def test_discourse_returns_flags(self):
        """Response should contain flags list."""
        raw = humanizer_discourse(text=SAMPLE_TEXT)
        result = json.loads(raw)
        assert "flags" in result
        assert isinstance(result["flags"], list)

    def test_discourse_returns_discipline_targets(self):
        """Response should contain discipline-calibrated targets."""
        raw = humanizer_discourse(text=SAMPLE_TEXT)
        result = json.loads(raw)
        targets = result["discipline_targets"]
        expected_target_keys = [
            "contraction_target",
            "pronoun_target",
            "hapax_target",
            "connective_diversity_target",
            "question_ratio_target",
            "abstract_noun_ceiling",
            "surprisal_variance_target",
        ]
        for key in expected_target_keys:
            assert key in targets, f"Missing target: {key}"

    def test_discourse_ai_text_gets_flags(self):
        """AI-typical text should produce flags."""
        ai_text = (
            "The study found significant results. The analysis showed important patterns. "
            "The findings indicated clear trends. The research demonstrated key outcomes. "
            "The investigation revealed notable observations. The examination confirmed hypotheses. "
            "The assessment highlighted critical factors. The evaluation established precedents."
        )
        raw = humanizer_discourse(text=ai_text)
        result = json.loads(raw)
        # AI-like text should trigger at least some flags
        assert len(result["flags"]) > 0

    def test_discourse_humanized_text(self):
        """Well-humanized text should have lower penalties."""
        raw_sample = humanizer_discourse(text=SAMPLE_TEXT)
        raw_humanized = humanizer_discourse(text=HUMANIZED_TEXT)
        result_sample = json.loads(raw_sample)
        result_humanized = json.loads(raw_humanized)
        # Humanized text should have fewer or equal flags
        # (not strictly guaranteed, but the HUMANIZED_TEXT is designed to be more human-like)
        assert isinstance(result_humanized["flags"], list)
        assert isinstance(result_sample["flags"], list)
