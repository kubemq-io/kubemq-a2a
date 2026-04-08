import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "disconnect-agent-01";
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

    for (let i = 1; i <= 10; i++) {
      if (res.writableEnded) {
        console.log(`Client disconnected at event ${i}`);
        return;
      }
      const event = {
        type: "status_update",
        payload: { status: "working", progress: i, total: 10 },
      };
      res.write(`event: task.status\ndata: ${JSON.stringify(event)}\n\n`);
      console.log(`Sent event ${i}/10`);
      await new Promise((r) => setTimeout(r, 1000));
    }

    const done = { type: "done", payload: { final_result: "completed" } };
    res.write(`event: task.done\ndata: ${JSON.stringify(done)}\n\n`);
    res.end();
  } else {
    res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
  }
});

app.listen(AGENT_PORT, async () => {
  console.log(`Disconnect agent listening on port ${AGENT_PORT}`);
  console.log("(emits 10 events slowly — client disconnects after 2)");

  const card = {
    agent_id: AGENT_ID,
    name: "Disconnect Agent",
    description: "Emits events slowly for client disconnect testing",
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
