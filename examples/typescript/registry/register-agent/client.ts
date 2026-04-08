const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "echo-agent-01";

async function main() {
  const resp = await fetch(`${KUBEMQ_URL}/agents/${AGENT_ID}`);
  const data = await resp.json();
  console.log("Agent info:", JSON.stringify(data, null, 2));

  console.log("\nVerification:");
  console.log(`  agent_id:      ${data.agent_id}`);
  console.log(`  name:          ${data.name}`);
  console.log(`  registered_at: ${data.registered_at}`);
  console.log(`  last_seen:     ${data.last_seen}`);
}

main().catch(console.error);
