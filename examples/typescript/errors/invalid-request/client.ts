const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "echo-agent-01";

async function sendRaw(label: string, url: string, opts: RequestInit) {
  console.log(`=== ${label} ===`);
  try {
    const resp = await fetch(url, opts);
    const text = await resp.text();
    let data: unknown;
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
    console.log(`Status: ${resp.status}`);
    console.log(`Response: ${JSON.stringify(data, null, 2)}\n`);
  } catch (err) {
    console.log(`Error: ${err}\n`);
  }
}

async function main() {
  await sendRaw(
    "Invalid JSON body (expect -32700)",
    `${KUBEMQ_URL}/a2a/${AGENT_ID}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{invalid json!!!}",
    },
  );

  await sendRaw(
    "Missing method field (expect -32600)",
    `${KUBEMQ_URL}/a2a/${AGENT_ID}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, params: {} }),
    },
  );

  await sendRaw(
    "Wrong JSON-RPC version (expect -32600)",
    `${KUBEMQ_URL}/a2a/${AGENT_ID}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "1.0", id: 1, method: "message/send", params: {} }),
    },
  );

  await sendRaw(
    "Wrong Content-Type (expect -32700)",
    `${KUBEMQ_URL}/a2a/${AGENT_ID}`,
    {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "message/send", params: {} }),
    },
  );

  await sendRaw(
    "Invalid agent_id format (expect -32600)",
    `${KUBEMQ_URL}/a2a/UPPERCASE-BAD`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "message/send", params: {} }),
    },
  );
}

main().catch(console.error);
