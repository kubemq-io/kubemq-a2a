import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "slow-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", async (req, res) => {
  console.log("Received request, sleeping 5s...");
  await new Promise((r) => setTimeout(r, 5000));
  console.log("Sleep done, sending response");
  res.json({
    jsonrpc: "2.0",
    id: req.body.id,
    result: { status: "ok", delayed_ms: 5000 },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Slow agent listening on port ${AGENT_PORT} (5s delay)`);

  const card = {
    agent_id: AGENT_ID,
    name: "Slow Timeout Agent",
    description: "5s delay to trigger timeout errors",
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
