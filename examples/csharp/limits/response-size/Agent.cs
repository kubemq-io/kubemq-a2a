using System.Text.Json;
using System.Text.Json.Nodes;

public static class Agent
{
    private const string KubeMqUrl = "http://localhost:9090";
    private const string AgentId = "oversize-agent-01";
    private const int AgentPort = 18080;
    private const int ResponseSizeBytes = 11 * 1024 * 1024; // 11MB

    public static async Task RunAsync()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Logging.ClearProviders();
        builder.WebHost.ConfigureKestrel(o => o.Limits.MaxRequestBodySize = 50 * 1024 * 1024);
        var app = builder.Build();

        app.MapPost("/", async (HttpContext context) =>
        {
            var body = (await JsonSerializer.DeserializeAsync<JsonNode>(context.Request.Body))!;
            var largePayload = new string('x', ResponseSizeBytes);
            var response = new JsonObject
            {
                ["jsonrpc"] = "2.0",
                ["id"] = body["id"]?.DeepClone(),
                ["result"] = new JsonObject { ["data"] = largePayload }
            };
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsync(response.ToJsonString());
        });

        app.Urls.Add($"http://0.0.0.0:{AgentPort}");
        await app.StartAsync();
        Console.WriteLine($"Agent listening on port {AgentPort} (response size={ResponseSizeBytes / 1024 / 1024}MB)");

        await RegisterAgentAsync();

        await app.WaitForShutdownAsync();
    }

    private static async Task RegisterAgentAsync()
    {
        var card = new JsonObject
        {
            ["agent_id"] = AgentId,
            ["name"] = "Oversize Agent",
            ["description"] = "Returns responses larger than 10MB",
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
