package net.keimag.hakoirimusume;

import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import static org.assertj.core.api.Assertions.assertThat;
import java.util.Objects;

@SpringBootTest
@ContextConfiguration(classes = HakoirimusumeApplication.class)
class AuthorizerTests {

    private static final Logger log = LoggerFactory.getLogger(AuthorizerTests.class);
    @Autowired
    HakoirimusumeProperties properties;

    @Test
    void authorizeTest() {
        Authorizer authorizer = new Authorizer(properties);
        assertThat(authorizer.authorize("aikotoba")).isFalse();
        String aikotoba = authorizer.generateNewAikotoba("test1");
        assertThat(authorizer.authorize(aikotoba)).isTrue();
        aikotoba = authorizer.generateNewAikotoba("test1");
        assertThat(authorizer.authorize("wrongAikotoba")).isFalse();
        aikotoba = authorizer.generateNewAikotoba("test1");
        assertThat(authorizer.generateNewAikotoba("test2")).isNull();
        assertThat(authorizer.generateNewAikotoba("test1")).isNotBlank();
    }
}
