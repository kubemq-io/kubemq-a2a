"""Agent-Info example — retrieves and displays all agent card fields."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "full-info-agent-01"


async def main() -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        print(f"Status: {resp.status_code}")
        data = resp.json()

        print(f"\n--- Agent Card ---")
        print(f"  agent_id:           {data.get('agent_id')}")
        print(f"  name:               {data.get('name')}")
        print(f"  description:        {data.get('description')}")
        print(f"  version:            {data.get('version')}")
        print(f"  url:                {data.get('url')}")
        print(f"  defaultInputModes:  {data.get('defaultInputModes')}")
        print(f"  defaultOutputModes: {data.get('defaultOutputModes')}")
        print(f"  protocolVersions:   {data.get('protocolVersions')}")
        print(f"  registered_at:      {data.get('registered_at')}")
        print(f"  last_seen:          {data.get('last_seen')}")

        skills = data.get("skills", [])
        print(f"\n--- Skills ({len(skills)}) ---")
        for skill in skills:
            print(f"  [{skill['id']}] {skill['name']}: {skill['description']}")
            print(f"    tags: {skill.get('tags', [])}")


if __name__ == "__main__":
    asyncio.run(main())
