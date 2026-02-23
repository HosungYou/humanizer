"""Quantitative stylometric metrics for academic text humanization.

All algorithms are pure Python — no external NLP libraries required.
"""

import math
import re
import string


# ---------------------------------------------------------------------------
# Discipline calibration profiles
# ---------------------------------------------------------------------------

DISCIPLINE_PROFILES: dict[str, dict] = {
    "default": {"burstiness_threshold": 0.45, "mtld_threshold": 80},
    "psychology": {"burstiness_threshold": 0.40, "mtld_threshold": 75},
    "management": {"burstiness_threshold": 0.42, "mtld_threshold": 78},
    "education": {"burstiness_threshold": 0.43, "mtld_threshold": 76},
}


def get_discipline_profile(discipline: str) -> dict:
    """Return the calibration profile for *discipline*, falling back to default."""
    return DISCIPLINE_PROFILES.get(discipline, DISCIPLINE_PROFILES["default"])


# ---------------------------------------------------------------------------
# Sentence tokeniser
# ---------------------------------------------------------------------------

# Abbreviations that should NOT trigger a sentence split.
_ABBREVIATIONS = (
    r"et\s+al", r"Fig", r"Dr", r"Mr", r"Mrs", r"Prof",
    r"Inc", r"Ltd", r"vs", r"i\.e", r"e\.g", r"etc",
)

# Build a negative‐lookbehind‐style protection pattern.  We replace known
# abbreviation dots with a placeholder, split, then restore.
_ABBREV_RE = re.compile(
    r"\b(?:" + "|".join(_ABBREVIATIONS) + r")\.",
    re.IGNORECASE,
)

_PLACEHOLDER = "\x00ABBRDOT\x00"

# Protect decimal numbers like 0.45 or p = .001
_DECIMAL_RE = re.compile(r"(\d)\.(\d)")
_LEADING_DECIMAL_RE = re.compile(r"(?<=\s)\.(\d)")
_DECIMAL_PLACEHOLDER = "\x00DECDOT\x00"
_LEADING_DEC_PLACEHOLDER = "\x00LDDOT\x00"

# Protect periods inside parenthetical citations e.g. (Author, 2024).
_PAREN_PERIOD_RE = re.compile(r"\(([^)]*)\.\)")
_PAREN_PLACEHOLDER = "\x00PARDOT\x00"


def _tokenize_sentences(text: str) -> list[str]:
    """Split *text* into sentences with abbreviation / decimal protection."""
    working = text

    # 1. Protect abbreviation dots
    working = _ABBREV_RE.sub(lambda m: m.group(0)[:-1] + _PLACEHOLDER, working)

    # 2. Protect decimal numbers
    working = _DECIMAL_RE.sub(rf"\1{_DECIMAL_PLACEHOLDER}\2", working)
    working = _LEADING_DECIMAL_RE.sub(rf"{_LEADING_DEC_PLACEHOLDER}\1", working)

    # 3. Protect parenthetical citation dots
    working = _PAREN_PERIOD_RE.sub(
        lambda m: "(" + m.group(1).replace(".", _PAREN_PLACEHOLDER) + _PAREN_PLACEHOLDER + ")",
        working,
    )

    # 4. Split on sentence‐ending punctuation followed by whitespace or EOS
    parts = re.split(r"(?<=[.!?])(?:\s+|$)", working)

    # 5. Restore placeholders and filter
    sentences: list[str] = []
    for part in parts:
        restored = (
            part.replace(_PLACEHOLDER, ".")
            .replace(_DECIMAL_PLACEHOLDER, ".")
            .replace(_LEADING_DEC_PLACEHOLDER, ".")
            .replace(_PAREN_PLACEHOLDER, ".")
            .strip()
        )
        if not restored:
            continue
        word_count = len(restored.split())
        if word_count >= 3:
            sentences.append(restored)

    return sentences


def _word_count(sentence: str) -> int:
    return len(sentence.split())


# ---------------------------------------------------------------------------
# Burstiness (coefficient of variation of sentence lengths)
# ---------------------------------------------------------------------------

def compute_burstiness(text: str, non_native: bool = False) -> dict:
    """Return burstiness metrics based on sentence‐length variation."""
    sentences = _tokenize_sentences(text)
    lengths = [_word_count(s) for s in sentences]

    if len(lengths) < 2:
        return {
            "cv": 0.0,
            "mean_length": float(lengths[0]) if lengths else 0.0,
            "std_dev": 0.0,
            "penalty": 0.0,
            "sentence_count": len(lengths),
            "sentence_lengths": lengths,
            "label": "Minimal burstiness",
        }

    mean_length = sum(lengths) / len(lengths)
    variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    cv = std_dev / mean_length if mean_length > 0 else 0.0

    threshold = 0.35 if non_native else 0.45
    if cv >= threshold:
        penalty = 0.0
    else:
        penalty = (threshold - cv) / threshold * 100

    if cv > 0.55:
        label = "High burstiness"
    elif cv >= 0.45:
        label = "Normal burstiness"
    elif cv >= 0.35:
        label = "Low burstiness"
    elif cv >= 0.25:
        label = "Very low burstiness"
    else:
        label = "Minimal burstiness"

    return {
        "cv": round(cv, 4),
        "mean_length": round(mean_length, 2),
        "std_dev": round(std_dev, 2),
        "penalty": round(penalty, 2),
        "sentence_count": len(lengths),
        "sentence_lengths": lengths,
        "label": label,
    }


