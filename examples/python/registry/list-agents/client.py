"""List-Agents example — lists agents and filters by skill tags."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print("=== All Agents ===")
        resp = await client.get(f"{KUBEMQ_URL}/agents")
        data = resp.json()
        agents = data.get("agents", data) if isinstance(data, dict) else data
        for agent in agents:
            skills = [s["id"] for s in agent.get("skills", [])]
            print(f"  {agent['agent_id']}: skills={skills}")

        print(f"\nTotal agents: {len(agents)}")

        print("\n=== Filter by skill_tags=echo ===")
        resp = await client.get(f"{KUBEMQ_URL}/agents", params={"skill_tags": "echo"})
        data = resp.json()
        filtered = data.get("agents", data) if isinstance(data, dict) else data
        for agent in filtered:
            print(f"  {agent['agent_id']}")
        print(f"\nFiltered count: {len(filtered)}")

        print("\n=== Filter by skill_tags=nlp ===")
        resp = await client.get(f"{KUBEMQ_URL}/agents", params={"skill_tags": "nlp"})
        data = resp.json()
        filtered = data.get("agents", data) if isinstance(data, dict) else data
        for agent in filtered:
            print(f"  {agent['agent_id']}")
        print(f"\nFiltered count: {len(filtered)}")


if __name__ == "__main__":
    asyncio.run(main())
