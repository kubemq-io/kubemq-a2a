const KUBEMQ_URL = "http://localhost:9090";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: { parts: [{ text: "Hello?" }] },
    },
  };

  console.log("Sending to nonexistent agent...");

  const resp = await fetch(`${KUBEMQ_URL}/a2a/nonexistent-agent`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const data = await resp.json();
  console.log("Response:", JSON.stringify(data, null, 2));

  if (data.error) {
    console.log(`\nError code:    ${data.error.code} (expect -32002)`);
    console.log(`Error message: ${data.error.message}`);
    console.log(`Match:         ${data.error.code === -32002}`);
  }
}

main().catch(console.error);
