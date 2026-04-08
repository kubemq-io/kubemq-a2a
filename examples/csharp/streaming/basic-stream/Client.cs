using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "stream-agent-01";

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/stream",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "Stream me some updates" })
        }
    }
};

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(60) };
var request = new HttpRequestMessage(HttpMethod.Post, $"{KubeMqUrl}/a2a/{AgentId}")
{
    Content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json")
};

Console.WriteLine("Connecting to SSE stream...");
using var resp = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
using var stream = await resp.Content.ReadAsStreamAsync();
using var reader = new StreamReader(stream);

string? eventType = null;
int eventCount = 0;

while (!reader.EndOfStream)
{
    var line = await reader.ReadLineAsync();
    if (line == null) break;

    if (line.StartsWith("event: "))
        eventType = line[7..];
    else if (line.StartsWith("data: ") && eventType != null)
    {
        eventCount++;
        var data = line[6..];
        Console.WriteLine($"[{eventType}] {data}");

        if (eventType is "task.done" or "task.error")
            break;
    }
    else if (line.Length == 0)
        eventType = null;
}

Console.WriteLine($"\nReceived {eventCount} events");
Console.WriteLine("Stream completed!");
