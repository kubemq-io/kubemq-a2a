# Header Forwarding

Demonstrates that KubeMQ forwards custom HTTP headers to the target agent.

## What It Shows

- Sending custom `X-*` headers with a JSON-RPC request
- Agent receives and returns the forwarded headers
- KubeMQ may inject its own headers (e.g., `X-KubeMQ-Caller-ID`)

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project HeaderForwarding.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project HeaderForwarding.csproj
```

## Expected Output

```
Forwarded headers: {"X-Custom-Header":"my-custom-value",...}
X-Custom-Header was forwarded successfully!
```
