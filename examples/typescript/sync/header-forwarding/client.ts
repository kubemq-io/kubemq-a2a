const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "header-agent-01";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: { parts: [{ text: "Check my headers" }] },
    },
  };

  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Custom-Header": "test-value-123",
    },
    body: JSON.stringify(request),
  });

  const data = await resp.json();
  const headers = data.result?.received_headers || {};

  console.log("=== Header Forwarding Results ===");
  console.log(`X-Custom-Header:    ${headers["x-custom-header"] || "(not forwarded)"}`);
  console.log(`X-KubeMQ-Caller-ID: ${headers["x-kubemq-caller-id"] || "(not present)"}`);

  console.log("\n=== All received headers ===");
  for (const [key, val] of Object.entries(headers)) {
    console.log(`  ${key}: ${val}`);
  }
}

main().catch(console.error);
