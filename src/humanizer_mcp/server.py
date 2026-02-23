"""FastMCP server exposing stylometric humanization tools."""

import json

from mcp.server.fastmcp import FastMCP

from humanizer_mcp.metrics import (
    DISCIPLINE_PROFILES,
    _compute_discourse_penalty,
    _compute_psycholinguistic_penalty,
    compute_abstract_noun_ratio,
    compute_all_metrics,
    compute_burstiness,
    compute_composite_score,
    compute_connective_diversity,
    compute_contraction_density,
    compute_fano_factor,
    compute_hapax_rate,
    compute_hedge_density,
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

mcp = FastMCP("humanizer")


# ---------------------------------------------------------------------------
# Tool 1: full metrics
# ---------------------------------------------------------------------------

@mcp.tool()
def humanizer_metrics(
    text: str,
    pattern_score: float = 0,
    structural_penalty: float = 0,
    non_native: bool = False,
    discipline: str = "default",
) -> dict:
    """Compute all quantitative stylometric metrics for input text.

    Returns burstiness CV, MTLD, Fano Factor, sentence length range,
    paragraph opener diversity, hedge density, discourse and psycholinguistic
    penalties, and composite AI probability score (v3 formula).
    """
    profile = get_discipline_profile(discipline)
    result = compute_all_metrics(
        text,
        pattern_score=pattern_score,
        structural_penalty=structural_penalty,
        non_native=non_native,
    )

    # Recalculate penalties with discipline-specific thresholds if not default
    if discipline != "default":
        bust = result["burstiness"]
        cv = bust["cv"]
        b_thresh = profile["burstiness_threshold"]
        bust["penalty"] = round(
            0.0 if cv >= b_thresh else (b_thresh - cv) / b_thresh * 100, 2
        )

        mtld_data = result["mtld"]
        mtld_val = mtld_data["mtld"]
        m_thresh = profile["mtld_threshold"]
        mtld_data["penalty"] = round(
            0.0 if mtld_val >= m_thresh else (m_thresh - mtld_val) / m_thresh * 100, 2
        )

        # Recompute composite with updated penalties (v3 includes discourse + psycholinguistic)
        result["composite"] = compute_composite_score(
            pattern_score,
            {
                "burstiness_penalty": bust["penalty"],
                "vocab_diversity_penalty": mtld_data["penalty"],
                "structural_penalty": structural_penalty,
                "discourse_penalty": result["discourse_penalty"],
                "psycholinguistic_penalty": result["psycholinguistic_penalty"],
            },
        )

    result["discipline"] = discipline
    result["discipline_profile"] = profile
    return result


# ---------------------------------------------------------------------------
# Tool 2: before / after verification
# ---------------------------------------------------------------------------

@mcp.tool()
def humanizer_verify(
    original_text: str,
    humanized_text: str,
    pattern_score_before: float = 0,
    pattern_score_after: float = 0,
) -> dict:
    """Compare before/after metrics, flag regressions, determine if another pass is needed.

    Returns metrics comparison, regression flags, and needs_another_pass recommendation.
    """
    before = compute_all_metrics(original_text, pattern_score=pattern_score_before)
    after = compute_all_metrics(humanized_text, pattern_score=pattern_score_after)

    regressions: list[dict] = []

    # Check burstiness CV (higher is better)
    if after["burstiness"]["cv"] < before["burstiness"]["cv"]:
        diff = before["burstiness"]["cv"] - after["burstiness"]["cv"]
        regressions.append({
            "metric": "burstiness_cv",
            "before": before["burstiness"]["cv"],
            "after": after["burstiness"]["cv"],
            "severity": "high" if diff > 0.10 else "moderate" if diff > 0.05 else "low",
        })

    # Check MTLD (higher is better)
    if after["mtld"]["mtld"] < before["mtld"]["mtld"]:
        diff = before["mtld"]["mtld"] - after["mtld"]["mtld"]
        regressions.append({
            "metric": "mtld",
            "before": before["mtld"]["mtld"],
            "after": after["mtld"]["mtld"],
            "severity": "high" if diff > 15 else "moderate" if diff > 5 else "low",
        })

    # Check paragraph opener diversity (higher is better)
    opener_decreased = (
        after["paragraph_opener_diversity"]["diversity"]
        < before["paragraph_opener_diversity"]["diversity"]
    )
    if opener_decreased:
        diff = (
            before["paragraph_opener_diversity"]["diversity"]
            - after["paragraph_opener_diversity"]["diversity"]
        )
        regressions.append({
            "metric": "paragraph_opener_diversity",
            "before": before["paragraph_opener_diversity"]["diversity"],
            "after": after["paragraph_opener_diversity"]["diversity"],
            "severity": "high" if diff > 0.20 else "moderate" if diff > 0.10 else "low",
        })

    # Check discourse penalty (lower is better)
    if after["discourse_penalty"] > before["discourse_penalty"]:
        diff = after["discourse_penalty"] - before["discourse_penalty"]
        regressions.append({
            "metric": "discourse_penalty",
            "before": before["discourse_penalty"],
            "after": after["discourse_penalty"],
            "severity": "high" if diff > 15 else "moderate" if diff > 5 else "low",
        })

    # Check psycholinguistic penalty (lower is better)
    if after["psycholinguistic_penalty"] > before["psycholinguistic_penalty"]:
        diff = after["psycholinguistic_penalty"] - before["psycholinguistic_penalty"]
        regressions.append({
            "metric": "psycholinguistic_penalty",
            "before": before["psycholinguistic_penalty"],
            "after": after["psycholinguistic_penalty"],
            "severity": "high" if diff > 15 else "moderate" if diff > 5 else "low",
        })

    # Check connective diversity (higher is better)
    if (
        after["connective_diversity"]["diversity"]
        < before["connective_diversity"]["diversity"]
    ):
        diff = (
            before["connective_diversity"]["diversity"]
            - after["connective_diversity"]["diversity"]
        )
        regressions.append({
            "metric": "connective_diversity",
            "before": before["connective_diversity"]["diversity"],
            "after": after["connective_diversity"]["diversity"],
            "severity": "high" if diff > 0.20 else "moderate" if diff > 0.10 else "low",
        })

    # Check hapax rate (higher is better)
    if after["hapax_rate"]["rate"] < before["hapax_rate"]["rate"]:
        diff = before["hapax_rate"]["rate"] - after["hapax_rate"]["rate"]
        regressions.append({
            "metric": "hapax_rate",
            "before": before["hapax_rate"]["rate"],
            "after": after["hapax_rate"]["rate"],
            "severity": "high" if diff > 0.10 else "moderate" if diff > 0.05 else "low",
        })

    composite_after = after["composite"]["composite_score"]
    needs_another_pass = (
        composite_after > 30
        or len(regressions) > 0
        or opener_decreased
    )

    recommendations: list[str] = []
    if composite_after > 30:
        recommendations.append(
            f"Composite score is {composite_after:.1f}% (target: <=30%). "
            "Continue humanization to reduce AI probability."
        )
    for reg in regressions:
        recommendations.append(
            f"{reg['metric']} regressed from {reg['before']} to {reg['after']} "
            f"(severity: {reg['severity']}). Address in next pass."
        )
    if not needs_another_pass:
        recommendations.append("All metrics improved or held. Text is ready.")

    return {
        "before": before,
        "after": after,
        "regressions": regressions,
        "needs_another_pass": needs_another_pass,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# Tool 3: per-metric delta report
# ---------------------------------------------------------------------------

@mcp.tool()
def humanizer_diff(
    original_text: str,
    humanized_text: str,
) -> dict:
    """Generate per-metric delta report between original and humanized text.

    Returns deltas, improvement percentages, and sentence length distribution comparison.
    """
    before = compute_all_metrics(original_text)
    after = compute_all_metrics(humanized_text)

    def _delta(after_val: float, before_val: float) -> dict:
        d = round(after_val - before_val, 4)
        pct = round(d / before_val * 100, 2) if before_val != 0 else 0.0
        return {"delta": d, "improvement_pct": pct}

    deltas = {
        "burstiness_cv": {
            "before": before["burstiness"]["cv"],
            "after": after["burstiness"]["cv"],
            **_delta(after["burstiness"]["cv"], before["burstiness"]["cv"]),
        },
        "burstiness_penalty": {
            "before": before["burstiness"]["penalty"],
            "after": after["burstiness"]["penalty"],
            **_delta(after["burstiness"]["penalty"], before["burstiness"]["penalty"]),
        },
        "mtld": {
            "before": before["mtld"]["mtld"],
            "after": after["mtld"]["mtld"],
            **_delta(after["mtld"]["mtld"], before["mtld"]["mtld"]),
        },
        "mtld_penalty": {
            "before": before["mtld"]["penalty"],
            "after": after["mtld"]["penalty"],
            **_delta(after["mtld"]["penalty"], before["mtld"]["penalty"]),
        },
        "fano_factor": {
            "before": before["fano_factor"],
            "after": after["fano_factor"],
            **_delta(after["fano_factor"], before["fano_factor"]),
        },
        "sentence_length_range": {
            "before": before["sentence_length_range"]["range"],
            "after": after["sentence_length_range"]["range"],
            **_delta(
                after["sentence_length_range"]["range"],
                before["sentence_length_range"]["range"],
            ),
        },
        "paragraph_opener_diversity": {
            "before": before["paragraph_opener_diversity"]["diversity"],
            "after": after["paragraph_opener_diversity"]["diversity"],
            **_delta(
                after["paragraph_opener_diversity"]["diversity"],
                before["paragraph_opener_diversity"]["diversity"],
            ),
        },
        "hedge_density": {
            "before": before["hedge_density"]["density"],
            "after": after["hedge_density"]["density"],
            **_delta(after["hedge_density"]["density"], before["hedge_density"]["density"]),
        },
        "discourse_penalty": {
            "before": before["discourse_penalty"],
            "after": after["discourse_penalty"],
            **_delta(after["discourse_penalty"], before["discourse_penalty"]),
        },
        "psycholinguistic_penalty": {
            "before": before["psycholinguistic_penalty"],
            "after": after["psycholinguistic_penalty"],
            **_delta(
                after["psycholinguistic_penalty"],
                before["psycholinguistic_penalty"],
            ),
        },
        "connective_diversity": {
            "before": before["connective_diversity"]["diversity"],
            "after": after["connective_diversity"]["diversity"],
            **_delta(
                after["connective_diversity"]["diversity"],
                before["connective_diversity"]["diversity"],
            ),
        },
        "hapax_rate": {
            "before": before["hapax_rate"]["rate"],
            "after": after["hapax_rate"]["rate"],
            **_delta(after["hapax_rate"]["rate"], before["hapax_rate"]["rate"]),
        },
        "question_ratio": {
            "before": before["question_ratio"]["ratio"],
            "after": after["question_ratio"]["ratio"],
            **_delta(
                after["question_ratio"]["ratio"],
                before["question_ratio"]["ratio"],
            ),
        },
        "composite_score": {
            "before": before["composite"]["composite_score"],
            "after": after["composite"]["composite_score"],
            **_delta(
                after["composite"]["composite_score"],
                before["composite"]["composite_score"],
            ),
        },
    }

    return {
        "deltas": deltas,
        "sentence_length_distribution": {
            "before": before["burstiness"]["sentence_lengths"],
            "after": after["burstiness"]["sentence_lengths"],
        },
    }


# ---------------------------------------------------------------------------
# Tool 4: status / readiness check
# ---------------------------------------------------------------------------

@mcp.tool()
def humanizer_status(
    text: str,
    discipline: str = "default",
    target: float = 30,
) -> dict:
    """Return current metrics vs target thresholds with discipline-specific calibration.

    Shows distance-to-target for each metric and overall readiness assessment.
    """
    profile = get_discipline_profile(discipline)
    result = compute_all_metrics(text)

    b_thresh = profile["burstiness_threshold"]
    m_thresh = profile["mtld_threshold"]

    cv = result["burstiness"]["cv"]
    mtld_val = result["mtld"]["mtld"]
    slr = result["sentence_length_range"]["range"]
    opener_div = result["paragraph_opener_diversity"]["diversity"]
    composite = result["composite"]["composite_score"]
    conn_div = result["connective_diversity"]["diversity"]
    hapax = result["hapax_rate"]["rate"]
    question = result["question_ratio"]["ratio"]
    disc_pen = result["discourse_penalty"]
    psych_pen = result["psycholinguistic_penalty"]

    status_details = {
        "burstiness_cv": {
            "current": cv,
            "target": b_thresh,
            "distance": round(b_thresh - cv, 4) if cv < b_thresh else 0.0,
            "passed": cv >= b_thresh,
        },
        "mtld": {
            "current": mtld_val,
            "target": m_thresh,
            "distance": round(m_thresh - mtld_val, 2) if mtld_val < m_thresh else 0.0,
            "passed": mtld_val >= m_thresh,
        },
        "sentence_length_range": {
            "current": slr,
            "target": 25,
            "distance": 25 - slr if slr < 25 else 0,
            "passed": slr >= 25,
        },
        "paragraph_opener_diversity": {
            "current": opener_div,
            "target": 0.70,
            "distance": round(0.70 - opener_div, 4) if opener_div < 0.70 else 0.0,
            "passed": opener_div >= 0.70,
        },
        "connective_diversity": {
            "current": conn_div,
            "target": 0.70,
            "distance": round(0.70 - conn_div, 4) if conn_div < 0.70 else 0.0,
            "passed": conn_div >= 0.70,
        },
        "hapax_rate": {
            "current": hapax,
            "target": 0.45,
            "distance": round(0.45 - hapax, 4) if hapax < 0.45 else 0.0,
            "passed": hapax >= 0.45,
        },
        "question_ratio": {
            "current": question,
            "target": 0.02,
            "distance": round(0.02 - question, 4) if question < 0.02 else 0.0,
            "passed": question >= 0.02,
        },
        "discourse_penalty": {
            "current": disc_pen,
            "target": 20.0,
            "distance": round(disc_pen - 20.0, 2) if disc_pen > 20.0 else 0.0,
            "passed": disc_pen <= 20.0,
        },
        "psycholinguistic_penalty": {
            "current": psych_pen,
            "target": 20.0,
            "distance": round(psych_pen - 20.0, 2) if psych_pen > 20.0 else 0.0,
            "passed": psych_pen <= 20.0,
        },
        "composite_score": {
            "current": composite,
            "target": target,
            "distance": round(composite - target, 2) if composite > target else 0.0,
            "passed": composite <= target,
        },
    }

    all_passed = all(s["passed"] for s in status_details.values())

    return {
        "readiness": "ready" if all_passed else "needs_work",
        "discipline": discipline,
        "discipline_profile": profile,
        "target_composite": target,
        "metrics": status_details,
        "full_metrics": result,
    }


# ---------------------------------------------------------------------------
# Tool 5: discourse-level analysis
# ---------------------------------------------------------------------------

@mcp.tool()
def humanizer_discourse(text: str, discipline: str = "default") -> str:
    """Compute discourse-level metrics for AI detection assessment.

    Analyzes text for discourse patterns that are difficult for AI text
    to replicate, including connective diversity, question usage,
    pronoun density, and psycholinguistic markers.

    Args:
        text: The text to analyze
        discipline: Academic discipline for calibration
                   (default, psychology, management, education, stem, humanities, social_sciences)

    Returns:
        JSON with discourse metrics, penalties, and discipline-calibrated targets
    """
    profile = get_discipline_profile(discipline)

    # Compute all 9 new metrics
    hapax = compute_hapax_rate(text)
    contraction = compute_contraction_density(text)
    para_var = compute_paragraph_length_variance(text)
    surprisal = compute_surprisal_proxy(text)
    surprisal_ac = compute_surprisal_autocorrelation(text)
    connective_div = compute_connective_diversity(text)
    pronoun = compute_pronoun_density(text)
    question = compute_question_ratio(text)
    abstract_noun = compute_abstract_noun_ratio(text)

    # Compute derived penalties
    discourse_penalty = _compute_discourse_penalty(
        connective_div, question, pronoun,
    )
    psycholinguistic_penalty = _compute_psycholinguistic_penalty(
        hapax, contraction, abstract_noun, surprisal,
    )

    # Discipline-calibrated targets
    targets = {
        "contraction_target": profile.get("contraction_target", 0.10),
        "pronoun_target": profile.get("pronoun_target", 0.05),
        "hapax_target": profile.get("hapax_target", 0.45),
        "connective_diversity_target": 0.70,
        "question_ratio_target": 0.02,
        "abstract_noun_ceiling": 0.30,
        "surprisal_variance_target": 15.0,
    }

    # Flag metrics in AI-typical range
    flags: list[str] = []
    if connective_div["diversity"] < 0.50:
        flags.append("connective_diversity: AI-typical (<0.50)")
    if hapax["rate"] < 0.35:
        flags.append("hapax_rate: AI-typical (<0.35)")
    if question["ratio"] < 0.01:
        flags.append("question_ratio: AI-typical (<0.01)")
    if pronoun["density"] < 0.02:
        flags.append("pronoun_density: AI-typical (<0.02)")
    if contraction["density"] < 0.05:
        flags.append("contraction_density: AI-typical (<0.05)")
    if abstract_noun["ratio"] > 0.45:
        flags.append("abstract_noun_ratio: AI-typical (>0.45)")
    if surprisal.get("variance", 0) < 8.0:
        flags.append("surprisal_variance: AI-typical (<8.0)")
    if para_var["cv"] < 0.25:
        flags.append("paragraph_length_variance: AI-typical (<0.25)")
    if abs(surprisal_ac.get("autocorrelation", 0)) < 0.15:
        flags.append("surprisal_autocorrelation: AI-typical (<0.15)")

    return json.dumps({
        "metrics": {
            "hapax_rate": hapax,
            "contraction_density": contraction,
            "paragraph_length_variance": para_var,
            "surprisal_proxy": surprisal,
            "surprisal_autocorrelation": surprisal_ac,
            "connective_diversity": connective_div,
            "pronoun_density": pronoun,
            "question_ratio": question,
            "abstract_noun_ratio": abstract_noun,
        },
        "penalties": {
            "discourse_penalty": discourse_penalty,
            "psycholinguistic_penalty": psycholinguistic_penalty,
        },
        "discipline": discipline,
        "discipline_targets": targets,
        "flags": flags,
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
