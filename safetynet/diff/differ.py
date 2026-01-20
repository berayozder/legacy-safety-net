from typing import Dict, List, Optional
import difflib

def diff_snapshots(baseline: Dict, current: Dict) -> Dict:
    """
    Compare two behavior snapshots (baseline vs current) and return structured differences.
    """
    diffs = {}

    # Check for Exit Code deviations
    if baseline.get("exit_code") != current.get("exit_code"):
        diffs["exit_code"] = {
            "severity": "critical",
            "before": baseline.get("exit_code"),
            "after": current.get("exit_code"),
        }

    # Check for Captured Return Value deviations
    if baseline.get("captured_return_value") != current.get("captured_return_value"):
        import json
        diffs["captured_return_value"] = {
            "severity": "high",
            "diff": text_diff(
                json.dumps(baseline.get("captured_return_value"), indent=2, sort_keys=True),
                json.dumps(current.get("captured_return_value"), indent=2, sort_keys=True)
            )
        }

    # Check for Standard Output deviations (raw_stdout)
    if baseline.get("raw_stdout", "") != current.get("raw_stdout", ""):
        diffs["stdout"] = {
            "severity": "low", # Low because return value is more important
            "diff": text_diff(
                baseline.get("raw_stdout", ""),
                current.get("raw_stdout", "")
            )
        }

    # Check for Standard Error deviations
    if baseline.get("stderr", "") != current.get("stderr", ""):
        diffs["stderr"] = {
            "severity": "medium",
            "diff": text_diff(
                baseline.get("stderr", ""),
                current.get("stderr", "")
            )
        }

    return diffs


def text_diff(before: str, after: str) -> List[str]:
    """
    Generates a unified diff for human-readable output.
    """
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)

    return list(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile="baseline",
            tofile="current",
        )
    )