import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "header-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", (req, res) => {
  const headers: Record<string, string> = {};
  for (const [key, val] of Object.entries(req.headers)) {
    if (typeof val === "string") headers[key] = val;
  }

  console.log("Received headers:", JSON.stringify(headers, null, 2));

  res.json({
    jsonrpc: "2.0",
    id: req.body.id,
    result: { received_headers: headers },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Header agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Header Agent",
    description: "Logs all received headers",
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
