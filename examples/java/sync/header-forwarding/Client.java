import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "header-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var payload = Map.of(
            "jsonrpc", "2.0",
            "id", 1,
            "method", "message/send",
            "params", Map.of(
                "message", Map.of("parts", List.of(Map.of("text", "Check my headers")))
            )
        );

        var client = HttpClient.newHttpClient();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/a2a/" + AGENT_ID))
            .header("Content-Type", "application/json")
            .header("X-Custom-Header", "my-custom-value")
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(payload)))
            .build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var data = MAPPER.readTree(resp.body());
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(data));

        var received = data.path("result").path("received_headers");
        System.out.println("\nForwarded headers: " + received);

        boolean foundCustom = false;
        boolean foundCaller = false;
        var fields = received.fields();
        while (fields.hasNext()) {
            var entry = fields.next();
            if (entry.getKey().equalsIgnoreCase("X-Custom-Header")) foundCustom = true;
            if (entry.getKey().equalsIgnoreCase("X-Kubemq-Caller-Id")) foundCaller = true;
        }

        if (foundCustom) System.out.println("X-Custom-Header was forwarded successfully!");
        else System.out.println("Warning: X-Custom-Header not found in forwarded headers");

        if (foundCaller) System.out.println("X-KubeMQ-Caller-ID injected by KubeMQ");
    }
}
