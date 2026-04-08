import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "concurrent-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

let requestCount = 0;

app.post("/", (req, res) => {
  requestCount++;
  const num = requestCount;
  console.log(`Request #${num} received`);
  res.json({
    jsonrpc: "2.0",
    id: req.body.id,
    result: { echo: req.body, request_number: num },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Concurrent agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Concurrent Agent",
    description: "Handles concurrent requests",
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
