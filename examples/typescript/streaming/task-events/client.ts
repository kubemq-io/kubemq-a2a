const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "task-events-agent-01";

function parseSSE(chunk: string): Array<{ event: string; data: string }> {
  const events: Array<{ event: string; data: string }> = [];
  let currentEvent = "";
  let currentData = "";

  for (const line of chunk.split("\n")) {
    if (line.startsWith("event: ")) {
      currentEvent = line.slice(7).trim();
    } else if (line.startsWith("data: ")) {
      currentData = line.slice(6).trim();
    } else if (line === "" && currentEvent) {
      events.push({ event: currentEvent, data: currentData });
      currentEvent = "";
      currentData = "";
    }
  }
  return events;
}

async function main() {
  const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "message/stream",
    params: { message: { parts: [{ text: "Send me task events" }] } },
  };

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
  const counts: Record<string, number> = {};

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const text = decoder.decode(value, { stream: true });
    const events = parseSSE(text);

    for (const evt of events) {
      counts[evt.event] = (counts[evt.event] || 0) + 1;
      const payload = JSON.parse(evt.data);

      switch (evt.event) {
        case "task.status":
          console.log(`[STATUS]   progress=${payload.payload.progress}/${payload.payload.total} status=${payload.payload.status}`);
          break;
        case "task.artifact":
          console.log(`[ARTIFACT] name=${payload.payload.name} data=${JSON.stringify(payload.payload.data)}`);
          break;
        case "task.done":
          console.log(`[DONE]     result=${payload.payload.final_result}`);
          break;
        case "task.error":
          console.log(`[ERROR]    ${payload.payload.message}`);
          break;
      }

      if (evt.event === "task.done" || evt.event === "task.error") {
        console.log("\n=== Event Summary ===");
        for (const [type, count] of Object.entries(counts)) {
          console.log(`  ${type}: ${count}`);
        }
        reader.cancel();
        return;
      }
    }
  }
}

main().catch(console.error);
