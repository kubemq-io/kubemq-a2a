using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "slow-stream-agent-01";
const int MaxEvents = 2;

var payload = new JsonObject
{
    ["jsonrpc"] = "2.0",
    ["id"] = 1,
    ["method"] = "message/stream",
    ["params"] = new JsonObject
    {
        ["message"] = new JsonObject
        {
            ["parts"] = new JsonArray(new JsonObject { ["text"] = "I will disconnect early" })
        }
    }
};

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
var request = new HttpRequestMessage(HttpMethod.Post, $"{KubeMqUrl}/a2a/{AgentId}")
{
    Content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json")
};

Console.WriteLine($"Connecting to stream (will disconnect after {MaxEvents} events)...");
using var resp = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
using var stream = await resp.Content.ReadAsStreamAsync();
using var reader = new StreamReader(stream);

string? eventType = null;
int count = 0;

while (!reader.EndOfStream)
{
    var line = await reader.ReadLineAsync();
    if (line == null) break;

    if (line.StartsWith("event: "))
        eventType = line[7..];
    else if (line.StartsWith("data: ") && eventType != null)
    {
        count++;
        var data = JsonNode.Parse(line[6..])!;
        Console.WriteLine($"  Event {count}: [{eventType}] progress={data["payload"]?["progress"]}");

        if (count >= MaxEvents)
        {
            Console.WriteLine($"\nDisconnecting after {MaxEvents} events...");
            break;
        }
    }
    else if (line.Length == 0)
        eventType = null;
}

Console.WriteLine("Client disconnected.");
Console.WriteLine("KubeMQ will detect the disconnect and clean up the stream.");
