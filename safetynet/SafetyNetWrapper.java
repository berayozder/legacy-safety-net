import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

/**
 * SafetyNetWrapper
 * Introspection agent that captures argument states before and after execution 
 * to detect side effects and return values.
 */
public class SafetyNetWrapper {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: SafetyNetWrapper <ClassName> <MethodName>");
            System.exit(1);
        }

        String className = args[0];
        String methodName = args[1];
        
        // Configure Gson to include nulls for accurate regression testing
        Gson gson = new GsonBuilder().serializeNulls().create();

        try {
            Class<?> clazz = Class.forName(className);
            Object instance = clazz.getDeclaredConstructor().newInstance();

            // 1. ARGUMENT PREPARATION
            // Note: In a full production version, arguments would be deserialized from a config file.
            // For this demo, we manually setup the 'User' object scenario.
            Object[] methodArgs = null;
            Class<?>[] paramTypes = null;

            if (methodName.equals("updateUserAge")) {
                methodArgs = new Object[] { new User("Intern", 25) };
                paramTypes = new Class<?>[] { User.class };
            } else {
                methodArgs = null;
                paramTypes = null;
            }

            Method method = clazz.getMethod(methodName, paramTypes);

            // 2. CAPTURE BEFORE STATE
            String argsBeforeJson = (methodArgs != null) ? gson.toJson(methodArgs) : "null";

            // 3. EXECUTE METHOD
            Object result = method.invoke(instance, methodArgs);

            // 4. CAPTURE AFTER STATE (Detect Side Effects)
            String argsAfterJson = (methodArgs != null) ? gson.toJson(methodArgs) : "null";
            String returnJson = gson.toJson(result);

            // 5. CONSTRUCT FINAL REPORT
            Map<String, Object> finalReport = new HashMap<>();
            finalReport.put("return_value", gson.fromJson(returnJson, Object.class));
            finalReport.put("args_before", gson.fromJson(argsBeforeJson, Object.class));
            finalReport.put("args_after", gson.fromJson(argsAfterJson, Object.class));

            // Output the result with a unique delimiter for the Python parser
            System.out.println("###SAFETYNET_RESULT###" + gson.toJson(finalReport));

        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}