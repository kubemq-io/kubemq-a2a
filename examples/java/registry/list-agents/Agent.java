import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpServer;

import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;

public class Agent {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final int BASE_PORT = 18080;
    static final ObjectMapper MAPPER = new ObjectMapper();

    static final List<Map<String, Object>> AGENTS = List.of(
        Map.of(
            "agent_id", "echo-agent-01",
            "name", "Echo Agent",
            "description", "Echoes back messages",
            "version", "1.0.0",
            "url", "http://localhost:" + BASE_PORT + "/",
            "skills", List.of(Map.of("id", "echo", "name", "Echo",
                "description", "Echo skill", "tags", List.of("echo", "test"))),
            "defaultInputModes", List.of("text"),
            "defaultOutputModes", List.of("text"),
            "protocolVersions", List.of("1.0")
        ),
        Map.of(
            "agent_id", "translate-agent-01",
            "name", "Translate Agent",
            "description", "Translates text",
            "version", "1.0.0",
            "url", "http://localhost:" + (BASE_PORT + 1) + "/",
            "skills", List.of(Map.of("id", "translate", "name", "Translate",
                "description", "Translation skill", "tags", List.of("translate", "nlp"))),
            "defaultInputModes", List.of("text"),
            "defaultOutputModes", List.of("text"),
            "protocolVersions", List.of("1.0")
        ),
        Map.of(
            "agent_id", "summarize-agent-01",
            "name", "Summarize Agent",
            "description", "Summarizes text",
            "version", "1.0.0",
            "url", "http://localhost:" + (BASE_PORT + 2) + "/",
            "skills", List.of(Map.of("id", "summarize", "name", "Summarize",
                "description", "Summarization skill", "tags", List.of("summarize", "nlp"))),
            "defaultInputModes", List.of("text"),
            "defaultOutputModes", List.of("text"),
            "protocolVersions", List.of("1.0")
        )
    );

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < AGENTS.size(); i++) {
            int port = BASE_PORT + i;
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            server.createContext("/", exchange -> {
                if (!"POST".equals(exchange.getRequestMethod())) {
                    exchange.sendResponseHeaders(405, -1);
                    return;
                }
                var body = MAPPER.readTree(exchange.getRequestBody());
                var response = MAPPER.createObjectNode();
                response.put("jsonrpc", "2.0");
                response.set("id", body.get("id"));
                response.putObject("result").set("echo", body);

                byte[] out = MAPPER.writeValueAsBytes(response);
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, out.length);
                try (OutputStream os = exchange.getResponseBody()) { os.write(out); }
            });
            server.start();
            System.out.println("Agent '" + AGENTS.get(i).get("agent_id") + "' listening on port " + port);
        }

        var client = HttpClient.newHttpClient();
        for (var card : AGENTS) {
            var req = HttpRequest.newBuilder()
                .uri(URI.create(KUBEMQ_URL + "/agents/register"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(card)))
                .build();
            var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
            System.out.println("Registered '" + card.get("agent_id") + "': " + resp.statusCode());
        }

        Thread.currentThread().join();
    }
}
