"""
Integration tests for the humanizer MCP server tools.

The @mcp.tool() decorator preserves the original function,
so we test by calling the tool functions directly.

Run with:
    pytest tests/test_server.py -v
"""

import json

from humanizer_mcp.server import (
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
        assert "burstiness" in result
        assert "mtld" in result
        assert "fano_factor" in result
        assert "composite" in result
        assert "hedge_density" in result
        assert "discipline" in result

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
