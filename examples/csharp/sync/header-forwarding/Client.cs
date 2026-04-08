using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "header-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/send",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Check my headers" })
        }
    }
};

using var client = new HttpClient();
var request = new HttpRequestMessage(HttpMethod.Post, $"{KubeMqUrl}/a2a/{AgentId}")
{
    Content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json")
};
request.Headers.Add("X-Custom-Header", "my-custom-value");

var resp = await client.SendAsync(request);
var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;
Console.WriteLine(JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));

var received = data["result"]?["received_headers"];
Console.WriteLine($"\nForwarded headers: {received?.ToJsonString()}");

var xCustom = received?["X-Custom-Header"]?.GetValue<string>();
if (xCustom != null)
    Console.WriteLine("X-Custom-Header was forwarded successfully!");
else
    Console.WriteLine("Warning: X-Custom-Header not found in forwarded headers");

var xCaller = received?["X-KubeMQ-Caller-ID"]?.GetValue<string>();
if (xCaller != null)
    Console.WriteLine($"X-KubeMQ-Caller-ID injected: {xCaller}");
