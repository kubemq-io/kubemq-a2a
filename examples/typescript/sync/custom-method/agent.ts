import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "custom-method-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", (req, res) => {
  const body = req.body;
  const method = body.method;
  console.log(`Received method: ${method}`);

  if (method === "custom/action") {
    res.json({
      jsonrpc: "2.0",
      id: body.id,
      result: { echo: body },
    });
  } else if (method === "tasks/get") {
    res.json({
      jsonrpc: "2.0",
      id: body.id,
      result: { taskId: body.params?.taskId, status: "completed" },
    });
  } else if (method === "tasks/cancel") {
    res.json({
      jsonrpc: "2.0",
      id: body.id,
      result: { taskId: body.params?.taskId, status: "cancelled" },
    });
  } else {
    res.json({
      jsonrpc: "2.0",
      id: body.id,
      result: { echo: body },
    });
  }
});

app.listen(AGENT_PORT, async () => {
  console.log(`Custom method agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Custom Method Agent",
    description: "Handles custom/action and standard methods",
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
