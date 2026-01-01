import argparse
import json
from pathlib import Path

from safetynet.runner.runner import compile_and_run
from safetynet.recorder.recorder import record_behavior
from safetynet.generator.test_generator import generate_junit_test
from safetynet.diff.differ import diff_snapshots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to legacy java app folder")
    parser.add_argument("--main", required=True, help="Main class name, e.g., LegacyApp")
    parser.add_argument(
        "--accept",
        action="store_true",
        help="Accept behavior changes and update baseline snapshot"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if behavior changes are detected (useful for CI)"
    )

    args = parser.parse_args()

    # Run legacy system
    result = compile_and_run(args.path, args.main)
    snapshot = record_behavior(result)

    # Snapshot paths
    snapshot_dir = Path(args.path) / ".safetynet"
    snapshot_dir.mkdir(exist_ok=True)
    snapshot_path = snapshot_dir / "snapshot.json"
    diff_path = snapshot_dir / "last_diff.json"

    # Diff against baseline if exists
    if snapshot_path.exists():
        baseline = json.loads(snapshot_path.read_text())
        diffs = diff_snapshots(baseline, snapshot)

        if diffs:
            print("⚠️  Behavior changed:")

            for key, value in diffs.items():
                print(f"\n--- {key} ---")

                if isinstance(value, dict) and "diff" in value:
                    print("".join(value["diff"]))
                elif isinstance(value, dict):
                    print(f"{value['before']} → {value['after']}")

            # Save diff for CI / audit
            diff_path.write_text(json.dumps(diffs, indent=2))

            if not args.accept:
                msg = "\n❌ Behavior changed."
                if args.strict:
                    print(msg + " Failing because --strict is enabled.")
                    raise SystemExit(1)
                else:
                    print(msg + " Run with --accept to update baseline.")
                    return
        else:
            print("✅ No behavior changes detected.")
            if diff_path.exists():
                diff_path.unlink()
    else:
        print("No baseline snapshot found. Creating one.")

    # Update baseline ONLY if accepted or first run
    snapshot_path.write_text(json.dumps(snapshot, indent=2))

    # Generate test (baseline-aligned)
    test_path = generate_junit_test(args.path, args.main, snapshot)

    print("Run result:", result)
    print("Snapshot saved.")
    print("Generated test:", test_path)


if __name__ == "__main__":
    main()
