
plugins {
	java
	id("org.springframework.boot") version "3.2.5"
	id("io.spring.dependency-management") version "1.1.4"
}

group = "net.keimag"
version = "0.0.1-SNAPSHOT"

java {
	sourceCompatibility = JavaVersion.VERSION_17
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter")
	implementation("org.springframework.boot:spring-boot-starter-validation")
	implementation("org.projectlombok:lombok:1.18.30")
	compileOnly("org.springframework.boot:spring-boot-configuration-processor") // for adding custom configuration to application.yml

	// LINE Bot SDK
	implementation("com.linecorp.bot:line-bot-messaging-api-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-insight-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-manage-audience-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-module-attach-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-module-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-shop-client:8.6.0")
	implementation("com.linecorp.bot:line-channel-access-token-client:8.6.0")
	implementation("com.linecorp.bot:line-liff-client:8.6.0")
	implementation("com.linecorp.bot:line-bot-webhook:8.6.0")
	implementation("com.linecorp.bot:line-bot-parser:8.6.0") // You don't need to depend on this explicitly.
	implementation("com.linecorp.bot:line-bot-spring-boot-webmvc:8.6.0")
	implementation("com.linecorp.bot:line-bot-spring-boot-client:8.6.0") // If you want to write spring-boot API client
	implementation("com.linecorp.bot:line-bot-spring-boot-handler:8.6.0") // You don't need to depend on this explicitly.
	implementation("com.linecorp.bot:line-bot-spring-boot-web:8.6.0") // You don't need to depend on this explicitly.

	// for HTTP Request
	implementation("com.squareup.okhttp3:okhttp:4.12.0")

	// for SQLite3 Support
	implementation("org.xerial:sqlite-jdbc:3.45.3.0")

	// for general testing
	testImplementation("org.springframework.boot:spring-boot-starter-test")
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