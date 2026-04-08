using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";

using var client = new HttpClient();

Console.WriteLine("=== All Agents ===");
var resp = await client.GetAsync($"{KubeMqUrl}/agents");
var agents = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!.AsArray();
foreach (var agent in agents)
{
    var skills = agent!["skills"]?.AsArray().Select(s => s!["id"]!.GetValue<string>()).ToList() ?? [];
    Console.WriteLine($"  {agent["agent_id"]}: skills=[{string.Join(", ", skills)}]");
}
Console.WriteLine($"\nTotal agents: {agents.Count}");

Console.WriteLine("\n=== Filter by skill_tags=echo ===");
resp = await client.GetAsync($"{KubeMqUrl}/agents?skill_tags=echo");
var filtered = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!.AsArray();
foreach (var agent in filtered)
    Console.WriteLine($"  {agent!["agent_id"]}");
Console.WriteLine($"\nFiltered count: {filtered.Count}");

Console.WriteLine("\n=== Filter by skill_tags=nlp ===");
resp = await client.GetAsync($"{KubeMqUrl}/agents?skill_tags=nlp");
filtered = JsonNode.Parse(await resp.Content.ReadAsStringAsync())!.AsArray();
foreach (var agent in filtered)
    Console.WriteLine($"  {agent!["agent_id"]}");
Console.WriteLine($"\nFiltered count: {filtered.Count}");
