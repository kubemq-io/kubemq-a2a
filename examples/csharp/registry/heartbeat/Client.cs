using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "heartbeat-agent-01";

using var client = new HttpClient();

for (int i = 1; i <= 3; i++)
{
    var body = new JsonObject { ["agent_id"] = AgentId };
    var resp = await client.PostAsync(
        $"{KubeMqUrl}/agents/heartbeat",
        new StringContent(body.ToJsonString(), Encoding.UTF8, "application/json"));
    var data = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!;
    Console.WriteLine($"Heartbeat {i}: status={(int)resp.StatusCode} last_seen={data["last_seen"]}");
    if (i < 3)
        await Task.Delay(2000);
}

Console.WriteLine("\n=== Final agent state ===");
var finalResp = await client.GetAsync($"{KubeMqUrl}/agents/{AgentId}");
var finalData = JsonNode.Parse(await finalResp.Content.ReadAsStringAsync())!;
Console.WriteLine($"registered_at: {finalData["registered_at"]}");
Console.WriteLine($"last_seen:     {finalData["last_seen"]}");
Console.WriteLine("\nHeartbeat cycle completed!");
