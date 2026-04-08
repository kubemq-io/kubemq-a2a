import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "heartbeat-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();

        for (int i = 1; i <= 3; i++) {
            var req = HttpRequest.newBuilder()
                .uri(URI.create(KUBEMQ_URL + "/agents/heartbeat"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(
                    MAPPER.writeValueAsString(Map.of("agent_id", AGENT_ID))))
                .build();
            var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
            var data = MAPPER.readTree(resp.body());
            System.out.println("Heartbeat " + i + ": status=" + resp.statusCode()
                + " last_seen=" + data.path("last_seen").asText());
            if (i < 3) Thread.sleep(2000);
        }

        System.out.println("\n=== Final agent state ===");
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/" + AGENT_ID))
            .GET().build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var data = MAPPER.readTree(resp.body());
        System.out.println("registered_at: " + data.path("registered_at").asText());
        System.out.println("last_seen:     " + data.path("last_seen").asText());
        System.out.println("\nHeartbeat cycle completed!");
    }
}
