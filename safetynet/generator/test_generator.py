from pathlib import Path
from safetynet.recorder.recorder import save_snapshot

def generate_junit_test(project_path: str, main_class: str, snapshot: dict) -> str:
    snapshot_path = save_snapshot(project_path, snapshot)

    out_dir = Path(project_path) / ".safetynet"
    test_file = out_dir / "GeneratedSafetyNetTest.java"

    expected_stdout = snapshot["stdout"].replace("\\", "\\\\").replace("\"", "\\\"")

    test_code = f"""\
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

public class GeneratedSafetyNetTest {{

    @Test
    public void test_{main_class}_stdout_is_stable() throws Exception {{
        ProcessBuilder pb = new ProcessBuilder("java", "{main_class}");
        pb.directory(new File("{Path(project_path).as_posix()}"));
        pb.redirectErrorStream(true);

        Process p = pb.start();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (InputStream is = p.getInputStream()) {{
            is.transferTo(baos);
        }}
        int code = p.waitFor();

        String output = baos.toString().trim();
        assertEquals(0, code, "Exit code changed");
        assertEquals("{expected_stdout.strip()}", output, "Stdout changed");
    }}
}}
"""
    test_file.write_text(test_code, encoding="utf-8")
    return str(test_file)
