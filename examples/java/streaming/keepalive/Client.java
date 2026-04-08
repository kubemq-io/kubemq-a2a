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
    static final String AGENT_ID = "keepalive-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var payload = Map.of(
            "jsonrpc", "2.0",
            "id", 1,
            "method", "message/stream",
            "params", Map.of(
                "message", Map.of("parts", List.of(Map.of("text", "Long-running task")))
            )
        );

        var client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(120)).build();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .header("Accept", "text/event-stream")
            .timeout(Duration.ofSeconds(120))
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
            .build();

        long start = System.nanoTime();
        System.out.println("Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...");

        var resp = client.send(req, HttpResponse.BodyHandlers.ofLines());
        String currentEvent = null;

        for (var it = resp.body().iterator(); it.hasNext(); ) {
            String line = it.next();
            double elapsed = (System.nanoTime() - start) / 1_000_000_000.0;

            if (line.startsWith("event: ")) {
                currentEvent = line.substring(7).trim();
            } else if (line.startsWith("data: ") && currentEvent != null) {
                System.out.printf("  [%6.1fs] [%s] %s%n", elapsed, currentEvent, line.substring(6));
                if ("task.done".equals(currentEvent) || "task.error".equals(currentEvent)) break;
            } else if (line.startsWith(":")) {
                System.out.printf("  [%6.1fs] [keepalive]%n", elapsed);
            }
        }

        double total = (System.nanoTime() - start) / 1_000_000_000.0;
        System.out.printf("%nStream completed in %.1fs%n", total);
        System.out.println("Keepalive kept the connection alive during long pauses!");
    }
}
