using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "concurrency-agent-01";
const int NumRequests = 101;

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
    return JsonNode.Parse(await resp.Content.ReadAsStringAsync());
}

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
Console.WriteLine($"Sending {NumRequests} concurrent requests (limit is 100)...");

var tasks = Enumerable.Range(1, NumRequests)
    .Select(i => SendRequest(client, i))
    .ToArray();

JsonNode?[] results;
try
{
    results = await Task.WhenAll(tasks);
}
catch
{
    results = tasks.Select(t => t.IsCompletedSuccessfully ? t.Result : null).ToArray();
}

int successes = 0, concurrencyErrors = 0, otherErrors = 0, exceptions = 0;

foreach (var r in results)
{
    if (r == null)
        exceptions++;
    else if (r["result"] != null)
        successes++;
    else if (r["error"]?["code"]?.GetValue<int>() == -32603)
        concurrencyErrors++;
    else
        otherErrors++;
}

Console.WriteLine($"\nResults:");
Console.WriteLine($"  Successes:            {successes}");
Console.WriteLine($"  Concurrency errors:   {concurrencyErrors} (code -32603)");
Console.WriteLine($"  Other errors:         {otherErrors}");
Console.WriteLine($"  Exceptions:           {exceptions}");
Console.WriteLine($"  Total:                {results.Length}");

if (concurrencyErrors >= 1)
    Console.WriteLine($"\nConcurrency limit enforced — {concurrencyErrors} request(s) rejected!");
