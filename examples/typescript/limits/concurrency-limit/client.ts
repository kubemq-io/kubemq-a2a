const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "concurrency-agent-01";
const NUM_REQUESTS = 101;

async function sendRequest(id: number): Promise<{ id: number; ok: boolean; errorCode?: number }> {
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
    if (data.error) {
      return { id, ok: false, errorCode: data.error.code };
    }
    return { id, ok: true };
  } catch {
    return { id, ok: false };
  }
}

async function main() {
  console.log(`Sending ${NUM_REQUESTS} concurrent requests (limit is 100)...`);
  const start = Date.now();

  const promises = Array.from({ length: NUM_REQUESTS }, (_, i) => sendRequest(i + 1));
  const results = await Promise.all(promises);

  const elapsed = Date.now() - start;
  const succeeded = results.filter((r) => r.ok).length;
  const rejected = results.filter((r) => r.errorCode === -32603);
  const otherErrors = results.filter((r) => !r.ok && r.errorCode !== -32603);

  console.log(`\nResults (${elapsed}ms):`);
  console.log(`  Total:          ${NUM_REQUESTS}`);
  console.log(`  Succeeded:      ${succeeded} (expect <=100)`);
  console.log(`  Rejected -32603:${rejected.length} (expect >=1)`);
  console.log(`  Other errors:   ${otherErrors.length}`);

  if (rejected.length > 0) {
    console.log(`\nConcurrency limit enforced correctly.`);
  } else {
    console.log(`\nWarning: no requests were rejected — limit may not have been hit.`);
  }
}

main().catch(console.error);
