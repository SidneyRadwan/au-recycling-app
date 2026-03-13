# syntax=docker/dockerfile:1

# ---- Build Stage ----
# Note: ensure a .dockerignore exists in backend/ to exclude:
#   .gradle/, build/, .git/, *.md, *.DS_Store
FROM gradle:8.10-jdk21 AS builder

WORKDIR /app

# Copy gradle wrapper and dependency specs first to leverage layer caching
COPY gradlew gradlew.bat settings.gradle build.gradle ./
COPY gradle/ gradle/

# Download dependencies (cached unless build files change)
RUN ./gradlew dependencies --no-daemon --quiet

# Copy source and build the fat jar, skipping tests (tests run in CI separately)
COPY src/ src/
RUN ./gradlew build -x test -x spotlessCheck --no-daemon

# ---- Runtime Stage ----
FROM eclipse-temurin:21-jre-alpine AS runtime

# Install curl for healthcheck
RUN apk add --no-cache curl

# JVM memory tuning — override at runtime via JAVA_OPTS env var
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+ExitOnOutOfMemoryError"

WORKDIR /app

# Copy only the built jar from the builder stage
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

# Run the application, honouring any JAVA_OPTS overrides
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
