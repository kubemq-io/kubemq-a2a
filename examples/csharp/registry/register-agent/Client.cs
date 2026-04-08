using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "echo-agent-01";

using var client = new HttpClient();
var resp = await client.GetAsync($"{KubeMqUrl}/agents/{AgentId}");
Console.WriteLine($"Status: {(int)resp.StatusCode}");

var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;
Console.WriteLine(JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));

if (data["agent_id"]?.GetValue<string>() == AgentId && data["registered_at"] != null)
    Console.WriteLine("\nAgent registration verified successfully!");
