import java.util.*;

public class LegacyApp {
    public User getUserData() {
        return new User("Engineer", 42); 
    }

    public List<User> getBatchUsers() {
        List<User> users = new ArrayList<>();
        users.add(new User("Alice", 101));
        users.add(new User("Bob", 102));
        users.add(new User("Charlie", 103));
        return users;
    }
}