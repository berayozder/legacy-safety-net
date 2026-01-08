import com.google.gson.Gson;
import java.lang.reflect.Method;

/**
 * SafetyNetWrapper
 * Acts as an introspection agent to capture the runtime state of legacy code.
 */
public class SafetyNetWrapper {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: SafetyNetWrapper <ClassName> <MethodName>");
            System.exit(1);
        }

        String className = args[0];
        String methodName = args[1];

        try {
            // 1. Load Target Class via Reflection
            Class<?> clazz = Class.forName(className);
            Object instance = clazz.getDeclaredConstructor().newInstance();

            // 2. Locate Target Method
            Method method = clazz.getMethod(methodName);

            // 3. Invoke Method
            Object result = method.invoke(instance);

            // 4. Serialize Result to JSON
            Gson gson = new Gson();
            String jsonResult = gson.toJson(result);

            // 5. Output with specific marker for the Python recorder
            System.out.println("###SAFETYNET_RESULT###" + jsonResult);

        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}