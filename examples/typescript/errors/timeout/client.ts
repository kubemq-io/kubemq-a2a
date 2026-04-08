const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "slow-agent-01";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: { parts: [{ text: "This will timeout" }] },
      configuration: { timeout: 1 },
    },
  };

  console.log("Sending with timeout=1s to a 5s-delay agent...");

  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const data = await resp.json();
  console.log("Response:", JSON.stringify(data, null, 2));

  if (data.error) {
    console.log(`\nError code:    ${data.error.code} (expect -32001)`);
    console.log(`Error message: ${data.error.message}`);
    console.log(`Match:         ${data.error.code === -32001}`);
  } else {
    console.log("\nUnexpected: got success response instead of timeout");
  }
}

main().catch(console.error);
