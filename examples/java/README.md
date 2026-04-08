# Java examples

KubeMQ A2A examples using **`com.sun.net.httpserver.HttpServer`** (JDK) for agents and **`java.net.http.HttpClient`** for clients. JSON is handled with **Jackson** (`ObjectMapper`). The **a2a-java-sdk-client** artifact is on the classpath for SDK alignment; examples use direct HTTP and JSON-RPC as specified.

## Requirements

- JDK 17+
- Maven 3.9+

## Build

From this directory:

```bash
mvn compile
```

Resolve dependencies only:

```bash
mvn dependency:resolve
```

## Run an example

After example sources are added under each scenario folder, run from that folder (or pass `exec.mainClass`), for example:

```bash
cd registry/register-agent
mvn -f ../../pom.xml exec:java -Dexec.mainClass=Agent
```

When each scenario ships its own layout, prefer the documented command in that scenario’s `README.md` (typically `mvn exec:java` with `-Dexec.mainClass=Agent` or `Client`).

## Environment

Default KubeMQ URL is `http://localhost:9090` unless constants are changed in the sources.

## Stack (see spec §5.3)

| Role | Library |
|------|---------|
| A2A SDK (declared) | `io.github.a2asdk:a2a-java-sdk-client` |
| JSON | `com.fasterxml.jackson.core:jackson-databind` |
| Agent HTTP server | `com.sun.net.httpserver.HttpServer` |
| HTTP client | `java.net.http.HttpClient` |

See [pom.xml](pom.xml).
