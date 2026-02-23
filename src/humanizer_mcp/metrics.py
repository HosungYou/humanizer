"""Quantitative stylometric metrics for academic text humanization.

All algorithms are pure Python — no external NLP libraries required.
"""

import json
import math
import os
import re
import string
from collections import Counter


# ---------------------------------------------------------------------------
# Discipline calibration profiles
# ---------------------------------------------------------------------------

DISCIPLINE_PROFILES: dict[str, dict] = {
    "default": {"burstiness_threshold": 0.45, "mtld_threshold": 80, "contraction_target": 0.10, "pronoun_target": 0.05, "hapax_target": 0.45},
    "psychology": {"burstiness_threshold": 0.40, "mtld_threshold": 75, "contraction_target": 0.08, "pronoun_target": 0.04, "hapax_target": 0.42},
    "management": {"burstiness_threshold": 0.42, "mtld_threshold": 78, "contraction_target": 0.12, "pronoun_target": 0.06, "hapax_target": 0.44},
    "education": {"burstiness_threshold": 0.43, "mtld_threshold": 76, "contraction_target": 0.15, "pronoun_target": 0.08, "hapax_target": 0.40},
    "stem": {"burstiness_threshold": 0.38, "mtld_threshold": 82, "contraction_target": 0.02, "pronoun_target": 0.02, "hapax_target": 0.48},
    "humanities": {"burstiness_threshold": 0.48, "mtld_threshold": 85, "contraction_target": 0.18, "pronoun_target": 0.10, "hapax_target": 0.50},
    "social_sciences": {"burstiness_threshold": 0.44, "mtld_threshold": 79, "contraction_target": 0.10, "pronoun_target": 0.06, "hapax_target": 0.44},
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
# Word frequency data (lazy-loaded, cached)
# ---------------------------------------------------------------------------

_WORD_FREQUENCIES: dict[str, float] | None = None


def _load_word_frequencies() -> dict[str, float]:
    """Load the bundled word frequency dictionary (log10 values).

    The file is loaded once and cached in a module-level variable.
    """
    global _WORD_FREQUENCIES
    if _WORD_FREQUENCIES is not None:
        return _WORD_FREQUENCIES

    data_path = os.path.join(
        os.path.dirname(__file__), "data", "word_frequencies.json",
    )
    try:
        with open(data_path, "r", encoding="utf-8") as fh:
            _WORD_FREQUENCIES = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        _WORD_FREQUENCIES = {}

    return _WORD_FREQUENCIES


# ---------------------------------------------------------------------------
# Helper: tokenise text into lowercase words
# ---------------------------------------------------------------------------

def _tokenize_words(text: str) -> list[str]:
    """Return lowercase alphabetic tokens from *text*."""
    raw = text.lower().split()
    tokens = [t.strip(string.punctuation) for t in raw]
    return [t for t in tokens if t and any(c.isalpha() for c in t)]


# ---------------------------------------------------------------------------
# Hapax legomena rate
# ---------------------------------------------------------------------------

def compute_hapax_rate(text: str) -> dict:
    """Compute hapax legomena rate (words appearing exactly once / total words).

    Human writing typically exceeds 0.50; AI-generated text tends to fall
    below 0.35 due to repetitive vocabulary selection.
    """
    tokens = _tokenize_words(text)
    total_words = len(tokens)

    if total_words == 0:
        return {
            "rate": 0.0,
            "hapax_count": 0,
            "total_words": 0,
            "label": "Insufficient text",
        }

    freq = Counter(tokens)
    hapax_count = sum(1 for count in freq.values() if count == 1)
    rate = hapax_count / total_words

    if rate >= 0.50:
        label = "High hapax rate (human-like)"
    elif rate >= 0.35:
        label = "Moderate hapax rate"
    elif rate >= 0.20:
        label = "Low hapax rate (AI-typical)"
    else:
        label = "Very low hapax rate"

    return {
        "rate": round(rate, 4),
        "hapax_count": hapax_count,
        "total_words": total_words,
        "label": label,
    }


# ---------------------------------------------------------------------------
# Contraction density
# ---------------------------------------------------------------------------

_CONTRACTION_RE = re.compile(
    r"\b\w+(?:'(?:t|s|re|ve|ll|d|m))\b",
    re.IGNORECASE,
)


def compute_contraction_density(text: str) -> dict:
    """Compute contractions per sentence.

    Human academic writing: > 0.15 contractions/sentence.
    AI-generated text: < 0.05 contractions/sentence.
    """
    sentences = _tokenize_sentences(text)
    sentence_count = len(sentences) if sentences else 1

    contractions_found = _CONTRACTION_RE.findall(text)
    contraction_count = len(contractions_found)
    density = contraction_count / sentence_count

    return {
        "density": round(density, 4),
        "contraction_count": contraction_count,
        "sentence_count": sentence_count,
        "contractions_found": contractions_found,
    }


# ---------------------------------------------------------------------------
# Paragraph length variance
# ---------------------------------------------------------------------------

def compute_paragraph_length_variance(text: str) -> dict:
    """Compute the coefficient of variation (CV) of paragraph word counts.

    Human: CV > 0.40 (varied paragraph sizes).
    AI: CV < 0.25 (uniform paragraph sizes).
    """
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if len(paragraphs) < 2:
        lengths = [len(p.split()) for p in paragraphs] if paragraphs else []
        return {
            "cv": 0.0,
            "mean_length": float(lengths[0]) if lengths else 0.0,
            "std_dev": 0.0,
            "paragraph_count": len(paragraphs),
            "paragraph_lengths": lengths,
            "label": "Insufficient paragraphs",
        }

    lengths = [len(p.split()) for p in paragraphs]
    mean_length = sum(lengths) / len(lengths)
    if mean_length == 0:
        return {
            "cv": 0.0,
            "mean_length": 0.0,
            "std_dev": 0.0,
            "paragraph_count": len(paragraphs),
            "paragraph_lengths": lengths,
            "label": "Insufficient text",
        }

    variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    cv = std_dev / mean_length

    if cv >= 0.50:
        label = "High variance (human-like)"
    elif cv >= 0.40:
        label = "Normal variance"
    elif cv >= 0.25:
        label = "Low variance (AI-typical)"
    else:
        label = "Very low variance"

    return {
        "cv": round(cv, 4),
        "mean_length": round(mean_length, 2),
        "std_dev": round(std_dev, 2),
        "paragraph_count": len(paragraphs),
        "paragraph_lengths": lengths,
        "label": label,
    }


# ---------------------------------------------------------------------------
# Surprisal proxy (word-frequency based)
# ---------------------------------------------------------------------------

_MAX_SURPRISAL = 20.0  # Cap for words not in frequency dictionary


def _compute_word_surprisals(tokens: list[str]) -> list[float]:
    """Return per-word surprisal values using the bundled frequency data.

    surprisal = log2(1 / 10^log_freq)  =  -log_freq * log2(10)
    """
    freqs = _load_word_frequencies()
    log2_of_10 = math.log2(10)
    surprisals: list[float] = []
    for token in tokens:
        log_freq = freqs.get(token)
        if log_freq is not None and log_freq > 0:
            surprisals.append(log_freq * log2_of_10)  # Higher freq -> lower surprisal... invert:
        else:
            surprisals.append(_MAX_SURPRISAL)

    # Actually: surprisal = -log2(p). If log10(freq) = lf, then p ~ 10^lf (normalized).
    # Higher lf means more common = LESS surprising.
    # surprisal = -log2(10^lf) = -lf * log2(10).  But lf is positive, so surprisal is negative?
    # The convention: lf is log10 of frequency count or Zipf value.
    # For a Zipf value z, surprisal ~ -z * log2(10) would be negative.
    # Let's use: surprisal = max_surprisal - lf * log2(10).
    # This way: high-freq word (lf=5) -> low surprisal; rare word (lf=1) -> high surprisal.
    surprisals_corrected: list[float] = []
    for token in tokens:
        log_freq = freqs.get(token)
        if log_freq is not None and log_freq > 0:
            s = _MAX_SURPRISAL - log_freq * log2_of_10
            surprisals_corrected.append(max(s, 0.0))
        else:
            surprisals_corrected.append(_MAX_SURPRISAL)
    return surprisals_corrected


def compute_surprisal_proxy(text: str) -> dict:
    """Compute word surprisal proxy using bundled frequency data.

    Variance of surprisal across words measures the mix of common and rare
    words.  Human text shows high variance (unpredictable mix); AI text
    shows low variance (uniformly medium-frequency vocabulary).
    """
    tokens = _tokenize_words(text)

    if len(tokens) < 10:
        return {
            "variance": 0.0,
            "mean_surprisal": 0.0,
            "std_dev": 0.0,
            "token_count": len(tokens),
            "label": "Insufficient text",
        }

    surprisals = _compute_word_surprisals(tokens)

    mean_s = sum(surprisals) / len(surprisals)
    variance = sum((s - mean_s) ** 2 for s in surprisals) / len(surprisals)
    std_dev = math.sqrt(variance)

    if variance >= 25.0:
        label = "High surprisal variance (human-like)"
    elif variance >= 15.0:
        label = "Moderate surprisal variance"
    elif variance >= 8.0:
        label = "Low surprisal variance (AI-typical)"
    else:
        label = "Very low surprisal variance"

    return {
        "variance": round(variance, 4),
        "mean_surprisal": round(mean_s, 4),
        "std_dev": round(std_dev, 4),
        "token_count": len(tokens),
        "label": label,
    }


# ---------------------------------------------------------------------------
# Surprisal autocorrelation
# ---------------------------------------------------------------------------

def compute_surprisal_autocorrelation(text: str) -> dict:
    """Compute 2nd-order autocorrelation of surprisal differences.

    Human text has high autocorrelation (irregular rhythm of word difficulty).
    AI text has low autocorrelation (smooth, predictable difficulty flow).
    """
    tokens = _tokenize_words(text)

    if len(tokens) < 15:
        return {
            "autocorrelation": 0.0,
            "label": "Insufficient text",
        }

    surprisals = _compute_word_surprisals(tokens)

    # First differences
    diffs = [surprisals[i + 1] - surprisals[i] for i in range(len(surprisals) - 1)]

    if len(diffs) < 4:
        return {
            "autocorrelation": 0.0,
            "label": "Insufficient text",
        }

    # Lag-2 autocorrelation
    n = len(diffs)
    mean_d = sum(diffs) / n
    var_d = sum((d - mean_d) ** 2 for d in diffs) / n

    if var_d == 0:
        return {
            "autocorrelation": 0.0,
            "label": "No variation in surprisal",
        }

    lag = 2
    if n <= lag:
        return {
            "autocorrelation": 0.0,
            "label": "Insufficient text",
        }

    cov = sum(
        (diffs[i] - mean_d) * (diffs[i + lag] - mean_d)
        for i in range(n - lag)
    ) / (n - lag)

    autocorr = cov / var_d

    if abs(autocorr) >= 0.30:
        label = "High autocorrelation (human-like)"
    elif abs(autocorr) >= 0.15:
        label = "Moderate autocorrelation"
    else:
        label = "Low autocorrelation (AI-typical)"

    return {
        "autocorrelation": round(autocorr, 4),
        "label": label,
    }


# ---------------------------------------------------------------------------
# Connective diversity
# ---------------------------------------------------------------------------

_CONNECTIVES = [
    "furthermore", "moreover", "however", "nevertheless", "consequently",
    "therefore", "additionally", "similarly", "conversely", "meanwhile",
    "nonetheless", "alternatively", "specifically", "notably", "indeed",
    "accordingly", "likewise", "thus", "hence", "yet",
    "still", "instead", "otherwise", "subsequently", "formerly",
    "simultaneously", "ultimately", "initially", "previously", "apparently",
    "certainly", "evidently", "presumably", "undoubtedly", "arguably",
    "admittedly", "frankly", "importantly", "significantly", "interestingly",
    "surprisingly", "ironically", "paradoxically", "incidentally", "namely",
    "essentially", "fundamentally", "primarily", "secondarily", "thirdly",
    "firstly", "secondly", "finally", "lastly", "overall",
    "broadly", "generally", "particularly", "especially", "chiefly",
    "mainly", "largely", "mostly", "partly", "wholly",
    "altogether", "equally", "comparatively", "relatively", "increasingly",
    "correspondingly", "proportionally", "respectively", "collectively",
    "individually", "mutually", "jointly", "separately", "independently",
]

_CONNECTIVE_PHRASES = [
    "in contrast", "on the other hand", "as a result", "in addition",
    "for instance", "in particular", "for example", "in other words",
    "on the contrary", "by contrast", "in fact", "as such",
    "to this end", "in turn", "at the same time", "in this regard",
    "to that end", "in this context", "with respect to", "in light of",
]


def compute_connective_diversity(text: str) -> dict:
    """Compute unique connectives / total connectives.

    Human: > 0.70 (varied connective usage).
    AI: < 0.50 (repetitive connective patterns).
    """
    text_lower = text.lower()

    found: list[str] = []

    # Multi-word phrases first
    for phrase in _CONNECTIVE_PHRASES:
        count = len(re.findall(re.escape(phrase), text_lower))
        found.extend([phrase] * count)

    # Single-word connectives
    for conn in _CONNECTIVES:
        count = len(re.findall(rf"\b{re.escape(conn)}\b", text_lower))
        found.extend([conn] * count)

    total_count = len(found)

    if total_count == 0:
        return {
            "diversity": 0.0,
            "unique_count": 0,
            "total_count": 0,
            "connectives_found": [],
            "label": "No connectives found",
        }

    unique_count = len(set(found))
    diversity = unique_count / total_count

    if diversity >= 0.70:
        label = "High connective diversity"
    elif diversity >= 0.50:
        label = "Moderate connective diversity"
    elif diversity >= 0.30:
        label = "Low connective diversity (AI-typical)"
    else:
        label = "Very low connective diversity"

    return {
        "diversity": round(diversity, 4),
        "unique_count": unique_count,
        "total_count": total_count,
        "connectives_found": found,
        "label": label,
    }


# ---------------------------------------------------------------------------
# Pronoun density (first-person)
# ---------------------------------------------------------------------------

_FIRST_PERSON_RE = re.compile(
    r"\b(?:I|we|my|our|me|us|myself|ourselves)\b",
    re.IGNORECASE,
)


def compute_pronoun_density(text: str) -> dict:
    """Compute first-person pronouns (I/we/my/our/me/us) per sentence.

    Density varies by discipline.  AI-generated text typically has near-zero
    first-person pronoun usage.
    """
    sentences = _tokenize_sentences(text)
    sentence_count = len(sentences) if sentences else 1

    pronouns_found = _FIRST_PERSON_RE.findall(text)
    pronoun_count = len(pronouns_found)
    density = pronoun_count / sentence_count

    return {
        "density": round(density, 4),
        "pronoun_count": pronoun_count,
        "sentence_count": sentence_count,
        "pronouns_found": pronouns_found,
    }


# ---------------------------------------------------------------------------
# Question ratio
# ---------------------------------------------------------------------------

def compute_question_ratio(text: str) -> dict:
    """Compute the ratio of questions to total sentences.

    Human: > 0.03 (occasional rhetorical questions).
    AI: < 0.01 (almost never asks questions).
    """
    sentences = _tokenize_sentences(text)
    total_sentences = len(sentences) if sentences else 1

    question_count = sum(1 for s in sentences if s.rstrip().endswith("?"))
    ratio = question_count / total_sentences

    return {
        "ratio": round(ratio, 4),
        "question_count": question_count,
        "sentence_count": total_sentences,
    }


# ---------------------------------------------------------------------------
# Abstract noun ratio
# ---------------------------------------------------------------------------

_ABSTRACT_SUFFIXES = (
    "tion", "sion", "ness", "ity", "ment", "ance", "ence", "ism", "ship",
)


def compute_abstract_noun_ratio(text: str) -> dict:
    """Compute abstract nouns / total words (by suffix heuristic).

    Human: < 0.30 (balanced vocabulary).
    AI: > 0.45 (over-reliance on abstract nominalisations).
    """
    tokens = _tokenize_words(text)
    total_words = len(tokens)

    if total_words == 0:
        return {
            "ratio": 0.0,
            "abstract_count": 0,
            "total_words": 0,
            "abstracts_found": [],
            "label": "Insufficient text",
        }

    abstracts_found: list[str] = []
    for token in tokens:
        if len(token) > 4 and token.endswith(_ABSTRACT_SUFFIXES):
            abstracts_found.append(token)

    abstract_count = len(abstracts_found)
    ratio = abstract_count / total_words

    if ratio <= 0.15:
        label = "Low abstraction (concrete)"
    elif ratio <= 0.30:
        label = "Normal abstraction"
    elif ratio <= 0.45:
        label = "High abstraction (AI-leaning)"
    else:
        label = "Very high abstraction (AI-typical)"

    return {
        "ratio": round(ratio, 4),
        "abstract_count": abstract_count,
        "total_words": total_words,
        "abstracts_found": abstracts_found[:50],  # Limit list size
        "label": label,
    }


# ---------------------------------------------------------------------------
# Composite score
# ---------------------------------------------------------------------------

def compute_composite_score(
    pattern_score: float,
    metrics: dict,
    scoring_version: str = "v3",
) -> dict:
    """Weighted composite AI-probability score.

    v2 formula (4 components):
        0.60*pattern + 0.20*burstiness + 0.10*vocab + 0.10*structural

    v3 formula (6 components):
        0.40*pattern + 0.15*burstiness + 0.10*vocab + 0.10*structural
        + 0.15*discourse + 0.10*psycholinguistic
    """
    burstiness_penalty = metrics.get("burstiness_penalty", 0)
    vocab_diversity_penalty = metrics.get("vocab_diversity_penalty", 0)
    structural_penalty = metrics.get("structural_penalty", 0)
    discourse_penalty = metrics.get("discourse_penalty", 0)
    psycholinguistic_penalty = metrics.get("psycholinguistic_penalty", 0)

    if scoring_version == "v2":
        composite = (
            0.60 * pattern_score
            + 0.20 * burstiness_penalty
            + 0.10 * vocab_diversity_penalty
            + 0.10 * structural_penalty
        )
        components = {
            "pattern_score": round(pattern_score, 2),
            "burstiness_penalty": round(burstiness_penalty, 2),
            "vocab_diversity_penalty": round(vocab_diversity_penalty, 2),
            "structural_penalty": round(structural_penalty, 2),
        }
    else:  # v3
        composite = (
            0.40 * pattern_score
            + 0.15 * burstiness_penalty
            + 0.10 * vocab_diversity_penalty
            + 0.10 * structural_penalty
            + 0.15 * discourse_penalty
            + 0.10 * psycholinguistic_penalty
        )
        components = {
            "pattern_score": round(pattern_score, 2),
            "burstiness_penalty": round(burstiness_penalty, 2),
            "vocab_diversity_penalty": round(vocab_diversity_penalty, 2),
            "structural_penalty": round(structural_penalty, 2),
            "discourse_penalty": round(discourse_penalty, 2),
            "psycholinguistic_penalty": round(psycholinguistic_penalty, 2),
        }

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
        "scoring_version": scoring_version,
        "components": components,
        "risk_level": risk_level,
        "label": f"{risk_level} risk ({round(composite, 1)}%)",
    }


