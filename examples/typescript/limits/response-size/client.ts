const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "oversize-agent-01";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: { parts: [{ text: "Give me a huge response" }] },
    },
  };

  console.log("Sending request to oversize agent (expects >10MB response)...");

  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const text = await resp.text();
  let data: { error?: { code: number; message: string }; result?: unknown };
  try {
    data = JSON.parse(text);
  } catch {
    console.log(`Raw response (${text.length} bytes): ${text.slice(0, 200)}...`);
    return;
  }

  if (data.error) {
    console.log(`Error code:    ${data.error.code}`);
    console.log(`Error message: ${data.error.message}`);
    const hasTooBig = data.error.message.toLowerCase().includes("too large") ||
                      data.error.code === -32603;
    console.log(`Size limit enforced: ${hasTooBig}`);
  } else {
    console.log("Unexpected: got success response. Response may have been under limit.");
  }
}

main().catch(console.error);
