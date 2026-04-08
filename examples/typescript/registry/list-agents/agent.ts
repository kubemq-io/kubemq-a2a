import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const BASE_PORT = 18080;

const agents = [
  {
    agent_id: "list-echo-01",
    name: "Echo Agent 1",
    description: "First echo agent",
    version: "1.0.0",
    port: BASE_PORT,
    skills: [
      { id: "echo", name: "Echo", description: "Echoes messages", tags: ["test", "echo"] },
    ],
  },
  {
    agent_id: "list-translate-01",
    name: "Translate Agent",
    description: "Translation agent",
    version: "1.0.0",
    port: BASE_PORT + 1,
    skills: [
      { id: "translate", name: "Translate", description: "Translates text", tags: ["nlp", "translate"] },
    ],
  },
  {
    agent_id: "list-summarize-01",
    name: "Summarize Agent",
    description: "Summarization agent",
    version: "1.0.0",
    port: BASE_PORT + 2,
    skills: [
      { id: "summarize", name: "Summarize", description: "Summarizes text", tags: ["nlp", "summarize"] },
    ],
  },
];

for (const agent of agents) {
  const app = express();
  app.use(express.json());
  app.post("/", (req, res) => {
    res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
  });

  app.listen(agent.port, async () => {
    console.log(`${agent.name} listening on port ${agent.port}`);

    const card = {
      agent_id: agent.agent_id,
      name: agent.name,
      description: agent.description,
      version: agent.version,
      url: `http://localhost:${agent.port}/`,
      skills: agent.skills,
      defaultInputModes: ["text"],
      defaultOutputModes: ["text"],
      protocolVersions: ["1.0"],
    };

    const resp = await fetch(`${KUBEMQ_URL}/agents/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(card),
    });
    const data = await resp.json();
    console.log(`Registered ${agent.agent_id}:`, data.agent_id);
  });
}
