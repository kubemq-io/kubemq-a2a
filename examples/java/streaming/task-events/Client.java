import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "task-events-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var payload = Map.of(
            "jsonrpc", "2.0",
            "id", 1,
            "method", "message/stream",
            "params", Map.of(
                "message", Map.of("parts", List.of(Map.of("text", "Show me all event types")))
            )
        );

        var client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(60)).build();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .header("Accept", "text/event-stream")
            .timeout(Duration.ofSeconds(60))
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
            .build();

        System.out.println("Connecting to SSE stream...");
        var resp = client.send(req, HttpResponse.BodyHandlers.ofLines());

        Map<String, Integer> eventTypes = new LinkedHashMap<>();
        String currentEvent = null;

        for (var it = resp.body().iterator(); it.hasNext(); ) {
            String line = it.next();
            if (line.startsWith("event: ")) {
                currentEvent = line.substring(7).trim();
            } else if (line.startsWith("data: ") && currentEvent != null) {
                var data = MAPPER.readTree(line.substring(6));
                eventTypes.merge(currentEvent, 1, Integer::sum);

                switch (currentEvent) {
                    case "task.status" -> {
                        var p = data.path("payload");
                        System.out.println("  [STATUS]   progress=" + p.path("progress") + "/" + p.path("total"));
                    }
                    case "task.artifact" ->
                        System.out.println("  [ARTIFACT] name=" + data.path("payload").path("name").asText());
                    case "task.done" ->
                        System.out.println("  [DONE]     result=" + data.path("payload").path("final_result").asText());
                    case "task.error" ->
                        System.out.println("  [ERROR]    " + data.path("payload"));
                }

                if ("task.done".equals(currentEvent) || "task.error".equals(currentEvent)) break;
            }
        }

        System.out.println("\n--- Event Summary ---");
        int total = 0;
        for (var entry : eventTypes.entrySet()) {
            System.out.println("  " + entry.getKey() + ": " + entry.getValue());
            total += entry.getValue();
        }
        System.out.println("  Total: " + total);
    }
}
