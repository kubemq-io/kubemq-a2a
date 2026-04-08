import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
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
    static final String AGENT_ID = "slow-stream-agent-01";
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
            var method = body.path("method").asText("");

            if ("message/stream".equals(method)) {
                exchange.getResponseHeaders().set("Content-Type", "text/event-stream");
                exchange.getResponseHeaders().set("Cache-Control", "no-cache");
                exchange.sendResponseHeaders(200, 0);
                try (OutputStream os = exchange.getResponseBody()) {
                    for (int i = 1; i <= 10; i++) {
                        var event = MAPPER.writeValueAsString(Map.of(
                            "type", "status_update",
                            "payload", Map.of("status", "working", "progress", i, "total", 10)));
                        try {
                            os.write(("event: task.status\ndata: " + event + "\n\n").getBytes());
                            os.flush();
                            System.out.println("Sent event " + i);
                        } catch (IOException e) {
                            System.out.println("Client disconnected after event " + (i - 1));
                            return;
                        }
                        Thread.sleep(2000);
                    }
                    var done = MAPPER.writeValueAsString(Map.of(
                        "type", "done", "payload", Map.of("final_result", "completed")));
                    os.write(("event: task.done\ndata: " + done + "\n\n").getBytes());
                    os.flush();
                }
                return;
            }

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
            "name", "Slow Stream Agent",
            "description", "Emits events slowly for disconnect testing",
            "version", "1.0.0",
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

        Thread.currentThread().join();
    }
}
