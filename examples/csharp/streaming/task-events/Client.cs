using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "task-events-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/stream",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Show me all event types" })
        }
    }
};

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(60) };
var request = new HttpRequestMessage(HttpMethod.Post, $"{KubeMqUrl}/a2a/{AgentId}")
{
    Content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json")
};

var eventTypes = new Dictionary<string, int>();

Console.WriteLine("Connecting to SSE stream...");
using var resp = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
using var stream = await resp.Content.ReadAsStreamAsync();
using var reader = new StreamReader(stream);

string? eventType = null;

while (!reader.EndOfStream)
{
    var line = await reader.ReadLineAsync();
    if (line == null) break;

    if (line.StartsWith("event: "))
        eventType = line[7..];
    else if (line.StartsWith("data: ") && eventType != null)
    {
        eventTypes[eventType] = eventTypes.GetValueOrDefault(eventType) + 1;
        var data = JsonNode.Parse(line[6..])!;

        if (eventType == "task.status")
        {
            var p = data["payload"]!;
            Console.WriteLine($"  [STATUS]   progress={p["progress"]}/{p["total"]}");
        }
        else if (eventType == "task.artifact")
            Console.WriteLine($"  [ARTIFACT] name={data["payload"]!["name"]}");
        else if (eventType == "task.done")
            Console.WriteLine($"  [DONE]     result={data["payload"]!["final_result"]}");
        else if (eventType == "task.error")
            Console.WriteLine($"  [ERROR]    {data["payload"]}");

        if (eventType is "task.done" or "task.error")
            break;
    }
    else if (line.Length == 0)
        eventType = null;
}

Console.WriteLine($"\n--- Event Summary ---");
foreach (var (et, count) in eventTypes.OrderBy(kv => kv.Key))
    Console.WriteLine($"  {et}: {count}");
Console.WriteLine($"  Total: {eventTypes.Values.Sum()}");
