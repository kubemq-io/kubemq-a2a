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
    static final String AGENT_ID = "slow-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var payload = Map.of(
            "jsonrpc", "2.0",
            "id", 1,
            "method", "message/send",
            "params", Map.of(
                "message", Map.of("parts", List.of(Map.of("text", "This will timeout"))),
                "configuration", Map.of("timeout", 1)
            )
        );

        var client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(30)).build();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .timeout(Duration.ofSeconds(30))
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
            .build();

        System.out.println("Sending request with timeout=1 to slow agent (5s delay)...");
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var data = MAPPER.readTree(resp.body());
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(data));

        var error = data.path("error");
        System.out.println("\nError code:    " + error.path("code").asInt());
        System.out.println("Error message: " + error.path("message").asText());

        assert error.path("code").asInt() == -32001 : "Expected -32001, got " + error.path("code").asInt();
        System.out.println("\nTimeout error (-32001) received as expected!");
    }
}
