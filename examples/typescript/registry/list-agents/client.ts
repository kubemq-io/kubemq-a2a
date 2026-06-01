const KUBEMQ_URL = "http://localhost:9090";

async function main() {
  console.log("=== List all agents ===");
  const allResp = await fetch(`${KUBEMQ_URL}/agents`);
  const allData = await allResp.json();
  const allAgents = Array.isArray(allData) ? allData : (allData.agents || []);
  console.log(`Found ${allAgents.length} agent(s):`);
  for (const agent of allAgents) {
    const skillIds = (agent.skills || []).map((s: { id?: string }) => s.id).filter(Boolean);
    console.log(`  - ${agent.agent_id} (skills: ${skillIds.join(", ") || "none"})`);
  }

  console.log("\n=== Filter by skill_tags=echo ===");
  const echoResp = await fetch(`${KUBEMQ_URL}/agents?skill_tags=echo`);
  const echoData = await echoResp.json();
  const echoAgents = Array.isArray(echoData) ? echoData : (echoData.agents || []);
  console.log(`Found ${echoAgents.length} agent(s) with 'echo' tag:`);
  for (const agent of echoAgents) {
    console.log(`  - ${agent.agent_id}`);
  }

  console.log("\n=== Filter by skill_tags=nlp ===");
  const nlpResp = await fetch(`${KUBEMQ_URL}/agents?skill_tags=nlp`);
  const nlpData = await nlpResp.json();
  const nlpAgents = Array.isArray(nlpData) ? nlpData : (nlpData.agents || []);
  console.log(`Found ${nlpAgents.length} agent(s) with 'nlp' tag:`);
  for (const agent of nlpAgents) {
    console.log(`  - ${agent.agent_id}`);
  }
}

main().catch(console.error);
