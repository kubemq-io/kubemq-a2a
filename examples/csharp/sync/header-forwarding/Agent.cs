using System.Text.Json;
using System.Text.Json.Nodes;

public static class Agent
{
    private const string KubeMqUrl = "http://localhost:9090";
    private const string AgentId = "header-agent-01";
    private const int AgentPort = 18080;

    public static async Task RunAsync()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Logging.ClearProviders();
        var app = builder.Build();

        app.MapPost("/", async (HttpContext context) =>
        {
            var body = (await JsonSerializer.DeserializeAsync<JsonNode>(context.Request.Body))!;
            var headers = new JsonObject();
            foreach (var h in context.Request.Headers)
            {
                if (h.Key.StartsWith("X-", StringComparison.OrdinalIgnoreCase) ||
                    h.Key.StartsWith("x-", StringComparison.OrdinalIgnoreCase))
                {
                    headers[h.Key] = h.Value.ToString();
                }
            }
            Console.WriteLine($"Received headers: {headers.ToJsonString()}");

            var response = new JsonObject
            {
                ["jsonrpc"] = "2.0",
                ["id"] = body["id"]?.DeepClone(),
                ["result"] = new JsonObject
                {
                    ["echo"] = body.DeepClone(),
                    ["received_headers"] = headers
                }
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
            ["name"] = "Header Agent",
            ["description"] = "Logs and returns received headers",
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
