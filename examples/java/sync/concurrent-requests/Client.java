import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "concurrent-agent-01";
    static final int NUM_REQUESTS = 20;
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();
        System.out.println("Sending " + NUM_REQUESTS + " concurrent requests...");

        List<CompletableFuture<HttpResponse<String>>> futures = new ArrayList<>();
        for (int i = 1; i <= NUM_REQUESTS; i++) {
            var payload = Map.of(
                "jsonrpc", "2.0",
                "id", i,
                "method", "message/send",
                "params", Map.of(
                    "message", Map.of("parts", List.of(Map.of("text", "Request #" + i)))
                )
            );
            var req = HttpRequest.newBuilder()
                .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
                .build();
            futures.add(client.sendAsync(req, HttpResponse.BodyHandlers.ofString()));
        }

        var all = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));
        all.join();

        int successes = 0, errors = 0, exceptions = 0;
        for (var future : futures) {
            try {
                var data = MAPPER.readTree(future.get().body());
                if (data.has("result")) successes++;
                else if (data.has("error")) errors++;
            } catch (Exception e) {
                exceptions++;
            }
        }

        System.out.println("\nResults:");
        System.out.println("  Successes:  " + successes);
        System.out.println("  Errors:     " + errors);
        System.out.println("  Exceptions: " + exceptions);
        System.out.println("  Total:      " + futures.size());

        assert successes == NUM_REQUESTS : "Expected " + NUM_REQUESTS + " successes, got " + successes;
        System.out.println("\nAll " + NUM_REQUESTS + " concurrent requests completed successfully!");
    }
}
