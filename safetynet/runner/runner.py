import subprocess
import os
from pathlib import Path

def compile_and_run(project_path: str, main_class: str, method_name: str = "execute") -> dict:
    """
    Compiles the target legacy project and executes the SafetyNet wrapper.
    """
    print(f">>> Compiling and Running {main_class}.{method_name}...")
    
    project = Path(project_path).resolve()
    root_dir = project.parent
    
    # Determine OS-specific path separator
    path_sep = ";" if os.name == 'nt' else ":"
    
    # Locate Gson JAR (Required for JSON serialization)
    gson_path = None
    possible_lib_paths = [project / "lib", root_dir / "lib"]
    
    for lib_dir in possible_lib_paths:
        if (lib_dir / "gson-2.10.1.jar").exists():
            gson_path = lib_dir / "gson-2.10.1.jar"
            break
            
    if not gson_path:
        return {
            "stage": "setup",
            "stdout": "",
            "stderr": f"Error: gson-2.10.1.jar not found in {possible_lib_paths}.",
            "exit_code": 1
        }

    # 1. Find Source Files
    # Exclude files inside .safetynet to prevent circular dependencies (e.g., existing tests)
    all_java_files = list(project.rglob("*.java"))
    java_files = [f for f in all_java_files if ".safetynet" not in str(f)]

    # Locate the SafetyNetWrapper.java (Search in project or root)
    wrapper_src = None
    if (project / "SafetyNetWrapper.java").exists():
        wrapper_src = project / "SafetyNetWrapper.java"
    elif (root_dir / "SafetyNetWrapper.java").exists():
        wrapper_src = root_dir / "SafetyNetWrapper.java"
    
    if wrapper_src:
        java_files.append(wrapper_src)
    else:
        return {
            "stage": "compile",
            "stdout": "",
            "stderr": "Error: SafetyNetWrapper.java not found in project or root directory.",
            "exit_code": 1
        }

    # 2. Compile
    target_classes = project / "target" / "classes"
    target_classes.mkdir(parents=True, exist_ok=True)

    compile_cmd = [
        "javac",
        "-cp", str(gson_path),
        "-d", str(target_classes),
    ] + [str(f) for f in java_files]

    print("   + Compiling...")
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)

    if compile_proc.returncode != 0:
        return {
            "stage": "compile",
            "stdout": compile_proc.stdout,
            "stderr": "Compilation Failed:\n" + compile_proc.stderr,
            "exit_code": compile_proc.returncode,
        }

    # 3. Run via Wrapper
    full_classpath = f"{target_classes}{path_sep}{gson_path}"
    
    run_cmd = [
        "java",
        "-cp", full_classpath,
        "SafetyNetWrapper",  # Execute our wrapper instead of main
        main_class,          # Arg 1: Target Class
        method_name          # Arg 2: Target Method
    ]

    print("   + Running...")
    run_proc = subprocess.run(run_cmd, capture_output=True, text=True, cwd=project)

    return {
        "stage": "run",
        "stdout": run_proc.stdout,
        "stderr": run_proc.stderr,
        "exit_code": run_proc.returncode,
    }