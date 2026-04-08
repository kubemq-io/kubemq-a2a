# C# examples

KubeMQ A2A examples using **ASP.NET Core** minimal hosting for agents and **`HttpClient`** for clients. NuGet packages **`A2A`** and **`A2A.AspNetCore`** match the official .NET SDK; sample code still uses explicit JSON-RPC JSON for clarity and parity with other languages.

## Requirements

- .NET 8 SDK

## Restore and build

From this directory:

```bash
dotnet restore
dotnet build
```

The root [KubeMqA2aExamples.csproj](KubeMqA2aExamples.csproj) pulls shared package references. **Each scenario directory** will also contain its own `.csproj` next to `Agent.cs` and `Client.cs` (per spec §5.5); build and run from that folder when those files exist.

## Run an example

From a scenario directory (once present):

```bash
cd registry/register-agent
dotnet run --project . -- agent
dotnet run --project . -- client
```

Exact arguments follow each scenario’s `README.md`.

## Environment

Default KubeMQ base address is `http://localhost:9090` unless configured otherwise in code.

## Stack (see spec §5.5)

| Role | Package |
|------|---------|
| A2A types / client helpers | `A2A` |
| ASP.NET Core integration | `A2A.AspNetCore` |
| Agent host | ASP.NET Core / Kestrel |
| HTTP client | `System.Net.Http.HttpClient` |

Package versions are set in `KubeMqA2aExamples.csproj`.
