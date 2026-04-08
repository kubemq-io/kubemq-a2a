import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "keepalive-agent-01";
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

    // 35s pause — KubeMQ sends keepalive comments during this gap
    await new Promise((r) => setTimeout(r, 35_000));

    const status2 = { type: "status_update", payload: { status: "working", progress: 2, total: 3 } };
    res.write(`event: task.status\ndata: ${JSON.stringify(status2)}\n\n`);

    await new Promise((r) => setTimeout(r, 35_000));

    const status3 = { type: "status_update", payload: { status: "working", progress: 3, total: 3 } };
    res.write(`event: task.status\ndata: ${JSON.stringify(status3)}\n\n`);

    const done = { type: "done", payload: { final_result: "completed" } };
    res.write(`event: task.done\ndata: ${JSON.stringify(done)}\n\n`);
    res.end();
  } else {
    res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
  }
});

app.listen(AGENT_PORT, async () => {
  console.log(`Keepalive agent listening on port ${AGENT_PORT}`);
  console.log("(35s pauses between events to trigger keepalive comments)");

  const card = {
    agent_id: AGENT_ID,
    name: "Keepalive Agent",
    description: "Emits events with 35s pauses to demonstrate keepalive",
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
