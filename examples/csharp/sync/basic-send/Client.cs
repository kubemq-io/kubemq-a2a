using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "echo-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/send",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Hello, agent!" })
        }
    }
};

using var client = new HttpClient();
var resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json"));

Console.WriteLine($"Status: {(int)resp.StatusCode}");
var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;
Console.WriteLine(JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));

if (data["result"] != null)
    Console.WriteLine("\nBasic send completed successfully!");
