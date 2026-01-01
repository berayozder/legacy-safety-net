from typing import Dict, List
import difflib


def diff_snapshots(baseline: Dict, current: Dict) -> Dict:
    """
    Compare two behavior snapshots and return structured differences.
    """
    diffs = {}

    # Exit code diff
    if baseline.get("exit_code") != current.get("exit_code"):
        diffs["exit_code"] = {
            "severity": "critical",
            "before": baseline.get("exit_code"),
            "after": current.get("exit_code"),
        }

    # Stdout diff
    if baseline.get("stdout") != current.get("stdout"):
        diffs["stdout"] = {
            "severity": "medium",
            "diff": text_diff(
                baseline.get("stdout", ""),
                current.get("stdout", "")
            )
        }


    # Stderr diff
    if baseline.get("stderr") != current.get("stderr"):
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
    Line-based unified diff for human-readable output.
    """
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)

    return list(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile="before",
            tofile="after",
        )
    )
