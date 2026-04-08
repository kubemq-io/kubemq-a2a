const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "echo-agent-01";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: {
        parts: [{ text: "Hello, agent!" }],
      },
    },
  };

  console.log("Sending message/send to", AGENT_ID);
  console.log("Request:", JSON.stringify(request, null, 2));

  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const data = await resp.json();
  console.log("\nResponse:", JSON.stringify(data, null, 2));

  if (data.result?.echo) {
    console.log("\nRound-trip verified: agent echoed the request");
  } else if (data.error) {
    console.error("\nError:", data.error.message);
  }
}

main().catch(console.error);
