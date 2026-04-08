import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "echo-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", (req, res) => {
  const body = req.body;
  console.log("Received request:", JSON.stringify(body));
  res.json({
    jsonrpc: "2.0",
    id: body.id,
    result: { echo: body },
  });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Echo Agent",
    description: "A simple echo agent for testing",
    version: "1.0.0",
    url: `http://localhost:${AGENT_PORT}/`,
    skills: [
      {
        id: "echo",
        name: "Echo",
        description: "Echoes back the received message",
        tags: ["test", "echo"],
      },
    ],
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
  console.log("Registered:", JSON.stringify(data, null, 2));
});
