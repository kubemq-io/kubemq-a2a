import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "task-events-agent-01";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", async (req, res) => {
  const accept = req.headers.accept || "";

  if (accept.includes("text/event-stream") || req.body.method === "message/stream") {
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.flushHeaders();

    const status1 = { type: "status_update", payload: { status: "working", progress: 1, total: 3 } };
    res.write(`event: task.status\ndata: ${JSON.stringify(status1)}\n\n`);
    await new Promise((r) => setTimeout(r, 200));

    const status2 = { type: "status_update", payload: { status: "working", progress: 2, total: 3 } };
    res.write(`event: task.status\ndata: ${JSON.stringify(status2)}\n\n`);
    await new Promise((r) => setTimeout(r, 200));

    const artifact = {
      type: "artifact",
      payload: { name: "result.json", data: { key: "value", items: [1, 2, 3] } },
    };
    res.write(`event: task.artifact\ndata: ${JSON.stringify(artifact)}\n\n`);
    await new Promise((r) => setTimeout(r, 200));

    const status3 = { type: "status_update", payload: { status: "finishing", progress: 3, total: 3 } };
    res.write(`event: task.status\ndata: ${JSON.stringify(status3)}\n\n`);
    await new Promise((r) => setTimeout(r, 200));

    const done = { type: "done", payload: { final_result: "completed", event_count: 4 } };
    res.write(`event: task.done\ndata: ${JSON.stringify(done)}\n\n`);
    res.end();
  } else {
    res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
  }
});

app.listen(AGENT_PORT, async () => {
  console.log(`Task events agent listening on port ${AGENT_PORT}`);

  const card = {
    agent_id: AGENT_ID,
    name: "Task Events Agent",
    description: "Emits status, artifact, and done events",
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
