import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "concurrency-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

let activeRequests = 0;

app.post("/", async (req, res) => {
  activeRequests++;
  const current = activeRequests;
  console.log(`Active requests: ${current}`);

  await new Promise((r) => setTimeout(r, 2000));

  activeRequests--;
  res.json({
    jsonrpc: "2.0",
    id: req.body.id,
    result: { status: "ok", delayed_ms: 2000, concurrent_at_arrival: current },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Concurrency limit agent on port ${AGENT_PORT} (2s delay per request)`);

  const card = {
    agent_id: AGENT_ID,
    name: "Concurrency Limit Agent",
    description: "2s delay to hold connections for concurrency testing",
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