# ---------------------------------------------------------------------------
# Aggregate helper
# ---------------------------------------------------------------------------

def _compute_discourse_penalty(
    connective_div: dict,
    question_ratio: dict,
    pronoun_density: dict,
) -> float:
    """Derive a 0-100 discourse penalty from connective, question, and pronoun metrics.

    Each sub-metric contributes equally (weight 1/3).
    """
    # Connective diversity: ideal >= 0.70, penalty rises as diversity drops
    cd = connective_div.get("diversity", 0.0)
    if cd >= 0.70:
        cd_pen = 0.0
    else:
        cd_pen = (0.70 - cd) / 0.70 * 100

    # Question ratio: ideal >= 0.03, penalty rises as ratio drops
    qr = question_ratio.get("ratio", 0.0)
    if qr >= 0.03:
        qr_pen = 0.0
    else:
        qr_pen = (0.03 - qr) / 0.03 * 100

    # Pronoun density: ideal >= 0.05, penalty rises as density drops
    pd = pronoun_density.get("density", 0.0)
    if pd >= 0.05:
        pd_pen = 0.0
    else:
        pd_pen = (0.05 - pd) / 0.05 * 100

    return round((cd_pen + qr_pen + pd_pen) / 3, 2)


def _compute_psycholinguistic_penalty(
    hapax: dict,
    contraction: dict,
    abstract_noun: dict,
    surprisal: dict,
) -> float:
    """Derive a 0-100 psycholinguistic penalty from hapax, contraction,
    abstract noun, and surprisal metrics.

    Each sub-metric contributes equally (weight 1/4).
    """
    # Hapax rate: ideal >= 0.45, penalty rises as rate drops
    hr = hapax.get("rate", 0.0)
    if hr >= 0.45:
        hr_pen = 0.0
    else:
        hr_pen = (0.45 - hr) / 0.45 * 100

    # Contraction density: ideal >= 0.10, penalty rises as density drops
    cd = contraction.get("density", 0.0)
    if cd >= 0.10:
        cd_pen = 0.0
    else:
        cd_pen = (0.10 - cd) / 0.10 * 100

    # Abstract noun ratio: ideal <= 0.30, penalty rises as ratio increases
    ar = abstract_noun.get("ratio", 0.0)
    if ar <= 0.30:
        ar_pen = 0.0
    else:
        ar_pen = min((ar - 0.30) / 0.30 * 100, 100.0)

    # Surprisal variance: ideal >= 15.0, penalty rises as variance drops
    sv = surprisal.get("variance", 0.0)
    if sv >= 15.0:
        sv_pen = 0.0
    else:
        sv_pen = (15.0 - sv) / 15.0 * 100

    return round((hr_pen + cd_pen + ar_pen + sv_pen) / 4, 2)


