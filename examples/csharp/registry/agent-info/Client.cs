using System.Text.Json;
using System.Text.Json.Nodes;

if (args.Length > 0 && args[0] == "agent")
{
    await Agent.RunAsync();
    return;
}

const string KubeMqUrl = "http://localhost:9090";
const string AgentId = "full-info-agent-01";

using var client = new HttpClient();
var resp = await client.GetAsync($"{KubeMqUrl}/agents/{AgentId}");
Console.WriteLine($"Status: {(int)resp.StatusCode}");

var body = await resp.Content.ReadAsStringAsync();
var data = JsonNode.Parse(body)!;

Console.WriteLine("\n--- Agent Card ---");
Console.WriteLine($"  agent_id:           {data["agent_id"]}");
Console.WriteLine($"  name:               {data["name"]}");
Console.WriteLine($"  description:        {data["description"]}");
Console.WriteLine($"  version:            {data["version"]}");
Console.WriteLine($"  url:                {data["url"]}");
Console.WriteLine($"  defaultInputModes:  {data["defaultInputModes"]}");
Console.WriteLine($"  defaultOutputModes: {data["defaultOutputModes"]}");
Console.WriteLine($"  protocolVersions:   {data["protocolVersions"]}");
Console.WriteLine($"  registered_at:      {data["registered_at"]}");
Console.WriteLine($"  last_seen:          {data["last_seen"]}");

var skills = data["skills"]?.AsArray() ?? [];
Console.WriteLine($"\n--- Skills ({skills.Count}) ---");
foreach (var skill in skills)
{
    Console.WriteLine($"  [{skill!["id"]}] {skill["name"]}: {skill["description"]}");
    Console.WriteLine($"    tags: {skill["tags"]}");
}
