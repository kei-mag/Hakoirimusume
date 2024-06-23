plugins {
	java
	id("org.springframework.boot") version "3.3.1"
	id("io.spring.dependency-management") version "1.1.5"
	id("io.freefair.lombok") version "8.6"
}

group = "net.keimag"
version = "2.0.0-SNAPSHOT"

java {
	sourceCompatibility = JavaVersion.VERSION_17
}

configurations {
	compileOnly {
		extendsFrom(configurations.annotationProcessor.get())
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.hibernate.orm:hibernate-community-dialects:6.1.7.Final")
	implementation("com.linecorp.bot:line-bot-messaging-api-client:8.6.0")
	implementation("com.linecorp.bot:line-channel-access-token-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-webhook:8.6.0")
	implementation("com.linecorp.bot:line-bot-spring-boot-handler:8.6.0")
	implementation("org.springframework.boot:spring-boot-starter")
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("org.springframework.boot:spring-boot-starter-data-jpa")
	implementation("org.springframework.boot:spring-boot-starter-validation")
	implementation("org.xerial:sqlite-jdbc:3.46.0.0")
	annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<Test> {
	useJUnitPlatform()
}

tasks.bootJar {
	enabled = true
}

tasks.withType<JavaCompile>().configureEach {
	options.encoding = "UTF-8"
}