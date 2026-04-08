using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "echo-agent-01";

using var client = new HttpClient();

Console.WriteLine("=== Test 1: Invalid JSON ===");
var resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent("{invalid json!!!}", Encoding.UTF8, "application/json"));
var data = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!;
var error = data["error"];
Console.WriteLine($"  Code: {error?["code"]} (expected -32700)");
Console.WriteLine($"  Message: {error?["message"]}");

Console.WriteLine("\n=== Test 2: Missing method field ===");
var payload2 = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["params"] = new JsonObject()
};
resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent(payload2.ToJsonString(), Encoding.UTF8, "application/json"));
data = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!;
error = data["error"];
Console.WriteLine($"  Code: {error?["code"]} (expected -32600)");
Console.WriteLine($"  Message: {error?["message"]}");

Console.WriteLine("\n=== Test 3: Bad jsonrpc version ===");
var payload3 = new JsonObject
{
    ["jsonrpc"] = "1.0",
    ["id"] = 1,
    ["method"] = "message/send",
    ["params"] = new JsonObject()
};
resp = await client.PostAsync(
    $"{KubeMqUrl}/a2a/{AgentId}",
    new StringContent(payload3.ToJsonString(), Encoding.UTF8, "application/json"));
data = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!;
error = data["error"];
Console.WriteLine($"  Code: {error?["code"]} (expected -32600)");
Console.WriteLine($"  Message: {error?["message"]}");

Console.WriteLine("\nAll invalid request errors demonstrated!");
