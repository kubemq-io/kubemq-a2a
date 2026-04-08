import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "oversize-agent-01";
const AGENT_PORT = 18080;
const RESPONSE_SIZE_BYTES = 20 * 1024 * 1024; // 20MB — exceeds 10MB limit

const app = express();
app.use(express.json());

app.post("/", (_req, res) => {
  console.log("Generating oversized response (~20MB)...");
  const payload = "X".repeat(RESPONSE_SIZE_BYTES);
  res.json({
    jsonrpc: "2.0",
    id: 1,
    result: { data: payload },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Oversize agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Oversize Agent",
    description: "Returns >10MB response to test size limits",
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
