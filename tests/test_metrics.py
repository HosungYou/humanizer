"""
Unit tests for humanizer_mcp.metrics — stylometric metric functions.

Run with:
    pytest tests/test_metrics.py -v
"""

from humanizer_mcp.metrics import (
    _compute_discourse_penalty,
    _compute_psycholinguistic_penalty,
    compute_abstract_noun_ratio,
    compute_burstiness,
    compute_composite_score,
    compute_connective_diversity,
    compute_contraction_density,
    compute_fano_factor,
    compute_hapax_rate,
    compute_hedge_density,
    compute_all_metrics,
    compute_mtld,
    compute_paragraph_length_variance,
    compute_paragraph_opener_diversity,
    compute_pronoun_density,
    compute_question_ratio,
    compute_sentence_length_range,
    compute_surprisal_autocorrelation,
    compute_surprisal_proxy,
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
    def test_worked_example_v2(self):
        """Verify the worked example from the quantitative-metrics.md reference doc (v2).

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
            scoring_version="v2",
        )
        assert 50 <= result["composite_score"] <= 53
        assert result["risk_level"] == "Elevated"
        assert result["scoring_version"] == "v2"

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
            {"burstiness_penalty": 100, "vocab_diversity_penalty": 100, "structural_penalty": 100,
             "discourse_penalty": 100, "psycholinguistic_penalty": 100},
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
        # Original v1/v2 keys
        assert "burstiness" in result
        assert "mtld" in result
        assert "fano_factor" in result
        assert "sentence_length_range" in result
        assert "paragraph_opener_diversity" in result
        assert "hedge_density" in result
        assert "composite" in result
        # v3 keys
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

    def test_v3_composite_has_six_components(self):
        """v3 composite should have 6 components by default."""
        text = (
            "Education mattered. But not in the straightforward way we expected. "
            "People with college degrees were more likely to know what large language "
            "models actually do, and that awareness amplified their concern about job "
            "displacement in ways that varied dramatically across partisan lines."
        )
        result = compute_all_metrics(text, pattern_score=50, structural_penalty=30)
        components = result["composite"]["components"]
        assert "pattern_score" in components
        assert "burstiness_penalty" in components
        assert "vocab_diversity_penalty" in components
        assert "structural_penalty" in components
        assert "discourse_penalty" in components
        assert "psycholinguistic_penalty" in components
        assert len(components) == 6
        assert result["composite"]["scoring_version"] == "v3"

    def test_v2_scoring_version(self):
        """Passing scoring_version='v2' should use 4-component formula."""
        text = (
            "Education mattered. But not in the straightforward way we expected. "
            "People with college degrees were more likely to know what large language "
            "models actually do, and that awareness amplified their concern about job "
            "displacement in ways that varied dramatically across partisan lines."
        )
        result = compute_all_metrics(
            text, pattern_score=50, structural_penalty=30, scoring_version="v2",
        )
        components = result["composite"]["components"]
        assert len(components) == 4
        assert "discourse_penalty" not in components
        assert "psycholinguistic_penalty" not in components
        assert result["composite"]["scoring_version"] == "v2"


# ============================================================================
# 10. Hapax Rate
# ============================================================================


class TestHapaxRate:
    def test_diverse_text_high_hapax(self):
        """Text with many unique words should have a high hapax rate."""
        text = (
            "The kaleidoscopic array of perspectives illuminated previously obscured "
            "dimensions of the phenomenon. Researchers grappled with contradictory evidence "
            "while navigating methodological constraints that shaped their interpretive "
            "frameworks. Paradoxically, the most robust findings emerged from seemingly "
            "tangential investigations into peripheral variables that nobody had anticipated "
            "would prove consequential."
        )
        result = compute_hapax_rate(text)
        assert result["rate"] > 0.40
        assert result["hapax_count"] > 0
        assert result["total_words"] > 20
        assert "hapax" in result["label"].lower() or "human" in result["label"].lower()

    def test_repetitive_text_low_hapax(self):
        """Text with repeated words should have a low hapax rate."""
        text = (
            "The study found the results. The results showed the findings. "
            "The findings indicated the results. The study confirmed the findings. "
            "The results of the study showed the findings of the research. "
            "The research findings showed the study results were the same results."
        )
        result = compute_hapax_rate(text)
        assert result["rate"] < 0.40
        assert result["hapax_count"] < result["total_words"]

    def test_empty_text(self):
        result = compute_hapax_rate("")
        assert result["rate"] == 0.0
        assert result["hapax_count"] == 0
        assert result["total_words"] == 0
        assert result["label"] == "Insufficient text"


# ============================================================================
# 11. Contraction Density
# ============================================================================


class TestContractionDensity:
    def test_informal_text_with_contractions(self):
        """Text with contractions should have positive density."""
        text = (
            "We don't really know what's going on here. "
            "It can't be that simple, and we've seen this before. "
            "They won't admit it, but I'd say we're onto something. "
            "That doesn't mean it's wrong though."
        )
        result = compute_contraction_density(text)
        assert result["density"] > 0.5
        assert result["contraction_count"] >= 6
        assert len(result["contractions_found"]) >= 6

    def test_formal_text_no_contractions(self):
        """Formal text without contractions should have density 0."""
        text = (
            "The study examined the relationship between education and AI concern. "
            "Higher educational attainment predicted greater awareness of AI capabilities. "
            "The relationship between education and concern was moderated by partisan identity."
        )
        result = compute_contraction_density(text)
        assert result["density"] == 0.0
        assert result["contraction_count"] == 0

    def test_empty_text(self):
        result = compute_contraction_density("")
        assert result["density"] == 0.0
        assert result["contraction_count"] == 0


# ============================================================================
# 12. Paragraph Length Variance
# ============================================================================


class TestParagraphLengthVariance:
    def test_varied_paragraph_lengths(self):
        """Paragraphs of different sizes should produce high CV."""
        text = (
            "Short opener.\n\n"
            "This is a somewhat longer paragraph with more words in it to create "
            "variation. It contains several sentences. The point is to be medium-length.\n\n"
            "Tiny.\n\n"
            "And here is the longest paragraph of them all, packed with enough words "
            "to create a substantial difference in length compared to the tiny paragraph "
            "above. We add more and more words to drive up the standard deviation. "
            "This ensures the coefficient of variation reflects genuine disparity in "
            "paragraph construction across the text."
        )
        result = compute_paragraph_length_variance(text)
        assert result["cv"] > 0.40
        assert result["paragraph_count"] == 4
        assert len(result["paragraph_lengths"]) == 4

    def test_uniform_paragraph_lengths(self):
        """Paragraphs of similar size should produce low CV."""
        text = (
            "Education mattered in ways we did not expect at all. "
            "The effect was strong across all groups studied here.\n\n"
            "Partisan identity shaped responses in unexpected directions. "
            "Democrats and Republicans diverged on many key issues.\n\n"
            "Age told a more complicated story than anticipated initially. "
            "Older respondents showed distinct patterns of genuine concern.\n\n"
            "Methodological choices influenced our final findings substantially. "
            "The survey design captured meaningful variation across groups."
        )
        result = compute_paragraph_length_variance(text)
        assert result["cv"] < 0.25
        assert result["paragraph_count"] == 4

    def test_single_paragraph(self):
        """Single paragraph should return CV of 0."""
        text = "This is a single paragraph with no line breaks. It has multiple sentences."
        result = compute_paragraph_length_variance(text)
        assert result["cv"] == 0.0
        assert result["paragraph_count"] == 1
        assert result["label"] == "Insufficient paragraphs"


# ============================================================================
# 13. Surprisal Proxy
# ============================================================================


class TestSurprisalProxy:
    def test_text_returns_valid_structure(self):
        """Surprisal proxy should return variance, mean, std_dev, token_count."""
        text = (
            "The kaleidoscopic array of perspectives illuminated previously obscured "
            "dimensions of the phenomenon. Researchers grappled with contradictory evidence "
            "while navigating methodological constraints that shaped their interpretive "
            "frameworks."
        )
        result = compute_surprisal_proxy(text)
        assert "variance" in result
        assert "mean_surprisal" in result
        assert "std_dev" in result
        assert "token_count" in result
        assert result["variance"] >= 0
        assert result["token_count"] > 10

    def test_common_words_vs_rare_words(self):
        """Text with common words should have different surprisal than rare words."""
        common_text = (
            "The man went to the store and got some food for the family. "
            "He came back home and put the food on the table for the children. "
            "They all sat down and ate the food together at the big table."
        )
        rare_text = (
            "The sesquipedalian obfuscation permeated the labyrinthine bureaucracy. "
            "Epistemological quandaries confounded the perspicacious interlocutors. "
            "Phantasmagorical juxtapositions illuminated the hermeneutical conundrum."
        )
        common_result = compute_surprisal_proxy(common_text)
        rare_result = compute_surprisal_proxy(rare_text)
        # Both should produce valid output
        assert common_result["variance"] >= 0
        assert rare_result["variance"] >= 0

    def test_short_text_insufficient(self):
        """Text with fewer than 10 tokens should return zero variance."""
        result = compute_surprisal_proxy("Short text only.")
        assert result["variance"] == 0.0
        assert result["label"] == "Insufficient text"


# ============================================================================
# 14. Surprisal Autocorrelation
# ============================================================================


class TestSurprisalAutocorrelation:
    def test_sufficient_text_returns_autocorrelation(self):
        """Text with enough tokens should return a numeric autocorrelation."""
        text = (
            "Education mattered in ways we did not expect. But not in the straightforward "
            "way conventional wisdom suggests. People with college degrees were more likely "
            "to know what large language models actually do, and that awareness amplified "
            "their concern about job displacement in ways that varied dramatically."
        )
        result = compute_surprisal_autocorrelation(text)
        assert "autocorrelation" in result
        assert isinstance(result["autocorrelation"], float)
        assert result["label"] != "Insufficient text"

    def test_short_text_insufficient(self):
        """Text with fewer than 15 tokens should return zero."""
        result = compute_surprisal_autocorrelation("Too short for analysis.")
        assert result["autocorrelation"] == 0.0
        assert result["label"] == "Insufficient text"


# ============================================================================
# 15. Connective Diversity
# ============================================================================


class TestConnectiveDiversity:
    def test_diverse_connectives(self):
        """Text with varied connectives should have high diversity."""
        text = (
            "However, the findings challenged expectations. Nevertheless, the data was robust. "
            "Meanwhile, other researchers pursued different approaches. Yet the core question "
            "remained unanswered. Consequently, new methods were developed. Furthermore, "
            "additional funding was secured. In contrast, some labs closed entirely."
        )
        result = compute_connective_diversity(text)
        assert result["diversity"] >= 0.70
        assert result["unique_count"] >= 5
        assert result["total_count"] >= 5

    def test_repetitive_connectives(self):
        """Text repeating the same connective should have low diversity."""
        text = (
            "Furthermore, the study examined education. Furthermore, the analysis included age. "
            "Furthermore, partisan effects were measured. Furthermore, gender was controlled. "
            "Furthermore, income was tested. Furthermore, race was included."
        )
        result = compute_connective_diversity(text)
        # 1 unique / 6 total = ~0.17
        assert result["diversity"] < 0.30
        assert result["unique_count"] == 1

    def test_no_connectives(self):
        """Text without connectives should return diversity 0."""
        text = (
            "Dogs ran across the field. Cats sat on the fence. "
            "Birds flew over the trees. Fish swam in the pond."
        )
        result = compute_connective_diversity(text)
        assert result["diversity"] == 0.0
        assert result["total_count"] == 0
        assert result["label"] == "No connectives found"


# ============================================================================
# 16. Pronoun Density
# ============================================================================


class TestPronounDensity:
    def test_first_person_text(self):
        """Text with first-person pronouns should have positive density."""
        text = (
            "I believe we need to rethink our approach to this problem. "
            "My colleagues and I have been working on a new framework. "
            "We presented our findings at the conference, and they resonated with us."
        )
        result = compute_pronoun_density(text)
        assert result["density"] > 0.5
        assert result["pronoun_count"] >= 5
        assert len(result["pronouns_found"]) >= 5

    def test_impersonal_text(self):
        """Impersonal text should have density near 0."""
        text = (
            "The study examined the relationship between variables. "
            "Results indicated significant correlations between factors. "
            "The analysis revealed patterns across multiple dimensions."
        )
        result = compute_pronoun_density(text)
        assert result["density"] == 0.0
        assert result["pronoun_count"] == 0


# ============================================================================
# 17. Question Ratio
# ============================================================================


class TestQuestionRatio:
    def test_text_with_questions(self):
        """Text containing questions should have positive ratio."""
        text = (
            "Why do Democrats and Republicans worry about AI at nearly identical rates? "
            "That puzzle drove much of our analysis. "
            "What explains the partisan divergence in the type of concern expressed? "
            "The answer lies in cultural versus economic framing."
        )
        result = compute_question_ratio(text)
        assert result["ratio"] > 0.0
        assert result["question_count"] >= 2

    def test_text_without_questions(self):
        """Text without questions should have ratio 0."""
        text = (
            "Education predicted AI concern. Partisan identity moderated the effect. "
            "Age interacted with technology awareness. The findings were robust."
        )
        result = compute_question_ratio(text)
        assert result["ratio"] == 0.0
        assert result["question_count"] == 0


# ============================================================================
# 18. Abstract Noun Ratio
# ============================================================================


class TestAbstractNounRatio:
    def test_abstract_heavy_text(self):
        """Text with many abstract nouns should have higher ratio."""
        text = (
            "The implementation of the recommendation required consideration of the "
            "organization's commitment to excellence. The administration's recognition "
            "of the situation led to acknowledgement that determination and persistence "
            "would be essential for the advancement of the institution."
        )
        result = compute_abstract_noun_ratio(text)
        assert result["ratio"] > 0.10
        assert result["abstract_count"] > 3
        assert len(result["abstracts_found"]) > 3

    def test_concrete_text(self):
        """Text with mostly concrete words should have lower ratio."""
        text = (
            "The dog ran across the green field. Birds sang in the tall oak trees. "
            "A child threw a red ball over the white fence. The cat slept on the warm rug."
        )
        result = compute_abstract_noun_ratio(text)
        assert result["ratio"] < 0.10

    def test_empty_text(self):
        result = compute_abstract_noun_ratio("")
        assert result["ratio"] == 0.0
        assert result["abstract_count"] == 0
        assert result["total_words"] == 0
        assert result["label"] == "Insufficient text"


# ============================================================================
# 19. Composite Score v3 (dedicated tests)
# ============================================================================


class TestCompositeScoreV3:
    def test_v3_uses_six_components(self):
        """v3 formula should use 6 weighted components."""
        result = compute_composite_score(
            pattern_score=50,
            metrics={
                "burstiness_penalty": 30,
                "vocab_diversity_penalty": 20,
                "structural_penalty": 40,
                "discourse_penalty": 60,
                "psycholinguistic_penalty": 50,
            },
        )
        assert result["scoring_version"] == "v3"
        assert len(result["components"]) == 6
        # Verify: 0.40*50 + 0.15*30 + 0.10*20 + 0.10*40 + 0.15*60 + 0.10*50
        # = 20 + 4.5 + 2 + 4 + 9 + 5 = 44.5
        assert 44 <= result["composite_score"] <= 45

    def test_v2_backward_compatibility(self):
        """v2 should use 4-component formula, ignoring discourse/psycholinguistic."""
        result = compute_composite_score(
            pattern_score=50,
            metrics={
                "burstiness_penalty": 30,
                "vocab_diversity_penalty": 20,
                "structural_penalty": 40,
                "discourse_penalty": 60,
                "psycholinguistic_penalty": 50,
            },
            scoring_version="v2",
        )
        assert result["scoring_version"] == "v2"
        assert len(result["components"]) == 4
        assert "discourse_penalty" not in result["components"]
        assert "psycholinguistic_penalty" not in result["components"]
        # Verify: 0.60*50 + 0.20*30 + 0.10*20 + 0.10*40
        # = 30 + 6 + 2 + 4 = 42
        assert 41 <= result["composite_score"] <= 43

    def test_result_between_0_and_100(self):
        """Composite score should always be between 0 and 100."""
        for pattern in [0, 25, 50, 75, 100]:
            result = compute_composite_score(
                pattern_score=pattern,
                metrics={
                    "burstiness_penalty": pattern,
                    "vocab_diversity_penalty": pattern,
                    "structural_penalty": pattern,
                    "discourse_penalty": pattern,
                    "psycholinguistic_penalty": pattern,
                },
            )
            assert 0 <= result["composite_score"] <= 100


# ============================================================================
# 20. Discourse Penalty
# ============================================================================


class TestDiscoursePenalty:
    def test_poor_discourse_high_penalty(self):
        """Low connective diversity, no questions, no pronouns -> high penalty."""
        penalty = _compute_discourse_penalty(
            connective_div={"diversity": 0.0},
            question_ratio={"ratio": 0.0},
            pronoun_density={"density": 0.0},
        )
        assert penalty == 100.0

    def test_good_discourse_low_penalty(self):
        """High connective diversity, questions present, pronouns present -> low penalty."""
        penalty = _compute_discourse_penalty(
            connective_div={"diversity": 0.80},
            question_ratio={"ratio": 0.05},
            pronoun_density={"density": 0.10},
        )
        assert penalty == 0.0

    def test_mixed_discourse_partial_penalty(self):
        """Some good, some poor discourse metrics -> partial penalty."""
        penalty = _compute_discourse_penalty(
            connective_div={"diversity": 0.70},  # passes threshold
            question_ratio={"ratio": 0.0},        # fails -> 100%
            pronoun_density={"density": 0.05},     # passes threshold
        )
        # cd_pen = 0, qr_pen = 100, pd_pen = 0 -> avg = 33.33
        assert 33 <= penalty <= 34


# ============================================================================
# 21. Psycholinguistic Penalty
# ============================================================================


class TestPsycholinguisticPenalty:
    def test_ai_typical_high_penalty(self):
        """Low hapax, no contractions, high abstraction, low surprisal -> high penalty."""
        penalty = _compute_psycholinguistic_penalty(
            hapax={"rate": 0.0},
            contraction={"density": 0.0},
            abstract_noun={"ratio": 0.60},
            surprisal={"variance": 0.0},
        )
        assert penalty == 100.0

    def test_human_like_low_penalty(self):
        """High hapax, contractions present, low abstraction, high surprisal -> low penalty."""
        penalty = _compute_psycholinguistic_penalty(
            hapax={"rate": 0.50},
            contraction={"density": 0.15},
            abstract_noun={"ratio": 0.20},
            surprisal={"variance": 20.0},
        )
        assert penalty == 0.0

    def test_mixed_partial_penalty(self):
        """Some good, some poor psycholinguistic metrics -> partial penalty."""
        penalty = _compute_psycholinguistic_penalty(
            hapax={"rate": 0.45},        # passes (>= 0.45)
            contraction={"density": 0.0},  # fails -> 100%
            abstract_noun={"ratio": 0.30}, # passes (<= 0.30)
            surprisal={"variance": 15.0},  # passes (>= 15.0)
        )
        # hr_pen=0, cd_pen=100, ar_pen=0, sv_pen=0 -> avg = 25
        assert penalty == 25.0


# ============================================================================
# 22. Discipline Profiles (expanded from 4 to 7)
# ============================================================================


class TestExpandedDisciplineProfiles:
    def test_stem_profile(self):
        profile = get_discipline_profile("stem")
        assert profile["burstiness_threshold"] == 0.38
        assert profile["mtld_threshold"] == 82
        assert profile["contraction_target"] == 0.02

    def test_humanities_profile(self):
        profile = get_discipline_profile("humanities")
        assert profile["burstiness_threshold"] == 0.48
        assert profile["mtld_threshold"] == 85
        assert profile["hapax_target"] == 0.50

    def test_social_sciences_profile(self):
        profile = get_discipline_profile("social_sciences")
        assert profile["burstiness_threshold"] == 0.44
        assert profile["pronoun_target"] == 0.06

    def test_education_profile(self):
        profile = get_discipline_profile("education")
        assert profile["burstiness_threshold"] == 0.43
        assert profile["contraction_target"] == 0.15

    def test_management_profile(self):
        profile = get_discipline_profile("management")
        assert profile["burstiness_threshold"] == 0.42
        assert profile["pronoun_target"] == 0.06

    def test_all_profiles_have_v3_keys(self):
        """Every profile should include contraction_target, pronoun_target, hapax_target."""
        from humanizer_mcp.metrics import DISCIPLINE_PROFILES
        for name, profile in DISCIPLINE_PROFILES.items():
            assert "contraction_target" in profile, f"{name} missing contraction_target"
            assert "pronoun_target" in profile, f"{name} missing pronoun_target"
            assert "hapax_target" in profile, f"{name} missing hapax_target"
