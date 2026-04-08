import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "deregister-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();

        System.out.println("=== Verify agent exists ===");
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/" + AGENT_ID))
            .GET().build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("GET /agents/" + AGENT_ID + ": " + resp.statusCode());

        System.out.println("\n=== Deregister via POST ===");
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/deregister"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(
                MAPPER.writeValueAsString(Map.of("agent_id", AGENT_ID))))
            .build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("POST /agents/deregister: " + resp.statusCode());

        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/" + AGENT_ID))
            .GET().build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("GET /agents/" + AGENT_ID + " after deregister: " + resp.statusCode());

        System.out.println("\n=== Re-register for DELETE test ===");
        var card = Map.of(
            "agent_id", AGENT_ID,
            "name", "Deregister Test Agent",
            "url", "http://localhost:18080/",
            "skills", List.of(),
            "defaultInputModes", List.of("text"),
            "defaultOutputModes", List.of("text"),
            "protocolVersions", List.of("1.0")
        );
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/register"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(card)))
            .build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("Re-registered: " + resp.statusCode());

        System.out.println("\n=== Deregister via DELETE ===");
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/" + AGENT_ID))
            .DELETE().build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("DELETE /agents/" + AGENT_ID + ": " + resp.statusCode());

        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/" + AGENT_ID))
            .GET().build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("GET /agents/" + AGENT_ID + " after delete: " + resp.statusCode());

        System.out.println("\nBoth deregistration methods demonstrated successfully!");
    }
}
