# humanizer-mcp

MCP server for precise stylometric metrics in academic text humanization.

Replaces LLM estimation of burstiness, MTLD, and other quantitative metrics with exact algorithmic computation. Designed for the [Diverga](https://github.com/HosungYou/Diverga) humanization pipeline (G5/G6/F5 agents).

## Installation

### Via Diverga Plugin (Recommended)

Install the [Diverga plugin](https://github.com/HosungYou/Diverga) for Claude Code — the humanizer MCP server is included automatically.

### Standalone via uvx

```bash
uvx humanizer-mcp
```

### Standalone via pip

```bash
pip install humanizer-mcp
```

## Claude Code Configuration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "humanizer": {
      "command": "uvx",
      "args": ["humanizer-mcp"]
    }
  }
}
```

## Tools

| Tool | Purpose |
|------|---------|
| `humanizer_metrics` | Full stylometric analysis: burstiness CV, MTLD, Fano factor, opener diversity, hedge density, discourse metrics, composite score |
| `humanizer_verify` | Before/after comparison with regression detection and `needs_another_pass` recommendation |
| `humanizer_diff` | Per-metric delta report with improvement percentages |
| `humanizer_status` | Readiness assessment with discipline-specific calibration |
| `humanizer_discourse` | Standalone discourse and psycholinguistic metrics: hapax rate, contraction density, surprisal, connective diversity, pronoun density, question ratio, abstract noun ratio |

## Metrics

### Core Stylometric Metrics

| Metric | Algorithm | Human Baseline | AI Typical |
|--------|-----------|---------------|------------|
| Burstiness CV | SD / Mean of sentence word counts | > 0.45 | < 0.30 |
| MTLD | Forward + backward pass, TTR threshold 0.72 | > 80 | < 60 |
| Fano Factor | Variance / Mean of sentence lengths | > 1 | < 1 |
| Sentence Length Range | max - min word count | > 25 | < 15 |
| Opener Diversity | unique first-3-words / total paragraphs | > 0.70 | < 0.50 |
| Hedge Density | hedge words / sentence count | varies | high |
| Composite Score | Weighted formula (see v3.0 formula below) | < 30% | > 60% |

### v3.0 Discourse and Psycholinguistic Metrics (New)

| Metric | Description |
|--------|-------------|
| `hapax_rate` | Proportion of words appearing exactly once; higher values indicate richer vocabulary |
| `contraction_density` | Contractions per sentence; human writing uses more contractions than AI |
| `paragraph_length_variance` | Variance in paragraph word counts; low variance is an AI signal |
| `surprisal_proxy` | Estimated word-level surprisal using SUBTLEX-US word frequency data; AI text tends toward lower surprisal (more predictable word choices) |
| `surprisal_autocorrelation` | Lag-1 autocorrelation of surprisal values across sentences; captures rhythmic predictability |
| `connective_diversity` | Type-token ratio of discourse connectives (however, therefore, moreover, etc.); AI overuses a small set |
| `pronoun_density` | First and second person pronouns per sentence; human academic text varies by discipline |
| `question_ratio` | Proportion of sentences ending with a question mark; rhetorical questions are a human signal |
| `abstract_noun_ratio` | Proportion of abstract nouns (nominalizations); AI text tends toward nominalization-heavy prose |

## v3.0 Composite Scoring Formula

```
AI_Probability = (0.40 * pattern_score)
              + (0.15 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
              + (0.15 * discourse_penalty)
              + (0.10 * psycholinguistic_penalty)
```

| Component | Weight | Source |
|-----------|--------|--------|
| `pattern_score` | 40% | Phase 1 pattern detection, normalized 0-100 |
| `burstiness_penalty` | 15% | `max(0, (0.45 - CV) / 0.45 * 100)` |
| `vocab_diversity_penalty` | 10% | `max(0, (80 - MTLD) / 80 * 100)` |
| `structural_penalty` | 10% | S7+S8+S9+S10 weighted scores, normalized 0-100 |
| `discourse_penalty` | 15% | Connective diversity, hapax rate, contraction density, paragraph variance |
| `psycholinguistic_penalty` | 10% | Surprisal proxy, surprisal autocorrelation, pronoun density, question ratio, abstract noun ratio |

## Discipline Calibration

| Discipline | Burstiness Threshold | MTLD Threshold |
|------------|---------------------|----------------|
| Default | 0.45 | 80 |
| Psychology | 0.40 | 75 |
| Management | 0.42 | 78 |
| Education | 0.43 | 76 |
| STEM | 0.38 | 72 |
| Humanities | 0.50 | 85 |
| Social Sciences | 0.43 | 77 |

Pass `discipline="psychology"` to any tool for field-specific thresholds.

## Development

```bash
git clone https://github.com/HosungYou/humanizer.git
cd humanizer
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT

## Links

- [Diverga Plugin](https://github.com/HosungYou/Diverga)
- [Release Notes](https://github.com/HosungYou/humanizer/blob/main/RELEASE_NOTES.md)
