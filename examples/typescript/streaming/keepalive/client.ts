const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "keepalive-agent-01";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/stream",
    params: { message: { parts: [{ text: "Send with keepalive pauses" }] } },
  };

  console.log("Connecting to stream (expect ~70s total with keepalive comments)...");

  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify(request),
  });

  const reader = resp.body!.getReader();
  const decoder = new TextDecoder();
  let keepaliveCount = 0;
  let eventCount = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const text = decoder.decode(value, { stream: true });

    for (const line of text.split("\n")) {
      if (line.startsWith(": keepalive") || line === ": keepalive") {
        keepaliveCount++;
        console.log(`[KEEPALIVE] #${keepaliveCount} at ${new Date().toISOString()}`);
      } else if (line.startsWith("event: ")) {
        const eventType = line.slice(7).trim();
        eventCount++;
        console.log(`[EVENT]     #${eventCount} ${eventType} at ${new Date().toISOString()}`);
      } else if (line.startsWith("data: ")) {
        const payload = JSON.parse(line.slice(6).trim());
        if (payload.type === "done") {
          console.log(`\nStream complete.`);
          console.log(`  Events:     ${eventCount}`);
          console.log(`  Keepalives: ${keepaliveCount}`);
          reader.cancel();
          return;
        }
      }
    }
  }
}

main().catch(console.error);
