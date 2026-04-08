using System.Text;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "deregister-agent-01";

using var client = new HttpClient();

Console.WriteLine("=== Verify agent exists ===");
var resp = await client.GetAsync($"{KubeMqUrl}/agents/{AgentId}");
Console.WriteLine($"GET /agents/{AgentId}: {(int)resp.StatusCode}");

Console.WriteLine("\n=== Deregister via POST ===");
var body = new JsonObject { ["agent_id"] = AgentId };
resp = await client.PostAsync(
    $"{KubeMqUrl}/agents/deregister",
    new StringContent(body.ToJsonString(), Encoding.UTF8, "application/json"));
Console.WriteLine($"POST /agents/deregister: {(int)resp.StatusCode}");

resp = await client.GetAsync($"{KubeMqUrl}/agents/{AgentId}");
Console.WriteLine($"GET /agents/{AgentId} after deregister: {(int)resp.StatusCode}");

Console.WriteLine("\n=== Re-register for DELETE test ===");
var card = new JsonObject
{
    ["agent_id"] = AgentId,
    ["name"] = "Deregister Test Agent",
    ["url"] = "http://localhost:18080/",
    ["skills"] = new JsonArray(),
    ["defaultInputModes"] = new JsonArray("text"),
    ["defaultOutputModes"] = new JsonArray("text"),
    ["protocolVersions"] = new JsonArray("1.0")
};
resp = await client.PostAsync(
    $"{KubeMqUrl}/agents/register",
    new StringContent(card.ToJsonString(), Encoding.UTF8, "application/json"));
Console.WriteLine($"Re-registered: {(int)resp.StatusCode}");

Console.WriteLine("\n=== Deregister via DELETE ===");
resp = await client.DeleteAsync($"{KubeMqUrl}/agents/{AgentId}");
Console.WriteLine($"DELETE /agents/{AgentId}: {(int)resp.StatusCode}");

resp = await client.GetAsync($"{KubeMqUrl}/agents/{AgentId}");
Console.WriteLine($"GET /agents/{AgentId} after delete: {(int)resp.StatusCode}");

Console.WriteLine("\nBoth deregistration methods demonstrated successfully!");
