using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "concurrent-agent-01";
const int NumRequests = 20;

async Task<JsonNode?> SendRequest(HttpClient httpClient, int requestId)
{
    var payload = new JsonObject
    {
        ["jsonrpc"] = "2.0",
        ["id"] = requestId,
        ["method"] = "message/send",
        ["params"] = new JsonObject
        {
            ["message"] = new JsonObject
            {
                ["parts"] = new JsonArray(new JsonObject { ["text"] = $"Request #{requestId}" })
            }
        }
    };
    var resp = await httpClient.PostAsync(
        $"{KubeMqUrl}/a2a/{AgentId}",
        new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json"));
    var body = await resp.Content.ReadAsStringAsync();
    return JsonNode.Parse(body);
}

using var client = new HttpClient();
Console.WriteLine($"Sending {NumRequests} concurrent requests...");

var tasks = Enumerable.Range(1, NumRequests)
    .Select(i => SendRequest(client, i))
    .ToArray();

var results = await Task.WhenAll(tasks);

var successes = results.Count(r => r?["result"] != null);
var errors = results.Count(r => r?["error"] != null);
var exceptions = NumRequests - results.Length;

Console.WriteLine($"\nResults:");
Console.WriteLine($"  Successes:  {successes}");
Console.WriteLine($"  Errors:     {errors}");
Console.WriteLine($"  Exceptions: {exceptions}");
Console.WriteLine($"  Total:      {results.Length}");

if (successes == NumRequests)
    Console.WriteLine($"\nAll {NumRequests} concurrent requests completed successfully!");
