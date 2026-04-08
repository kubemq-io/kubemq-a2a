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
    static final String AGENT_ID = "heartbeat-agent-01";
    static final int AGENT_PORT = 18080;
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(AGENT_PORT), 0);
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
        System.out.println("Agent listening on port " + AGENT_PORT);

        var card = Map.of(
            "agent_id", AGENT_ID,
            "name", "Heartbeat Test Agent",
            "url", "http://localhost:" + AGENT_PORT + "/",
            "skills", List.of(),
            "defaultInputModes", List.of("text"),
            "defaultOutputModes", List.of("text"),
            "protocolVersions", List.of("1.0")
        );

        var client = HttpClient.newHttpClient();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/register"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(card)))
            .build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("Registered: " + resp.statusCode());
        System.out.println("Agent registered. Run Client.java to test heartbeat.");

        Thread.currentThread().join();
    }
}
