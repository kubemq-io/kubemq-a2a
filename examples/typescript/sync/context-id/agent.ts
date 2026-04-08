import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "context-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", (req, res) => {
  const body = req.body;
  const contextId = body.params?.contextId;
  console.log(`Received request with contextId=${contextId}`);

  res.json({
    jsonrpc: "2.0",
    id: body.id,
    result: {
      echo: body,
      contextId: contextId,
    },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Context agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Context Agent",
    description: "Echoes contextId for correlation testing",
    version: "1.0.0",
    url: `http://localhost:${AGENT_PORT}/`,
    skills: [],
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
  console.log(`Registered: ${data.agent_id}`);
});
