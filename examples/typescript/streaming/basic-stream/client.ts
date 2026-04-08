const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "stream-agent-01";

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/stream",
    params: { message: { parts: [{ text: "Stream me some updates" }] } },
  };

  console.log("=== POST-based streaming ===");
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
  let eventCount = 0;

  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      if (!frame.trim()) continue;
      let eventType = "";
      let eventData = "";
      for (const line of frame.split("\n")) {
        if (line.startsWith("event: ")) eventType = line.slice(7).trim();
        else if (line.startsWith("data: ")) eventData = line.slice(6).trim();
      }
      if (!eventType) continue;
      eventCount++;
      const payload = JSON.parse(eventData);
      console.log(`[${eventType}] ${JSON.stringify(payload)}`);
      if (eventType === "task.done" || eventType === "task.error") {
        console.log(`\nStream complete. Total events: ${eventCount}`);
        reader.cancel();
        return;
      }
    }
  }

  console.log(`\nStream ended. Total events: ${eventCount}`);
}

main().catch(console.error);
