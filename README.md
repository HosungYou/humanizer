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
| `humanizer_metrics` | Full stylometric analysis: burstiness CV, MTLD, Fano factor, opener diversity, hedge density, composite score |
| `humanizer_verify` | Before/after comparison with regression detection and `needs_another_pass` recommendation |
| `humanizer_diff` | Per-metric delta report with improvement percentages |
| `humanizer_status` | Readiness assessment with discipline-specific calibration |

## Metrics

| Metric | Algorithm | Human Baseline | AI Typical |
|--------|-----------|---------------|------------|
| Burstiness CV | SD / Mean of sentence word counts | > 0.45 | < 0.30 |
| MTLD | Forward + backward pass, TTR threshold 0.72 | > 80 | < 60 |
| Fano Factor | Variance / Mean of sentence lengths | > 1 | < 1 |
| Sentence Length Range | max - min word count | > 25 | < 15 |
| Opener Diversity | unique first-3-words / total paragraphs | > 0.70 | < 0.50 |
| Hedge Density | hedge words / sentence count | varies | high |
| Composite Score | Weighted (pattern 60% + burstiness 20% + vocab 10% + structural 10%) | < 30% | > 60% |

## Discipline Calibration

| Discipline | Burstiness Threshold | MTLD Threshold |
|------------|---------------------|----------------|
| Default | 0.45 | 80 |
| Psychology | 0.40 | 75 |
| Management | 0.42 | 78 |
| Education | 0.43 | 76 |

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
