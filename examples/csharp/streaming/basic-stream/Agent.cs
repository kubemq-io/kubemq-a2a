using System.Text.Json;
using System.Text.Json.Nodes;

public static class Agent
{
    private const string KubeMqUrl = "http://localhost:9090";
    private const string AgentId = "stream-agent-01";
    private const int AgentPort = 18080;

    public static async Task RunAsync()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Logging.ClearProviders();
        var app = builder.Build();

        app.MapPost("/", async (HttpContext context) =>
        {
            var body = (await JsonSerializer.DeserializeAsync<JsonNode>(context.Request.Body))!;
            var method = body["method"]?.GetValue<string>() ?? "";

            if (method == "message/stream")
            {
                context.Response.ContentType = "text/event-stream";
                context.Response.Headers.CacheControl = "no-cache";

                for (int i = 1; i <= 5; i++)
                {
                    var ev = JsonSerializer.Serialize(new { type = "status_update", payload = new { status = "working", progress = i, total = 5 } });
                    await context.Response.WriteAsync($"event: task.status\ndata: {ev}\n\n");
                    await context.Response.Body.FlushAsync();
                    await Task.Delay(500);
                }

                var done = JsonSerializer.Serialize(new { type = "done", payload = new { final_result = "completed", event_count = 5 } });
                await context.Response.WriteAsync($"event: task.done\ndata: {done}\n\n");
                await context.Response.Body.FlushAsync();
                return;
            }

            var response = new JsonObject
            {
                ["jsonrpc"] = "2.0",
                ["id"] = body["id"]?.DeepClone(),
                ["result"] = new JsonObject { ["echo"] = body.DeepClone() }
            };
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsync(response.ToJsonString());
        });

        app.Urls.Add($"http://0.0.0.0:{AgentPort}");
        await app.StartAsync();
        Console.WriteLine($"Agent listening on port {AgentPort}");

        await RegisterAgentAsync();

        await app.WaitForShutdownAsync();
    }

    private static async Task RegisterAgentAsync()
    {
        var card = new JsonObject
        {
            ["agent_id"] = AgentId,
            ["name"] = "Stream Agent",
            ["description"] = "Emits SSE events for streaming",
            ["version"] = "1.0.0",
            ["url"] = $"http://localhost:{AgentPort}/",
            ["skills"] = new JsonArray(),
            ["defaultInputModes"] = new JsonArray("text"),
            ["defaultOutputModes"] = new JsonArray("text"),
            ["protocolVersions"] = new JsonArray("1.0")
        };

        using var client = new HttpClient();
        var resp = await client.PostAsync(
            $"{KubeMqUrl}/agents/register",
            new StringContent(card.ToJsonString(), System.Text.Encoding.UTF8, "application/json"));
        Console.WriteLine($"Registered: {(int)resp.StatusCode}");
    }
}