# ---------------------------------------------------------------------------
# MTLD (Measure of Textual Lexical Diversity)
# ---------------------------------------------------------------------------

def _mtld_one_direction(tokens: list[str], threshold: float = 0.72) -> float:
    """Run one pass of MTLD and return the factor count (including partial)."""
    factors = 0.0
    type_set: set[str] = set()
    token_count = 0

    for token in tokens:
        type_set.add(token)
        token_count += 1
        ttr = len(type_set) / token_count
        if ttr <= threshold:
            factors += 1
            type_set = set()
            token_count = 0

    # Partial factor for remaining tokens
    if token_count > 0:
        current_ttr = len(type_set) / token_count
        partial = (1.0 - current_ttr) / (1.0 - threshold) if threshold < 1.0 else 0.0
        factors += partial

    return factors


def compute_mtld(text: str) -> dict:
    """Compute Measure of Textual Lexical Diversity (McCarthy & Jarvis 2010)."""
    # Tokenise: lowercase, strip punctuation, keep only alphanumeric tokens
    raw_tokens = text.lower().split()
    tokens = [t.strip(string.punctuation) for t in raw_tokens]
    tokens = [t for t in tokens if t and any(c.isalnum() for c in t)]

    if len(tokens) < 10:
        return {
            "mtld": 0.0,
            "mtld_forward": 0.0,
            "mtld_backward": 0.0,
            "penalty": 0.0,
            "token_count": len(tokens),
            "label": "Minimal diversity",
        }

    factors_fwd = _mtld_one_direction(tokens)
    mtld_forward = len(tokens) / factors_fwd if factors_fwd > 0 else 0.0

    factors_bwd = _mtld_one_direction(list(reversed(tokens)))
    mtld_backward = len(tokens) / factors_bwd if factors_bwd > 0 else 0.0

    mtld = (mtld_forward + mtld_backward) / 2

    if mtld >= 80:
        penalty = 0.0
    else:
        penalty = (80 - mtld) / 80 * 100

    if mtld > 100:
        label = "Very high diversity"
    elif mtld >= 80:
        label = "Normal diversity"
    elif mtld >= 60:
        label = "Low diversity"
    elif mtld >= 40:
        label = "Very low diversity"
    else:
        label = "Minimal diversity"

    return {
        "mtld": round(mtld, 2),
        "mtld_forward": round(mtld_forward, 2),
        "mtld_backward": round(mtld_backward, 2),
        "penalty": round(penalty, 2),
        "token_count": len(tokens),
        "label": label,
    }


# ---------------------------------------------------------------------------
# Fano factor
# ---------------------------------------------------------------------------

def compute_fano_factor(sentence_lengths: list[int]) -> float:
    """Return variance / mean of *sentence_lengths* (population variance)."""
    if not sentence_lengths:
        return 0.0
    mean = sum(sentence_lengths) / len(sentence_lengths)
    if mean == 0:
        return 0.0
    variance = sum((x - mean) ** 2 for x in sentence_lengths) / len(sentence_lengths)
    return round(variance / mean, 4)


# ---------------------------------------------------------------------------
# Sentence length range
# ---------------------------------------------------------------------------

def compute_sentence_length_range(sentence_lengths: list[int]) -> dict:
    """Compute the spread of sentence lengths and an associated penalty."""
    if not sentence_lengths:
        return {
            "range": 0,
            "min_length": 0,
            "max_length": 0,
            "penalty": 100.0,
            "label": "Minimal",
        }

    min_len = min(sentence_lengths)
    max_len = max(sentence_lengths)
    rng = max_len - min_len

    if rng >= 25:
        penalty = 0.0
    else:
        penalty = (25 - rng) / 25 * 100

    if rng > 35:
        label = "Very wide"
    elif rng >= 25:
        label = "Normal"
    elif rng >= 15:
        label = "Narrow"
    elif rng >= 5:
        label = "Very narrow"
    else:
        label = "Minimal"

    return {
        "range": rng,
        "min_length": min_len,
        "max_length": max_len,
        "penalty": round(penalty, 2),
        "label": label,
    }


# ---------------------------------------------------------------------------
# Paragraph opener diversity
# ---------------------------------------------------------------------------

def _has_multiple_sentences(paragraph: str) -> bool:
    """Return True if *paragraph* contains at least 2 sentences."""
    # Count sentence-ending punctuation (beyond the first occurrence)
    endings = re.findall(r"[.!?]", paragraph)
    return len(endings) >= 2


