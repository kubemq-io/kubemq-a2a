import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "slow-stream-agent-01";
    static final int MAX_EVENTS = 2;
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var payload = Map.of(
            "jsonrpc", "2.0",
            "id", 1,
            "method", "message/stream",
            "params", Map.of(
                "message", Map.of("parts", List.of(Map.of("text", "I will disconnect early")))
            )
        );

        var client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(30)).build();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .header("Accept", "text/event-stream")
            .timeout(Duration.ofSeconds(30))
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
            .build();

        System.out.println("Connecting to stream (will disconnect after " + MAX_EVENTS + " events)...");
        var resp = client.send(req, HttpResponse.BodyHandlers.ofLines());

        int count = 0;
        String currentEvent = null;

        for (var it = resp.body().iterator(); it.hasNext(); ) {
            String line = it.next();
            if (line.startsWith("event: ")) {
                currentEvent = line.substring(7).trim();
            } else if (line.startsWith("data: ") && currentEvent != null) {
                count++;
                var data = MAPPER.readTree(line.substring(6));
                System.out.println("  Event " + count + ": [" + currentEvent + "] progress="
                    + data.path("payload").path("progress"));
                if (count >= MAX_EVENTS) {
                    System.out.println("\nDisconnecting after " + MAX_EVENTS + " events...");
                    break;
                }
            }
        }

        System.out.println("Client disconnected.");
        System.out.println("KubeMQ will detect the disconnect and clean up the stream.");
    }
}
