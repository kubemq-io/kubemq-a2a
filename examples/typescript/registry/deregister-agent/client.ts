const KUBEMQ_URL = "http://localhost:9090";

async function main() {
  console.log("=== Deregister via POST /agents/deregister ===");
  const postResp = await fetch(`${KUBEMQ_URL}/agents/deregister`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_id: "dereg-post-01" }),
  });
  console.log(`POST deregister status: ${postResp.status}`);
  const postBody = await postResp.text();
  console.log(`Response: ${postBody || "(empty)"}`);

  const verifyPost = await fetch(`${KUBEMQ_URL}/agents/dereg-post-01`);
  console.log(`Verify GET status: ${verifyPost.status} (expect 404)\n`);

  console.log("=== Deregister via DELETE /agents/{agent_id} ===");
  const delResp = await fetch(`${KUBEMQ_URL}/agents/dereg-delete-01`, {
    method: "DELETE",
  });
  console.log(`DELETE status: ${delResp.status}`);
  const delBody = await delResp.text();
  console.log(`Response: ${delBody || "(empty)"}`);

  const verifyDel = await fetch(`${KUBEMQ_URL}/agents/dereg-delete-01`);
  console.log(`Verify GET status: ${verifyDel.status} (expect 404)\n`);

  console.log("=== Deregister non-existent agent ===");
  const notFound = await fetch(`${KUBEMQ_URL}/agents/deregister`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_id: "nonexistent-agent" }),
  });
  console.log(`Status: ${notFound.status} (expect 404)`);
  const nfBody = await notFound.json();
  console.log(`Error: ${nfBody.error}`);
}

main().catch(console.error);
