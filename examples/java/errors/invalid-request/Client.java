import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "echo-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();

        System.out.println("=== Test 1: Invalid JSON ===");
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString("{invalid json!!!}"))
            .build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var data = MAPPER.readTree(resp.body());
        var error = data.path("error");
        System.out.println("  Code: " + error.path("code").asInt() + " (expected -32700)");
        System.out.println("  Message: " + error.path("message").asText());

        System.out.println("\n=== Test 2: Missing method field ===");
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(
                MAPPER.writeValueAsString(Map.of("jsonrpc", "2.0", "id", 1, "params", Map.of()))))
            .build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        data = MAPPER.readTree(resp.body());
        error = data.path("error");
        System.out.println("  Code: " + error.path("code").asInt() + " (expected -32600)");
        System.out.println("  Message: " + error.path("message").asText());

        System.out.println("\n=== Test 3: Bad jsonrpc version ===");
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(
                MAPPER.writeValueAsString(Map.of(
                    "jsonrpc", "1.0", "id", 1, "method", "message/send", "params", Map.of()))))
            .build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        data = MAPPER.readTree(resp.body());
        error = data.path("error");
        System.out.println("  Code: " + error.path("code").asInt() + " (expected -32600)");
        System.out.println("  Message: " + error.path("message").asText());

        System.out.println("\nAll invalid request errors demonstrated!");
    }
}
