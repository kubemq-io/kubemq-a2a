using System.Diagnostics;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "keepalive-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/stream",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Long-running task" })
        }
    }
};

var sw = Stopwatch.StartNew();

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(120) };
var request = new HttpRequestMessage(HttpMethod.Post, $"{KubeMqUrl}/a2a/{AgentId}")
{
    Content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json")
};

Console.WriteLine("Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...");
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
        var elapsed = sw.Elapsed.TotalSeconds;
        Console.WriteLine($"  [{elapsed,6:F1}s] [{eventType}] {line[6..]}");

        if (eventType is "task.done" or "task.error")
            break;
    }
    else if (line.Length == 0)
    {
        if (eventType == null)
        {
            var elapsed = sw.Elapsed.TotalSeconds;
            Console.WriteLine($"  [{elapsed,6:F1}s] [keepalive]");
        }
        eventType = null;
    }
}

Console.WriteLine($"\nStream completed in {sw.Elapsed.TotalSeconds:F1}s");
Console.WriteLine("Keepalive kept the connection alive during long pauses!");