def compute_all_metrics(
    text: str,
    pattern_score: float = 0,
    structural_penalty: float = 0,
    non_native: bool = False,
    scoring_version: str = "v3",
) -> dict:
    """Compute every metric and return a comprehensive results dict."""
    # --- Original metrics ---
    burstiness = compute_burstiness(text, non_native=non_native)
    mtld = compute_mtld(text)
    sentence_lengths = burstiness["sentence_lengths"]
    fano = compute_fano_factor(sentence_lengths)
    slr = compute_sentence_length_range(sentence_lengths)
    opener_div = compute_paragraph_opener_diversity(text)
    hedge = compute_hedge_density(text)

    # --- v3 metrics: Tier 1 ---
    hapax = compute_hapax_rate(text)
    contraction = compute_contraction_density(text)
    para_var = compute_paragraph_length_variance(text)
    surprisal = compute_surprisal_proxy(text)
    surprisal_ac = compute_surprisal_autocorrelation(text)

    # --- v3 metrics: Tier 2 ---
    connective_div = compute_connective_diversity(text)
    pronoun = compute_pronoun_density(text)
    question = compute_question_ratio(text)
    abstract_noun = compute_abstract_noun_ratio(text)

    # --- Derived penalties for v3 composite ---
    discourse_penalty = _compute_discourse_penalty(
        connective_div, question, pronoun,
    )
    psycholinguistic_penalty = _compute_psycholinguistic_penalty(
        hapax, contraction, abstract_noun, surprisal,
    )

    composite = compute_composite_score(
        pattern_score,
        {
            "burstiness_penalty": burstiness["penalty"],
            "vocab_diversity_penalty": mtld["penalty"],
            "structural_penalty": structural_penalty,
            "discourse_penalty": discourse_penalty,
            "psycholinguistic_penalty": psycholinguistic_penalty,
        },
        scoring_version=scoring_version,
    )

    return {
        "burstiness": burstiness,
        "mtld": mtld,
        "fano_factor": fano,
        "sentence_length_range": slr,
        "paragraph_opener_diversity": opener_div,
        "hedge_density": hedge,
        "hapax_rate": hapax,
        "contraction_density": contraction,
        "paragraph_length_variance": para_var,
        "surprisal_proxy": surprisal,
        "surprisal_autocorrelation": surprisal_ac,
        "connective_diversity": connective_div,
        "pronoun_density": pronoun,
        "question_ratio": question,
        "abstract_noun_ratio": abstract_noun,
        "discourse_penalty": discourse_penalty,
        "psycholinguistic_penalty": psycholinguistic_penalty,
        "composite": composite,
    }
