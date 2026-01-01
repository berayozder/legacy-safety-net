import subprocess
from pathlib import Path

def compile_and_run(project_path: str, main_class: str) -> dict:
    project = Path(project_path)

    # 1️⃣ Try flat layout (Phase 1 legacy)
    java_files = list(project.glob("*.java"))

    # 2️⃣ Try Maven layout (Phase 1.5+)
    if not java_files:
        maven_src = project / "src" / "main" / "java"
        if maven_src.exists():
            java_files = list(maven_src.rglob("*.java"))

    if not java_files:
        raise FileNotFoundError(
            "No .java files found (checked project root and src/main/java)"
        )

    compile_cmd = ["javac"] + [str(p.relative_to(project)) for p in java_files]
    compile_proc = subprocess.run(
        compile_cmd,
        cwd=project,
        capture_output=True,
        text=True
    )

    if compile_proc.returncode != 0:
        return {
            "stage": "compile",
            "stdout": compile_proc.stdout,
            "stderr": compile_proc.stderr,
            "exit_code": compile_proc.returncode
        }

    run_cmd = [
        "java",
        "-cp",
        "target/classes",
        main_class
    ]

    run_proc = subprocess.run(
        run_cmd,
        cwd=project,
        capture_output=True,
        text=True
    )

    return {
        "stage": "run",
        "stdout": run_proc.stdout,
        "stderr": run_proc.stderr,
        "exit_code": run_proc.returncode
    }
