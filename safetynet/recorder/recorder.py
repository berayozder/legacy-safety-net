import json
from pathlib import Path

def record_behavior(run_result: dict) -> dict:
    snapshot = {
        "stage": run_result["stage"],
        "stdout": run_result["stdout"],
        "stderr": run_result["stderr"],
        "exit_code": run_result["exit_code"]
    }
    return snapshot

def save_snapshot(project_path: str, snapshot: dict) -> str:
    out_dir = Path(project_path) / ".safetynet"
    out_dir.mkdir(exist_ok=True)

    out_file = out_dir / "snapshot.json"
    out_file.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return str(out_file)
