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

    # Check for Standard Output deviations
    if baseline.get("stdout") != current.get("stdout"):
        diffs["stdout"] = {
            "severity": "medium",
            "diff": text_diff(
                baseline.get("stdout", ""),
                current.get("stdout", "")
            )
        }

    # Check for Standard Error deviations
    if baseline.get("stderr") != current.get("stderr"):
        diffs["stderr"] = {
            "severity": "medium",
            "diff": text_diff(
                baseline.get("stderr", ""),
                current.get("stderr", "")
            )
        }

    # Note: Future versions should include deep diffing of "captured_return_value" JSON objects.

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