def compute_paragraph_opener_diversity(text: str) -> dict:
    """Measure how diverse the opening words of paragraphs are."""
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    # Keep only paragraphs with at least 2 sentences
    paragraphs = [p for p in paragraphs if _has_multiple_sentences(p)]

    if len(paragraphs) <= 1:
        openers = []
        if paragraphs:
            words = paragraphs[0].split()[:3]
            opener = " ".join(w.lower().strip(string.punctuation) for w in words)
            openers.append(opener)
        return {
            "diversity": 1.0,
            "unique_openers": len(openers),
            "total_paragraphs": len(paragraphs),
            "penalty": 0.0,
            "openers": openers,
            "label": "High diversity",
        }

    openers: list[str] = []
    for para in paragraphs:
        words = para.split()[:3]
        opener = " ".join(w.lower().strip(string.punctuation) for w in words)
        openers.append(opener)

    unique = len(set(openers))
    total = len(openers)
    diversity = unique / total

    if diversity >= 0.70:
        penalty = 0.0
    else:
        penalty = (0.70 - diversity) / 0.70 * 100

    if diversity > 0.80:
        label = "High diversity"
    elif diversity >= 0.70:
        label = "Normal diversity"
    elif diversity >= 0.50:
        label = "Low diversity"
    elif diversity >= 0.30:
        label = "Very low diversity"
    else:
        label = "Minimal diversity"

    return {
        "diversity": round(diversity, 4),
        "unique_openers": unique,
        "total_paragraphs": total,
        "penalty": round(penalty, 2),
        "openers": openers,
        "label": label,
    }


# ---------------------------------------------------------------------------
# Hedge density
# ---------------------------------------------------------------------------

_HEDGE_PHRASES = [
    "it is possible",
    "to some extent",
    "in some cases",
]

_HEDGE_WORDS = [
    "may", "might", "could", "would", "suggests",
    "appears", "seems", "possibly", "perhaps", "likely",
]


def compute_hedge_density(text: str) -> dict:
    """Count hedging language relative to sentence count."""
    sentences = _tokenize_sentences(text)
    sentence_count = len(sentences) if sentences else 1
    text_lower = text.lower()

    hedge_count = 0
    hedges_found: list[str] = []

    # Count multi‐word phrases first
    for phrase in _HEDGE_PHRASES:
        count = len(re.findall(re.escape(phrase), text_lower))
        if count > 0:
            hedge_count += count
            hedges_found.extend([phrase] * count)

    # Count single hedge words (word‐boundary match)
    for word in _HEDGE_WORDS:
        count = len(re.findall(rf"\b{word}\b", text_lower))
        if count > 0:
            hedge_count += count
            hedges_found.extend([word] * count)

    density = hedge_count / sentence_count

    return {
        "density": round(density, 4),
        "hedge_count": hedge_count,
        "sentence_count": sentence_count,
        "hedges_found": hedges_found,
    }


# ---------------------------------------------------------------------------
# Composite score
# ---------------------------------------------------------------------------

def compute_composite_score(
    pattern_score: float,
    metrics: dict,
) -> dict:
    """Weighted composite AI‐probability score.

    *metrics* must contain keys: burstiness_penalty, vocab_diversity_penalty,
    structural_penalty.
    """
    burstiness_penalty = metrics.get("burstiness_penalty", 0)
    vocab_diversity_penalty = metrics.get("vocab_diversity_penalty", 0)
    structural_penalty = metrics.get("structural_penalty", 0)

    composite = (
        0.60 * pattern_score
        + 0.20 * burstiness_penalty
        + 0.10 * vocab_diversity_penalty
        + 0.10 * structural_penalty
    )

    if composite >= 60:
        risk_level = "High"
    elif composite >= 40:
        risk_level = "Elevated"
    elif composite >= 20:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        "composite_score": round(composite, 2),
        "components": {
            "pattern_score": round(pattern_score, 2),
            "burstiness_penalty": round(burstiness_penalty, 2),
            "vocab_diversity_penalty": round(vocab_diversity_penalty, 2),
            "structural_penalty": round(structural_penalty, 2),
        },
        "risk_level": risk_level,
        "label": f"{risk_level} risk ({round(composite, 1)}%)",
    }


# ---------------------------------------------------------------------------
# Aggregate helper
# ---------------------------------------------------------------------------

def compute_all_metrics(
    text: str,
    pattern_score: float = 0,
    structural_penalty: float = 0,
    non_native: bool = False,
) -> dict:
    """Compute every metric and return a comprehensive results dict."""
    burstiness = compute_burstiness(text, non_native=non_native)
    mtld = compute_mtld(text)
    sentence_lengths = burstiness["sentence_lengths"]
    fano = compute_fano_factor(sentence_lengths)
    slr = compute_sentence_length_range(sentence_lengths)
    opener_div = compute_paragraph_opener_diversity(text)
    hedge = compute_hedge_density(text)

    composite = compute_composite_score(
        pattern_score,
        {
            "burstiness_penalty": burstiness["penalty"],
            "vocab_diversity_penalty": mtld["penalty"],
            "structural_penalty": structural_penalty,
        },
    )

    return {
        "burstiness": burstiness,
        "mtld": mtld,
        "fano_factor": fano,
        "sentence_length_range": slr,
        "paragraph_opener_diversity": opener_div,
        "hedge_density": hedge,
        "composite": composite,
    }
