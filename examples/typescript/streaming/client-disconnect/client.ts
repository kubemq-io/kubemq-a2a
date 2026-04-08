const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "disconnect-agent-01";
const MAX_EVENTS = 2;

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
    params: { message: { parts: [{ text: "Stream with disconnect" }] } },
  };

  console.log(`Connecting to stream, will disconnect after ${MAX_EVENTS} events...`);

  const controller = new AbortController();
  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify(request),
    signal: controller.signal,
  });

  const reader = resp.body!.getReader();
  const decoder = new TextDecoder();
  let eventCount = 0;

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      const events = parseSSE(text);

      for (const evt of events) {
        eventCount++;
        const payload = JSON.parse(evt.data);
        console.log(`[${evt.event}] progress=${payload.payload?.progress}`);

        if (eventCount >= MAX_EVENTS) {
          console.log(`\nReceived ${MAX_EVENTS} events, disconnecting...`);
          reader.cancel();
          controller.abort();
          console.log("Disconnected. KubeMQ will clean up the stream.");
          return;
        }
      }
    }
  } catch (err: unknown) {
    if (err instanceof Error && err.name === "AbortError") {
      console.log("Connection aborted (expected).");
    } else {
      throw err;
    }
  }
}

main().catch(console.error);
