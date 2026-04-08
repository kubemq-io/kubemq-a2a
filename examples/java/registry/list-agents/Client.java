import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();

        System.out.println("=== All Agents ===");
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents"))
            .GET().build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var agents = MAPPER.readTree(resp.body());
        for (var agent : agents) {
            var skills = agent.get("skills");
            var ids = new java.util.ArrayList<String>();
            if (skills != null) for (var s : skills) ids.add(s.get("id").asText());
            System.out.println("  " + agent.get("agent_id").asText() + ": skills=" + ids);
        }
        System.out.println("\nTotal agents: " + agents.size());

        System.out.println("\n=== Filter by skill_tags=echo ===");
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents?skill_tags=echo"))
            .GET().build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        var filtered = MAPPER.readTree(resp.body());
        for (var agent : filtered) {
            System.out.println("  " + agent.get("agent_id").asText());
        }
        System.out.println("\nFiltered count: " + filtered.size());

        System.out.println("\n=== Filter by skill_tags=nlp ===");
        req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents?skill_tags=nlp"))
            .GET().build();
        resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        filtered = MAPPER.readTree(resp.body());
        for (var agent : filtered) {
            System.out.println("  " + agent.get("agent_id").asText());
        }
        System.out.println("\nFiltered count: " + filtered.size());
    }
}
