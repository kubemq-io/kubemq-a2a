const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "context-agent-01";

async function main() {
  const contextId = "ctx-ts-001";

  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: { parts: [{ text: "Correlated request" }] },
      contextId: contextId,
    },
  };

  console.log(`Sending with contextId=${contextId}`);

  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const data = await resp.json();
  const echoedCtx = data.result?.contextId || data.result?.echo?.params?.contextId;
  console.log(`Echoed contextId: ${echoedCtx}`);
  console.log(`Match: ${echoedCtx === contextId}`);
  console.log("\nFull response:", JSON.stringify(data, null, 2));
}

main().catch(console.error);
