import argparse
from safetynet.runner.runner import compile_and_run
from safetynet.recorder.recorder import record_behavior
from safetynet.generator.test_generator import generate_junit_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to legacy java app folder")
    parser.add_argument("--main", required=True, help="Main class name, e.g., LegacyApp")
    args = parser.parse_args()

    result = compile_and_run(args.path, args.main)
    snapshot = record_behavior(result)
    test_path = generate_junit_test(args.path, args.main, snapshot)

    print("Run result:", result)
    print("Snapshot saved.")
    print("Generated test:", test_path)

if __name__ == "__main__":
    main()
