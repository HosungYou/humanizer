"""
Unit tests for humanizer_mcp.metrics — stylometric metric functions.

Run with:
    pytest tests/test_metrics.py -v
"""

from humanizer_mcp.metrics import (
    compute_burstiness,
    compute_mtld,
    compute_fano_factor,
    compute_sentence_length_range,
    compute_paragraph_opener_diversity,
    compute_composite_score,
    compute_hedge_density,
    compute_all_metrics,
    get_discipline_profile,
)


# ============================================================================
# 1. Burstiness (CV of sentence lengths)
# ============================================================================


class TestBurstiness:
    def test_high_cv_text(self):
        """High burstiness text should have CV > 0.45."""
        # Sentence lengths: 2, 9, 35 -> high CV
        text = (
            "Education mattered. But not in the straightforward way we expected. "
            "People with college degrees were more likely to know what large language "
            "models actually do, and that awareness amplified their concern about job "
            "displacement in ways that varied dramatically across partisan lines."
        )
        result = compute_burstiness(text)
        assert result["cv"] > 0.45
        assert result["penalty"] == 0
        assert result["label"] in ("High burstiness", "Normal burstiness")

    def test_low_cv_text(self):
        """Low burstiness text should have CV < 0.35."""
        text = (
            "Education was positively associated with concern about AI. "
            "Higher educational attainment predicted greater awareness of AI capabilities. "
            "The relationship between education and concern was moderated by partisan identity. "
            "These findings suggest that educational effects operate differently across political contexts."
        )
        result = compute_burstiness(text)
        assert result["cv"] < 0.35
        assert result["penalty"] > 0
        assert result["label"] in ("Very low burstiness", "Low burstiness", "Minimal burstiness")

    def test_non_native_calibration(self):
        """Non-native threshold should be 0.35 instead of 0.45."""
        text = (
            "The study examined AI concerns. Results showed education matters for awareness. "
            "Partisan identity played a significant moderating role. "
            "Age interacted with technology awareness in complex ways. "
            "These patterns suggest differential effects across groups."
        )
        result_default = compute_burstiness(text, non_native=False)
        result_nn = compute_burstiness(text, non_native=True)
        # Non-native should have lower or equal penalty
        assert result_nn["penalty"] <= result_default["penalty"]

    def test_empty_text(self):
        result = compute_burstiness("")
        assert result["cv"] == 0
        assert result["penalty"] == 0

    def test_single_sentence(self):
        result = compute_burstiness("This is a single sentence with enough words.")
        assert result["cv"] == 0
        assert result["sentence_count"] <= 1


# ============================================================================
# 2. MTLD (Measure of Textual Lexical Diversity)
# ============================================================================


class TestMTLD:
    def test_diverse_text(self):
        """Text with varied vocabulary should have high MTLD."""
        text = (
            "The kaleidoscopic array of perspectives illuminated previously obscured "
            "dimensions of the phenomenon. Researchers grappled with contradictory evidence "
            "while navigating methodological constraints that shaped their interpretive "
            "frameworks. Paradoxically, the most robust findings emerged from seemingly "
            "tangential investigations into peripheral variables that nobody had anticipated "
            "would prove consequential."
        )
        result = compute_mtld(text)
        assert result["mtld"] > 50  # Rich vocab
        assert result["token_count"] > 20

    def test_repetitive_text(self):
        """Text with repetitive vocabulary should have low MTLD."""
        text = (
            "The study found the results. The results showed the findings. "
            "The findings indicated the results. The study confirmed the findings. "
            "The results of the study showed the findings of the research. "
            "The research findings showed the study results."
        )
        result = compute_mtld(text)
        assert result["mtld"] < result["token_count"]  # Low diversity

    def test_penalty_calculation(self):
        """MTLD below 80 should incur penalty."""
        text = "The study found results. The results showed findings. The findings indicated results."
        result = compute_mtld(text)
        if result["mtld"] < 80:
            assert result["penalty"] > 0
        else:
            assert result["penalty"] == 0

    def test_empty_text(self):
        result = compute_mtld("")
        assert result["mtld"] == 0

    def test_short_text(self):
        result = compute_mtld("Hello world.")
        assert result["mtld"] == 0  # Too few tokens


# ============================================================================
# 3. Fano Factor
# ============================================================================


class TestFanoFactor:
    def test_super_poissonian(self):
        """Varied lengths should produce Fano > 1."""
        lengths = [3, 5, 35, 8, 42, 4, 28]  # high variance
        result = compute_fano_factor(lengths)
        assert result > 1.0

    def test_sub_poissonian(self):
        """Uniform lengths should produce Fano < 2."""
        lengths = [15, 16, 15, 16, 15, 16]  # very uniform
        result = compute_fano_factor(lengths)
        assert result < 2.0  # Low variance relative to mean

    def test_empty_list(self):
        assert compute_fano_factor([]) == 0.0


# ============================================================================
# 4. Sentence Length Range
# ============================================================================


