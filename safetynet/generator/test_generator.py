from pathlib import Path
import json

def clean_numbers(obj):
    """
    Recursively converts float values like 26.0 to int 26 if they are whole numbers.
    This fixes the Gson 'Double vs Integer' mismatch issue.
    """
    if isinstance(obj, float) and obj.is_integer():
        return int(obj)
    if isinstance(obj, dict):
        return {k: clean_numbers(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_numbers(v) for v in obj]
    return obj

def generate_junit_test(project_path: str, main_class: str, method_name: str, snapshot: dict) -> str:
    """
    Generates a generic JUnit 5 test.
    Handles SIDE EFFECTS, VOID methods, and NUMBER FORMATTING.
    """
    out_dir = Path(project_path) / ".safetynet"
    test_file = out_dir / "GeneratedSafetyNetTest.java"

    # Extract and clean snapshot data (fix 26.0 -> 26 issue)
    captured_data = snapshot["captured_return_value"]
    
    # 1. Expected Return Value (JSON)
    raw_return = captured_data.get("return_value")
    clean_return = clean_numbers(raw_return)
    expected_return_json = json.dumps(clean_return, separators=(',', ':')).replace('"', '\\"')
    
    # 2. Expected Argument State (for Side Effect checks)
    raw_args = captured_data.get("args_after")
    clean_args = clean_numbers(raw_args)
    
    expected_args_json = "null"
    if clean_args is not None:
        expected_args_json = json.dumps(clean_args, separators=(',', ':')).replace('"', '\\"')

    # 3. Argument Preparation (Demo-specific for updateUserAge)
    # Note: In a production tool, this would be dynamic/serialized. Hardcoded here for the demo.
    arg_setup_code = ""
    invoke_code = "Object actualResult = method.invoke(instance);"
    
    if method_name == "updateUserAge":
        arg_setup_code = f"""
        // Side Effect Demo: Reconstruct input argument
        Class<?> userClass = Class.forName("User");
        Object userArg = userClass.getConstructor(String.class, int.class).newInstance("Intern", 25);
        Object[] args = new Object[] {{ userArg }};
        """
        invoke_code = "Object actualResult = method.invoke(instance, args);"

    # JUNIT TEMPLATE
    test_code = f"""
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.lang.reflect.Method;

public class GeneratedSafetyNetTest {{

    @Test
    public void test_{method_name}_behavior() throws Exception {{
        // 1. ARRANGE
        String expectedReturnJson = "{expected_return_json}";
        String expectedArgsAfterJson = "{expected_args_json}";
        
        // Serialize nulls to match snapshot format
        Gson gson = new GsonBuilder().serializeNulls().create();
        
        Class<?> clazz = Class.forName("{main_class}");
        Object instance = clazz.getDeclaredConstructor().newInstance();
        
        // Find method
        Method method = null;
        try {{
            method = clazz.getMethod("{method_name}");
        }} catch (NoSuchMethodException e) {{
            // Fallback for parameterized methods (Specific to demo)
            method = clazz.getMethod("{method_name}", Class.forName("User"));
        }}

        {arg_setup_code}

        // 2. ACT
        {invoke_code}

        String actualReturnJson = gson.toJson(actualResult);
        
        // Capture argument state after execution
        String actualArgsAfterJson = "null";
        if ("{method_name}".equals("updateUserAge")) {{
            actualArgsAfterJson = gson.toJson(args);
        }}

        // 3. ASSERT
        // A) Return Value Check
        assertEquals(expectedReturnJson, actualReturnJson, "Return value mismatch!");

        // B) Side Effect Check
        if (!expectedArgsAfterJson.equals("null")) {{
            assertEquals(expectedArgsAfterJson, actualArgsAfterJson, "Side Effect (Argument State) mismatch!");
        }}
    }}
}}
"""
    test_file.write_text(test_code, encoding="utf-8")
    return str(test_file)