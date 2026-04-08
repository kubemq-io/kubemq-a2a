import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Client {

    static final String KUBEMQ_URL = "http://localhost:9090";
    static final String AGENT_ID = "full-info-agent-01";
    static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();
        var req = HttpRequest.newBuilder()
            .uri(URI.create(KUBEMQ_URL + "/agents/" + AGENT_ID))
            .GET().build();
        var resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println("Status: " + resp.statusCode());

        var data = MAPPER.readTree(resp.body());
        System.out.println("\n--- Agent Card ---");
        System.out.println("  agent_id:           " + data.path("agent_id").asText());
        System.out.println("  name:               " + data.path("name").asText());
        System.out.println("  description:        " + data.path("description").asText());
        System.out.println("  version:            " + data.path("version").asText());
        System.out.println("  url:                " + data.path("url").asText());
        System.out.println("  defaultInputModes:  " + data.path("defaultInputModes"));
        System.out.println("  defaultOutputModes: " + data.path("defaultOutputModes"));
        System.out.println("  protocolVersions:   " + data.path("protocolVersions"));
        System.out.println("  registered_at:      " + data.path("registered_at").asText());
        System.out.println("  last_seen:          " + data.path("last_seen").asText());

        var skills = data.path("skills");
        System.out.println("\n--- Skills (" + skills.size() + ") ---");
        for (var skill : skills) {
            System.out.println("  [" + skill.get("id").asText() + "] "
                + skill.get("name").asText() + ": " + skill.get("description").asText());
            System.out.println("    tags: " + skill.get("tags"));
        }
    }
}
