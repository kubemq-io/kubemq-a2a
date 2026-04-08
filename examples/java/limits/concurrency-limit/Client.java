import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "concurrency-agent-01";
    static final int NUM_REQUESTS = 101;
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();

        System.out.println("Sending " + NUM_REQUESTS + " concurrent requests (limit is 100)...");

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
                .timeout(Duration.ofSeconds(30))
                .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
                .build();
            futures.add(client.sendAsync(req, HttpResponse.BodyHandlers.ofString()));
        }

        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

        int successes = 0, concurrencyErrors = 0, otherErrors = 0, exceptions = 0;
        for (var future : futures) {
            try {
                var data = MAPPER.readTree(future.get().body());
                if (data.has("result")) {
                    successes++;
                } else if (data.has("error")) {
                    if (data.path("error").path("code").asInt() == -32603) concurrencyErrors++;
                    else otherErrors++;
                }
            } catch (Exception e) {
                exceptions++;
            }
        }

        System.out.println("\nResults:");
        System.out.println("  Successes:            " + successes);
        System.out.println("  Concurrency errors:   " + concurrencyErrors + " (code -32603)");
        System.out.println("  Other errors:         " + otherErrors);
        System.out.println("  Exceptions:           " + exceptions);
        System.out.println("  Total:                " + futures.size());

        assert concurrencyErrors >= 1 : "Expected at least 1 concurrency limit error";
        System.out.println("\nConcurrency limit enforced — " + concurrencyErrors + " request(s) rejected!");
    }
}
