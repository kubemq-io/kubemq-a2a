const KUBEMQ_URL = "http://localhost:9090";
const AGENT_ID = "custom-method-agent-01";

async function sendRpc(method: string, params: unknown) {
  const request = { jsonrpc: "2.0", id: Date.now(), method, params };
  const resp = await fetch(`${KUBEMQ_URL}/a2a/${AGENT_ID}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  return resp.json();
}

async function main() {
  console.log("=== custom/action ===");
  const custom = await sendRpc("custom/action", { data: "s10-custom" });
  console.log("Response:", JSON.stringify(custom, null, 2));

  console.log("\n=== tasks/get ===");
  const taskGet = await sendRpc("tasks/get", { taskId: "task-001" });
  console.log("Response:", JSON.stringify(taskGet, null, 2));

  console.log("\n=== tasks/cancel ===");
  const taskCancel = await sendRpc("tasks/cancel", { taskId: "task-002" });
  console.log("Response:", JSON.stringify(taskCancel, null, 2));
}

main().catch(console.error);
