package net.keimag.hakoirimusume;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Component;

@Component
public interface UserRepository extends CrudRepository<User, String> {
    Iterable<User> findByRoleGreaterThanEqual(int role);
    Iterable<User> findByRoleLessThan(int role);
}
