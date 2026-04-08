import express from "express";

const KUBEMQ_URL = "http://localhost:9090";
const AGENT_PORT = 18080;

const app = express();
app.use(express.json());

app.post("/", (req, res) => {
  res.json({ jsonrpc: "2.0", id: req.body.id, result: { echo: req.body } });
});

app.listen(AGENT_PORT, async () => {
  console.log(`Agent listening on port ${AGENT_PORT}`);

  for (const id of ["dereg-post-01", "dereg-delete-01"]) {
    const card = {
      agent_id: id,
      name: `Deregister Test (${id})`,
      description: "Agent to demonstrate deregistration",
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
  }

  console.log("\nAgents ready for deregistration. Run client.ts now.");
});
