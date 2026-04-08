using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "slow-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/send",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "This will timeout" })
        },
        ["configuration"] = new JsonObject { ["timeout"] = 1 }
    }
};

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
Console.WriteLine("Sending request with timeout=1 to slow agent (5s delay)...");

var resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json"));

var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;
Console.WriteLine(JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));

var error = data["error"];
Console.WriteLine($"\nError code:    {error?["code"]}");
Console.WriteLine($"Error message: {error?["message"]}");

var code = error?["code"]?.GetValue<int>();
if (code == -32001)
    Console.WriteLine("\nTimeout error (-32001) received as expected!");
