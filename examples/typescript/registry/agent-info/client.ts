const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "info-agent-01";

async function main() {
  const resp = await fetch(`${KUBEMQ_URL}/agents/${AGENT_ID}`);
  const agent = await resp.json();

  console.log("=== Agent Card Details ===");
  console.log(`  agent_id:          ${agent.agent_id}`);
  console.log(`  name:              ${agent.name}`);
  console.log(`  description:       ${agent.description}`);
  console.log(`  version:           ${agent.version}`);
  console.log(`  url:               ${agent.url}`);
  console.log(`  registered_at:     ${agent.registered_at}`);
  console.log(`  last_seen:         ${agent.last_seen}`);
  console.log(`  protocolVersions:  ${JSON.stringify(agent.protocolVersions)}`);
  console.log(`  defaultInputModes: ${JSON.stringify(agent.defaultInputModes)}`);
  console.log(`  defaultOutputModes:${JSON.stringify(agent.defaultOutputModes)}`);

  console.log("\n=== Skills ===");
  for (const skill of agent.skills || []) {
    console.log(`  - ${skill.id}: ${skill.name} (tags: ${(skill.tags || []).join(", ")})`);
    console.log(`    ${skill.description}`);
  }

  console.log("\n=== Full JSON ===");
  console.log(JSON.stringify(agent, null, 2));
}

main().catch(console.error);
