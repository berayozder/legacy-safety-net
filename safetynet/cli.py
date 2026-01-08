import argparse
import json
from pathlib import Path

from runner.runner import compile_and_run
from recorder.recorder import record_behavior
from generator.test_generator import generate_junit_test
from diff.differ import diff_snapshots


def main():
    parser = argparse.ArgumentParser(description="Legacy Safety Net - Automated Regression Testing Tool")
    
    parser.add_argument("path", help="Path to the legacy Java application folder")
    
    # Target specification
    parser.add_argument("--main", required=True, help="Target Class name (e.g. LegacyApp)")
    parser.add_argument("--method", required=True, help="Target Method to test (e.g. getUserData)")
    
    # Behavior control
    parser.add_argument(
        "--accept",
        action="store_true",
        help="Accept behavior changes and update the baseline snapshot"
    )
    
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if behavior changes are detected (Recommended for CI pipelines)"
    )

    args = parser.parse_args()

    print(f"🚀 Starting SafetyNet for {args.main}.{args.method}...")

    # Execute the compilation and run process
    result = compile_and_run(args.path, args.main, method_name=args.method)
    
    # Handle execution failures
    if result["exit_code"] != 0:
        print("❌ Execution failed!")
        print("Stderr:", result["stderr"])
        return

    # Capture behavior (Object serialization)
    snapshot = record_behavior(result)
    
    if snapshot.get("captured_return_value") is None:
        print("⚠️ Warning: No return value captured. Did SafetyNetWrapper run correctly?")
        print("Raw Output:", result["stdout"])

    # Define snapshot paths
    snapshot_dir = Path(args.path) / ".safetynet"
    snapshot_dir.mkdir(exist_ok=True)
    snapshot_path = snapshot_dir / "snapshot.json"
    diff_path = snapshot_dir / "last_diff.json"

    # Behavior Difference Analysis
    if snapshot_path.exists():
        try:
            baseline = json.loads(snapshot_path.read_text(encoding="utf-8"))
            diffs = diff_snapshots(baseline, snapshot)

            if diffs:
                print("⚠️  Behavior changed:")
                for key, value in diffs.items():
                    print(f"\n--- {key} ---")
                    if isinstance(value, dict):
                        print(value) 

                # Log differences
                diff_path.write_text(json.dumps(diffs, indent=2), encoding="utf-8")

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
        except json.JSONDecodeError:
            print("⚠️ Existing snapshot was corrupted. Overwriting.")

    else:
        print("No baseline snapshot found. Creating new baseline.")

    # Save Snapshot (If accepted or first run)
    snapshot_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

    # Generate the JUnit test file
    test_path = generate_junit_test(args.path, args.main, args.method, snapshot)

    print("Snapshot saved.")
    print(f"✅ Generated JUnit test: {test_path}")


if __name__ == "__main__":
    main()