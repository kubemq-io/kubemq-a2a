# Custom Method

Demonstrates sending a custom JSON-RPC method name through KubeMQ.

## What It Shows

- Sending a non-standard method name (`custom/action`) in the JSON-RPC request
- Verifying that KubeMQ forwards the method name verbatim to the agent
- Agents can handle arbitrary method names beyond `message/send`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project CustomMethod.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project CustomMethod.csproj
```

## Expected Output

```
Handled method: custom/action
Custom method forwarded successfully!
```
