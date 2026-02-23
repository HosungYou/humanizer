#!/usr/bin/env python3
"""End-to-end JSON-RPC stdio test for humanizer MCP server."""
import json
import subprocess
import sys
import time

proc = subprocess.Popen(
    [sys.executable, "-m", "humanizer_mcp.server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="/Users/hosung/humanizer",
)


def send_request(id_, method, params=None):
    """Send JSON-RPC request and read response (blocking readline)."""
    msg = {"jsonrpc": "2.0", "id": id_, "method": method}
    if params is not None:
        msg["params"] = params
    raw = json.dumps(msg) + "\n"
    proc.stdin.write(raw.encode())
    proc.stdin.flush()
    line = proc.stdout.readline().decode().strip()
    if not line:
        return None
    return json.loads(line)


def send_notification(method, params=None):
    """Send JSON-RPC notification (no id, no response expected)."""
    msg = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        msg["params"] = params
    raw = json.dumps(msg) + "\n"
    proc.stdin.write(raw.encode())
    proc.stdin.flush()
    # No readline — notifications produce no response
    time.sleep(0.1)


# ── Phase 1: Handshake ──────────────────────────────────────
r = send_request(
    1,
    "initialize",
    {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "e2e-test", "version": "1.0"},
    },
)
assert r and "result" in r, f"Initialize failed: {r}"
server_name = r["result"]["serverInfo"]["name"]
print(f"INIT: OK  (server={server_name})")

send_notification("notifications/initialized")

# ── Phase 2: Tool calls ─────────────────────────────────────
AI_TEXT = (
    "The results demonstrate that the findings are consistent with previous research. "
    "Furthermore, the analysis reveals significant patterns. "
    "Moreover, the data suggests that additional investigation is warranted. "
    "It is important to note that these results have implications."
)
HUMAN_TEXT = (
    "Some results line up with earlier work, though not all patterns held. "
    "The data pointed in a few directions — some expected, others less so. "
    "A couple of metrics stood out. "
    "Worth digging into further, especially the outlier cases that did not fit neatly."
)

print()
print("=" * 60)
print("JSON-RPC STDIO E2E TEST — 4 MCP TOOLS")
print("=" * 60)

# ── Test 1: humanizer_metrics ───────────────────────────────
r = send_request(
    10,
    "tools/call",
    {
        "name": "humanizer_metrics",
        "arguments": {
            "text": AI_TEXT,
            "pattern_score": 45,
            "discipline": "psychology",
        },
    },
)
assert r and "result" in r, f"metrics call failed: {r}"
c = json.loads(r["result"]["content"][0]["text"])
print(f"""
[1/4] humanizer_metrics
  burstiness_cv:  {c['burstiness']['cv']}
  mtld:           {c['mtld']['mtld']}
  fano_factor:    {round(c['fano_factor'], 3)}
  hedge_density:  {c['hedge_density']['density']}
  opener_div:     {c['paragraph_opener_diversity']['diversity']}
  composite:      {c['composite']['composite_score']}%
  risk_level:     {c['composite']['risk_level']}
  STATUS:         PASS""")

# ── Test 2: humanizer_verify ────────────────────────────────
r = send_request(
    11,
    "tools/call",
    {
        "name": "humanizer_verify",
        "arguments": {
            "original_text": AI_TEXT,
            "humanized_text": HUMAN_TEXT,
            "pattern_score_before": 45,
            "pattern_score_after": 15,
        },
    },
)
assert r and "result" in r, f"verify call failed: {r}"
c = json.loads(r["result"]["content"][0]["text"])
print(f"""
[2/4] humanizer_verify
  needs_another_pass: {c['needs_another_pass']}
  regressions:        {len(c['regressions'])}
  recommendations:    {len(c.get('recommendations', []))}
  STATUS:             PASS""")

# ── Test 3: humanizer_diff ──────────────────────────────────
r = send_request(
    12,
    "tools/call",
    {
        "name": "humanizer_diff",
        "arguments": {
            "original_text": AI_TEXT,
            "humanized_text": HUMAN_TEXT,
        },
    },
)
assert r and "result" in r, f"diff call failed: {r}"
c = json.loads(r["result"]["content"][0]["text"])
deltas = c["deltas"]
print(f"\n[3/4] humanizer_diff")
for name, d in deltas.items():
    print(
        f"  {name:30s} {str(d['before']):>8} -> {str(d['after']):>8}  ({d['improvement_pct']}%)"
    )
print("  STATUS:             PASS")

# ── Test 4: humanizer_status ────────────────────────────────
r = send_request(
    13,
    "tools/call",
    {
        "name": "humanizer_status",
        "arguments": {
            "text": HUMAN_TEXT,
            "discipline": "psychology",
        },
    },
)
assert r and "result" in r, f"status call failed: {r}"
c = json.loads(r["result"]["content"][0]["text"])
metrics = c["metrics"]
print(f"\n[4/4] humanizer_status (discipline: {c['discipline']})")
for name, m in metrics.items():
    status_str = "PASS" if m["passed"] else "FAIL"
    print(
        f"  {name:30s} current={str(m['current']):>8}  target={str(m['target']):>6}  {status_str}"
    )
print(f"  readiness:          {c['readiness']}")
print("  STATUS:             PASS")

# ── Cleanup ─────────────────────────────────────────────────
proc.stdin.close()
proc.terminate()
proc.wait(timeout=5)

print()
print("=" * 60)
print("ALL 4 TOOLS PASSED — JSON-RPC STDIO E2E VERIFIED")
print("=" * 60)
