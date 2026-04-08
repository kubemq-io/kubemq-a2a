using System.Text.Json;
using System.Text.Json.Nodes;

public static class Agent
{
    private const string KubeMqUrl = "http://localhost:9090";
    private const string AgentId = "full-info-agent-01";
    private const int AgentPort = 18080;

    public static async Task RunAsync()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Logging.ClearProviders();
        var app = builder.Build();

        app.MapPost("/", async (HttpContext context) =>
        {
            var body = (await JsonSerializer.DeserializeAsync<JsonNode>(context.Request.Body))!;
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
            ["name"] = "Full Info Agent",
            ["description"] = "An agent with all card fields populated for demonstration",
            ["version"] = "2.1.0",
            ["url"] = $"http://localhost:{AgentPort}/",
            ["skills"] = new JsonArray(
                new JsonObject
                {
                    ["id"] = "echo", ["name"] = "Echo",
                    ["description"] = "Echoes back the received message verbatim",
                    ["tags"] = new JsonArray("echo", "test", "debug")
                },
                new JsonObject
                {
                    ["id"] = "greet", ["name"] = "Greeting",
                    ["description"] = "Responds with a personalized greeting",
                    ["tags"] = new JsonArray("greet", "chat")
                }
            ),
            ["defaultInputModes"] = new JsonArray("text"),
            ["defaultOutputModes"] = new JsonArray("text"),
            ["protocolVersions"] = new JsonArray("1.0")
        };

        using var client = new HttpClient();
        var resp = await client.PostAsync(
            $"{KubeMqUrl}/agents/register",
            new StringContent(card.ToJsonString(), System.Text.Encoding.UTF8, "application/json"));
        Console.WriteLine($"Registered: {(int)resp.StatusCode}");
        var body = await resp.Content.ReadAsStringAsync();
        Console.WriteLine(JsonSerializer.Serialize(JsonNode.Parse(body), new JsonSerializerOptions { WriteIndented = true }));
    }
}
