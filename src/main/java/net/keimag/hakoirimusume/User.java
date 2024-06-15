package net.keimag.hakoirimusume;
import lombok.Data;
import org.springframework.data.annotation.Id;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Data
@Entity
@Table(name = "users")
public class User {
    @jakarta.persistence.Id
    @Id
    private String id;
    private int role;
    private int state;
    private String requestTime;
}
