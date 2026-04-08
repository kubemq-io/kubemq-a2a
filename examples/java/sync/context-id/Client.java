import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "context-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var payload = Map.of(
            "jsonrpc", "2.0",
            "id", 1,
            "method", "message/send",
            "params", Map.of(
                "message", Map.of("parts", List.of(Map.of("text", "Track this request"))),
                "contextId", "ctx-001"
            )
        );

        var client = HttpClient.newHttpClient();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
            .build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var data = MAPPER.readTree(resp.body());
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(data));

        var returnedCtx = data.path("result").path("contextId").asText(null);
        System.out.println("\nSent contextId:     ctx-001");
        System.out.println("Received contextId: " + returnedCtx);

        if ("ctx-001".equals(returnedCtx)) {
            System.out.println("Context ID correlation verified!");
        } else {
            System.out.println("Warning: contextId mismatch");
        }
    }
}
