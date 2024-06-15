package net.keimag.hakoirimusume;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

@Service
public class UserService {
    public static final int BANNED_USER = -1;
    public static final int UNAUTHORIZED_USER = 0;
    public static final int USER = 1;
    public static final int ADMIN = 2;

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public void resetStates() {
        Iterable<User> users = userRepository.findAll();
        users.forEach(user -> {
            user.setState(0);
            user.setRequestTime(null);
        });
        userRepository.saveAll(users);
    }

    public Integer getState(String userId) {
        return userRepository.findById(userId).map(User::getState).orElse(null);
    }

    public void setState(String userId, int state) {
        userRepository.findById(userId).ifPresent(user -> {
            user.setState(state);
            userRepository.save(user);
        });
    }

    public List<String> getUsers() {
        return StreamSupport.stream(userRepository.findByRoleGreaterThanEqual(USER).spliterator(), false)
                .map(User::getId)
                .collect(Collectors.toList());
    }

    public List<String> getAdmins() {
        return StreamSupport.stream(userRepository.findByRoleGreaterThanEqual(ADMIN).spliterator(), false)
                .map(User::getId)
                .collect(Collectors.toList());
    }

    public List<String> getBannedUsers() {
        return StreamSupport.stream(userRepository.findByRoleLessThan(BANNED_USER).spliterator(), false)
                .map(User::getId)
                .collect(Collectors.toList());
    }

    public boolean addUser(String userId) {
        if (userRepository.existsById(userId)) {
            User user = userRepository.findById(userId).orElse(null);
            return user == null || user.getRole() >= UNAUTHORIZED_USER;
        } else {
            User user = new User();
            user.setId(userId);
            userRepository.save(user);
            return true;
        }
    }

    public void removeUser(String userId) {
        userRepository.deleteById(userId);
    }

    public Integer getRole(String userId) {
        return userRepository.findById(userId).map(User::getRole).orElse(null);
    }

    public boolean isSatisfiedRole(String userId, int level) {
        return userRepository.findById(userId).map(user -> user.getRole() >= level).orElse(false);
    }

    public void setRole(String userId, int level) {
        userRepository.findById(userId).ifPresent(user -> {
            user.setRole(level);
            userRepository.save(user);
        });
    }


    // TODO: Delete this method when releasing the product.
    public void printTable() {
        Iterable<User> users = userRepository.findAll();
        users.forEach(System.out::println);
    }
}

