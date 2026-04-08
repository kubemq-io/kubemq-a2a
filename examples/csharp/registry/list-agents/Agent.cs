using System.Text.Json;
using System.Text.Json.Nodes;

public static class Agent
{
    private const string KubeMqUrl = "http://localhost:9090";
    private const int BasePort = 18080;

    private static readonly JsonObject[] AgentCards =
    [
        new()
        {
            ["agent_id"] = "echo-agent-01",
            ["name"] = "Echo Agent",
            ["description"] = "Echoes back messages",
            ["version"] = "1.0.0",
            ["url"] = $"http://localhost:{BasePort}/",
            ["skills"] = new JsonArray(new JsonObject
            {
                ["id"] = "echo", ["name"] = "Echo",
                ["description"] = "Echo skill",
                ["tags"] = new JsonArray("echo", "test")
            }),
            ["defaultInputModes"] = new JsonArray("text"),
            ["defaultOutputModes"] = new JsonArray("text"),
            ["protocolVersions"] = new JsonArray("1.0")
        },
        new()
        {
            ["agent_id"] = "translate-agent-01",
            ["name"] = "Translate Agent",
            ["description"] = "Translates text",
            ["version"] = "1.0.0",
            ["url"] = $"http://localhost:{BasePort + 1}/",
            ["skills"] = new JsonArray(new JsonObject
            {
                ["id"] = "translate", ["name"] = "Translate",
                ["description"] = "Translation skill",
                ["tags"] = new JsonArray("translate", "nlp")
            }),
            ["defaultInputModes"] = new JsonArray("text"),
            ["defaultOutputModes"] = new JsonArray("text"),
            ["protocolVersions"] = new JsonArray("1.0")
        },
        new()
        {
            ["agent_id"] = "summarize-agent-01",
            ["name"] = "Summarize Agent",
            ["description"] = "Summarizes text",
            ["version"] = "1.0.0",
            ["url"] = $"http://localhost:{BasePort + 2}/",
            ["skills"] = new JsonArray(new JsonObject
            {
                ["id"] = "summarize", ["name"] = "Summarize",
                ["description"] = "Summarization skill",
                ["tags"] = new JsonArray("summarize", "nlp")
            }),
            ["defaultInputModes"] = new JsonArray("text"),
            ["defaultOutputModes"] = new JsonArray("text"),
            ["protocolVersions"] = new JsonArray("1.0")
        }
    ];

    public static async Task RunAsync()
    {
        var apps = new List<WebApplication>();

        for (int i = 0; i < AgentCards.Length; i++)
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

            var port = BasePort + i;
            app.Urls.Add($"http://0.0.0.0:{port}");
            await app.StartAsync();
            Console.WriteLine($"Agent '{AgentCards[i]["agent_id"]}' listening on port {port}");
            apps.Add(app);
        }

        using var httpClient = new HttpClient();
        foreach (var card in AgentCards)
        {
            var resp = await httpClient.PostAsync(
                $"{KubeMqUrl}/agents/register",
                new StringContent(card.ToJsonString(), System.Text.Encoding.UTF8, "application/json"));
            Console.WriteLine($"Registered '{card["agent_id"]}': {(int)resp.StatusCode}");
        }

        await Task.WhenAll(apps.Select(a => a.WaitForShutdownAsync()));
    }
}
