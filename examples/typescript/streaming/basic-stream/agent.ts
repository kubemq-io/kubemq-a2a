import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "stream-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", async (req, res) => {
  if (req.body.method === "message/stream") {
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.flushHeaders();

    for (let i = 1; i <= 5; i++) {
      const event = {
        type: "status_update",
        payload: { status: "working", progress: i, total: 5 },
      };
      res.write(`event: task.status\ndata: ${JSON.stringify(event)}\n\n`);
      await new Promise((r) => setTimeout(r, 500));
    }

    const done = { type: "done", payload: { final_result: "completed", event_count: 5 } };
    res.write(`event: task.done\ndata: ${JSON.stringify(done)}\n\n`);
    res.end();
  } else {
    res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
  }
});

app.get("/stream", async (_req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();

  for (let i = 1; i <= 5; i++) {
    const event = {
      type: "status_update",
      payload: { status: "working", progress: i, total: 5 },
    };
    res.write(`event: task.status\ndata: ${JSON.stringify(event)}\n\n`);
    await new Promise((r) => setTimeout(r, 500));
  }

  const done = { type: "done", payload: { final_result: "completed", event_count: 5 } };
  res.write(`event: task.done\ndata: ${JSON.stringify(done)}\n\n`);
  res.end();
});

app.listen(AGENT_PORT, async () => {
  console.log(`Stream agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Stream Agent",
    description: "Emits 5 status events then a done event",
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
