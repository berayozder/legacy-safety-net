# Legacy Safety Net 🕸️

**"The goal is not refactoring. The goal is safety."**

A robust tool designed to bring safety to legacy Java codebases by automatically generating "Golden Master" regression tests.

## 🚀 Why I Built This

Refactoring legacy code is inherently dangerous. Often, these systems lack comprehensive test suites, meaning a single line change could silently break critical functionality.

**Legacy Safety Net** creates a protective barrier around your code. It records the exact behavior of your application in its current state, allowing you to refactor with the confidence that any deviation will be instantly detected.

## ✨ Capabilities

*   **🔍 Golden Master Testing:** Captures input/output snapshots of your methods to establish a baseline of "correct" behavior.
*   **👀 Side-Effect Detection:** Goes beyond simple return values to detect state mutations in void methods (e.g., modifying an object passed as an argument).
*   **🧠 Smart Serialization:** Handles complex Java objects and sanitizes JSON type mismatches (like Double vs Integer) that often plague cross-language serialization.
*   **⚡ Automatic JUnit Generation:** Generates standard, ready-to-run JUnit 5 test cases based on the captured snapshots.

## 🛠️ How It Works

1.  **Orchestration:** Python scripts manage the build and execution process.
2.  **Spying:** A lightweight Java wrapper uses reflection to invoke your target method and capture its output.
3.  **Snapshotting:** The object state is serialized to JSON using Gson.
4.  **Verification:** Future runs are compared against the "Golden Master" snapshot. Any difference triggers a failure.

## 📋 Prerequisites

*   **Python:** 3.8 or higher
*   **Java:** JDK 8 or higher
*   **Gson:** (The tool expects Gson to be available or handles it via the included lib folder if present. *Note: Ensure `google-gson` is in your classpath if not using the provided setup.*)

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/berayozder/legacy-safety-net.git
    cd legacy-safety-net
    ```

2.  (Optional) Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

## 📖 Usage

The tool is invoked via the `safetynet/cli.py` script.

### Basic Command

```bash
python safetynet/cli.py <path_to_source_root> --main <ClassName> --method <MethodName>
```

### Example

We have included a sample legacy application in `safetynet/src_legacy`. To test the `getUserData` method of the `LegacyApp` class:

```bash
python safetynet/cli.py safetynet/src_legacy --main LegacyApp --method getUserData
```

**What happens:**
1.  The tool compiles the Java code.
2.  It runs `LegacyApp.getUserData`.
3.  It saves the result to `safetynet/src_legacy/.safetynet/snapshot.json`.
4.  It generates a JUnit test file.

### Dealing with Changes

If you modify the Java code and the behavior changes:

1.  Run the tool again.
2.  It will report **"⚠️ Behavior changed"** and show a diff of the JSON output.
3.  If the change is intentional, approve it by running:
    ```bash
    python safetynet/cli.py safetynet/src_legacy --main LegacyApp --method getUserData --accept
    ```

### Strict Mode (CI/CD)

For automated pipelines where any change should fail the build:

```bash
python safetynet/cli.py safetynet/src_legacy --main LegacyApp --method getUserData --strict
```

## 📂 Project Structure

```
legacy-safety-net/
├── safetynet/
│   ├── cli.py              # Main entry point
│   ├── SafetyNetWrapper.java # Java agent for capturing state
│   ├── diff/               # Logic for comparing JSON snapshots
│   ├── generator/          # JUnit test generation logic
│   ├── recorder/           # Orchestrates Java execution
│   └── src_legacy/         # Example legacy application for testing
└── README.md
```

## 🔧 Troubleshooting

*   **"No return value captured"**: Ensure your target method is public and static, or that the class has a no-args constructor if it's an instance method.
*   **Compilation Errors**: Check that `javac` is in your system PATH.
