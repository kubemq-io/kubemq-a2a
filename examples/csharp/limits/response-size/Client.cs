using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "oversize-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/send",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Give me a large response" })
        }
    }
};

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
Console.WriteLine("Requesting oversized response (>10MB)...");

var resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json"));

var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;

if (data["error"] != null)
{
    var error = data["error"]!;
    Console.WriteLine($"\nError code:    {error["code"]}");
    Console.WriteLine($"Error message: {error["message"]}");
    Console.WriteLine("\nResponse size limit enforced!");
}
else
{
    Console.WriteLine($"\nStatus: {(int)resp.StatusCode}");
    Console.WriteLine("Note: Response was accepted (check KubeMQ size limit configuration)");
}
