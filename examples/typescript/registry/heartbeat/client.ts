const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "heartbeat-agent-01";

async function main() {
  const before = await fetch(`${KUBEMQ_URL}/agents/${AGENT_ID}`);
  const beforeData = await before.json();
  console.log(`Initial last_seen: ${beforeData.last_seen}`);

  for (let i = 1; i <= 3; i++) {
    await new Promise((r) => setTimeout(r, 1500));

    const resp = await fetch(`${KUBEMQ_URL}/agents/heartbeat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ agent_id: AGENT_ID }),
    });
    const data = await resp.json();
    console.log(`Heartbeat #${i}: status=${resp.status}, last_seen=${data.last_seen}`);
  }

  console.log("\n=== Heartbeat non-existent agent ===");
  const bad = await fetch(`${KUBEMQ_URL}/agents/heartbeat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_id: "nonexistent-agent" }),
  });
  const badData = await bad.json();
  console.log(`Status: ${bad.status} (expect 400)`);
  console.log(`Error: ${badData.error}`);
}

main().catch(console.error);
