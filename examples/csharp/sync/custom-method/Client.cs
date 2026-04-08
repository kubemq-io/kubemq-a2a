using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "custom-method-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "custom/action",
    ["params"] = new JsonObject { ["data"] = "custom-payload" }
};

using var client = new HttpClient();
var resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json"));

var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;
Console.WriteLine(JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));

var handledMethod = data["result"]?["handled_method"]?.GetValue<string>();
Console.WriteLine($"\nHandled method: {handledMethod}");

if (handledMethod == "custom/action")
    Console.WriteLine("Custom method forwarded successfully!");
