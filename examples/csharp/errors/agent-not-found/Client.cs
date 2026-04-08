using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "nonexistent-agent";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/send",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Hello?" })
        }
    }
};

using var client = new HttpClient();
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
if (code == -32002)
    Console.WriteLine("\nAgent-not-found error (-32002) received as expected!");
