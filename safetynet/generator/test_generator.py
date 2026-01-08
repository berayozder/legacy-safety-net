from pathlib import Path
import json

def generate_junit_test(project_path: str, main_class: str, method_name: str, snapshot: dict) -> str:
    """
    Generates a reproducible JUnit 5 test case based on the captured snapshot.
    """
    out_dir = Path(project_path) / ".safetynet"
    test_file = out_dir / "GeneratedSafetyNetTest.java"

    # Serialize the captured object back to a JSON string for the Java test.
    # We use separators=(',', ':') to remove whitespace, ensuring format compatibility with Gson's default output.
    expected_json_str = json.dumps(snapshot["captured_return_value"], separators=(',', ':')).replace('"', '\\"')

    # JUnit 5 Template utilizing Gson and Reflection
    test_code = f"""
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.Gson;
import java.lang.reflect.Method;

public class GeneratedSafetyNetTest {{

    @Test
    public void test_{method_name}_behavior() throws Exception {{
        // 1. ARRANGE
        String expectedJson = "{expected_json_str}";
        Gson gson = new Gson();
        
        Class<?> clazz = Class.forName("{main_class}");
        Object instance = clazz.getDeclaredConstructor().newInstance();
        Method method = clazz.getMethod("{method_name}");

        // 2. ACT (Invoke the real method via Reflection)
        Object actualResult = method.invoke(instance);
        String actualJson = gson.toJson(actualResult);

        // 3. ASSERT (Compare serialized states)
        assertEquals(expectedJson, actualJson, "Method return value has changed (Regression detected)!");
    }}
}}
"""
    test_file.write_text(test_code, encoding="utf-8")
    return str(test_file)