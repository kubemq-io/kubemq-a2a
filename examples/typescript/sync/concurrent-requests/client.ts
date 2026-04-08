const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "concurrent-agent-01";
const NUM_REQUESTS = 20;

async function sendRequest(id: number): Promise<{ id: number; ok: boolean; ms: number }> {
  const start = Date.now();
  const request = {
    jsonrpc: "2.0",
    id,
    method: "message/send",
    params: { message: { parts: [{ text: `Request ${id}` }] } },
  };

  try {
    const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    const data = await resp.json();
    return { id, ok: !!data.result, ms: Date.now() - start };
  } catch {
    return { id, ok: false, ms: Date.now() - start };
  }
}

async function main() {
  console.log(`Sending ${NUM_REQUESTS} concurrent requests to ${AGENT_ID}...`);
  const start = Date.now();

  const promises = Array.from({ length: NUM_REQUESTS }, (_, i) => sendRequest(i + 1));
  const results = await Promise.all(promises);

  const elapsed = Date.now() - start;
  const succeeded = results.filter((r) => r.ok).length;
  const failed = results.filter((r) => !r.ok).length;
  const avgMs = Math.round(results.reduce((s, r) => s + r.ms, 0) / results.length);

  console.log(`\nResults:`);
  console.log(`  Total:     ${NUM_REQUESTS}`);
  console.log(`  Succeeded: ${succeeded}`);
  console.log(`  Failed:    ${failed}`);
  console.log(`  Avg time:  ${avgMs}ms`);
  console.log(`  Wall time: ${elapsed}ms`);
}

main().catch(console.error);