class TestSentenceLengthRange:
    def test_wide_range(self):
        lengths = [4, 12, 25, 38, 45]
        result = compute_sentence_length_range(lengths)
        assert result["range"] == 41
        assert result["penalty"] == 0
        assert result["label"] == "Very wide"

    def test_narrow_range(self):
        lengths = [18, 20, 22, 21, 19]
        result = compute_sentence_length_range(lengths)
        assert result["range"] == 4
        assert result["penalty"] > 0
        assert result["label"] == "Minimal"

    def test_empty_list(self):
        result = compute_sentence_length_range([])
        assert result["range"] == 0
        assert result["penalty"] == 100


# ============================================================================
# 5. Paragraph Opener Diversity
# ============================================================================


class TestParagraphOpenerDiversity:
    def test_diverse_openers(self):
        text = (
            "Education mattered in ways we did not expect. The effect was strong across groups.\n\n"
            "Partisan identity shaped responses differently. Democrats and Republicans diverged on key issues.\n\n"
            "Age told a more complicated story. Older respondents showed distinct patterns of concern.\n\n"
            "Methodological choices influenced our findings substantially. The survey design captured variation well."
        )
        result = compute_paragraph_opener_diversity(text)
        assert result["diversity"] > 0.5

    def test_repetitive_openers(self):
        text = (
            "The results showed significant effects. The results confirmed our hypothesis.\n\n"
            "The results showed strong patterns. The results revealed important trends.\n\n"
            "The results showed clear outcomes. The results established key relationships.\n\n"
            "The results showed meaningful differences. The results supported predictions."
        )
        result = compute_paragraph_opener_diversity(text)
        assert result["diversity"] <= 0.25  # All "the results showed" openers -> 1 unique / 4 total

    def test_single_paragraph(self):
        text = "This is a single paragraph with multiple sentences. It has no breaks."
        result = compute_paragraph_opener_diversity(text)
        assert result["diversity"] == 1.0
        assert result["penalty"] == 0


# ============================================================================
# 6. Composite Score
# ============================================================================


class TestCompositeScore:
    def test_worked_example(self):
        """Verify the worked example from the quantitative-metrics.md reference doc.

        pattern_score=62, burstiness_penalty=31.1, vocab_diversity_penalty=27.5,
        structural_penalty=55.0
        Expected: ~51.67 -> 52%
        """
        result = compute_composite_score(
            pattern_score=62,
            metrics={
                "burstiness_penalty": 31.1,
                "vocab_diversity_penalty": 27.5,
                "structural_penalty": 55.0,
            },
        )
        assert 50 <= result["composite_score"] <= 53
        assert result["risk_level"] == "Elevated"

    def test_zero_scores(self):
        result = compute_composite_score(
            0,
            {"burstiness_penalty": 0, "vocab_diversity_penalty": 0, "structural_penalty": 0},
        )
        assert result["composite_score"] == 0
        assert result["risk_level"] == "Low"

    def test_max_scores(self):
        result = compute_composite_score(
            100,
            {"burstiness_penalty": 100, "vocab_diversity_penalty": 100, "structural_penalty": 100},
        )
        assert result["composite_score"] == 100
        assert result["risk_level"] == "High"


# ============================================================================
# 7. Hedge Density
# ============================================================================


class TestHedgeDensity:
    def test_hedgy_text(self):
        text = (
            "This may suggest that the results could possibly indicate a trend. "
            "It appears that participants might have been influenced. "
            "Perhaps the findings suggest a pattern."
        )
        result = compute_hedge_density(text)
        assert result["density"] > 1.0
        assert result["hedge_count"] > 3

    def test_confident_text(self):
        text = (
            "Education predicted AI concern. Partisan identity determined response patterns. "
            "Age moderated the awareness effect."
        )
        result = compute_hedge_density(text)
        assert result["density"] < 1.0


# ============================================================================
# 8. Discipline Profiles
# ============================================================================


class TestDisciplineProfiles:
    def test_default_profile(self):
        profile = get_discipline_profile("default")
        assert profile["burstiness_threshold"] == 0.45
        assert profile["mtld_threshold"] == 80

    def test_psychology_profile(self):
        profile = get_discipline_profile("psychology")
        assert profile["burstiness_threshold"] == 0.40

    def test_unknown_returns_default(self):
        profile = get_discipline_profile("unknown_field")
        assert profile["burstiness_threshold"] == 0.45


# ============================================================================
# 9. Aggregate — compute_all_metrics
# ============================================================================


class TestAllMetrics:
    def test_returns_all_keys(self):
        text = (
            "Education mattered. But not in the straightforward way we expected. "
            "People with college degrees were more likely to know what large language "
            "models actually do, and that awareness amplified their concern about job "
            "displacement in ways that varied dramatically across partisan lines."
        )
        result = compute_all_metrics(text, pattern_score=50, structural_penalty=30)
        assert "burstiness" in result
        assert "mtld" in result
        assert "fano_factor" in result
        assert "sentence_length_range" in result
        assert "paragraph_opener_diversity" in result
        assert "hedge_density" in result
        assert "composite" in result
