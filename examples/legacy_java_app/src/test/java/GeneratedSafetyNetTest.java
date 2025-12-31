import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

public class GeneratedSafetyNetTest {

    @Test
    public void test_LegacyApp_stdout_is_stable() throws Exception {
        ProcessBuilder pb = new ProcessBuilder(
            "java",
            "-cp",
            "target/classes",
            "LegacyApp"
        );

        pb.directory(new File("."));
        pb.redirectErrorStream(true);

        Process p = pb.start();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (InputStream is = p.getInputStream()) {
            byte[] buffer = new byte[1024];
            int read;
            while ((read = is.read(buffer)) != -1) {
                baos.write(buffer, 0, read);
            }
        }

        int code = p.waitFor();

        String output = baos.toString().trim();
        assertEquals(0, code, "Exit code changed");
        assertEquals("Hello from legacy system", output, "Stdout changed");
    }
}
