import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "info-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", (req, res) => {
  res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Info Agent",
    description: "Agent with full card details for inspection",
    version: "2.1.0",
    url: `http://localhost:${AGENT_PORT}/`,
    skills: [
      {
        id: "echo",
        name: "Echo",
        description: "Echoes back the received message",
        tags: ["test", "echo"],
      },
      {
        id: "transform",
        name: "Transform",
        description: "Transforms message format",
        tags: ["test", "transform"],
      },
    ],
    defaultInputModes: ["text", "data"],
    defaultOutputModes: ["text"],
    protocolVersions: ["1.0"],
  };

  const resp = await fetch(`${KUBEMQ_URL}/agents/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(card),
  });
  const data = await resp.json();
  console.log("Registered:", data.agent_id);
});
