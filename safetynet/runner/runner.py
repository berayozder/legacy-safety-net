import subprocess
from pathlib import Path

def compile_and_run(project_path: str, main_class: str) -> dict:
    project = Path(project_path)

    # Compile all .java files in the folder (simple MVP)
    java_files = list(project.glob("*.java"))
    if not java_files:
        raise FileNotFoundError("No .java files found in project path")

    compile_cmd = ["javac"] + [str(p.name) for p in java_files]
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

    run_cmd = ["java", main_class]
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
