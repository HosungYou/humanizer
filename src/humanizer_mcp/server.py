"""FastMCP server exposing stylometric humanization tools."""

from mcp.server.fastmcp import FastMCP

from humanizer_mcp.metrics import (
    DISCIPLINE_PROFILES,
    compute_all_metrics,
    compute_burstiness,
    compute_composite_score,
    compute_fano_factor,
    compute_hedge_density,
    compute_mtld,
    compute_paragraph_opener_diversity,
    compute_sentence_length_range,
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
    paragraph opener diversity, hedge density, and composite AI probability score.
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

        # Recompute composite with updated penalties
        result["composite"] = compute_composite_score(
            pattern_score,
            {
                "burstiness_penalty": bust["penalty"],
                "vocab_diversity_penalty": mtld_data["penalty"],
                "structural_penalty": structural_penalty,
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
# Entry point
# ---------------------------------------------------------------------------

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
