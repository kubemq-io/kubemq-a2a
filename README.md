# kubemq-a2a

Documentation, code examples, and burn-in suite for the KubeMQ A2A (Agent-to-Agent) endpoint.

## What Is This?

kubemq-a2a is a reference repository for developers integrating AI agents with KubeMQ via the A2A (Agent-to-Agent) protocol. It provides:

- **Documentation** — Complete reference for the KubeMQ A2A JSON-RPC 2.0 endpoint and agent registry REST API
- **Code Examples** — Copy-paste-ready examples in 5 languages (Python, TypeScript, Java, Go, C#)
- **Burn-in Suite** — Python test harness for validating KubeMQ A2A deployments

## Quick Start

1. Start KubeMQ with A2A enabled
2. Pick your language under `examples/`
3. Run an agent in one terminal, a client in another
4. See the A2A round-trip in action

See [docs/getting-started.md](docs/getting-started.md) for the full 5-minute guide.

## Repository Structure

```
kubemq-a2a/
├── README.md                    # This file
├── LICENSE                      # Apache 2.0
├── .gitignore                   # Multi-language gitignore
├── docs/                        # Full documentation
│   ├── README.md                # Documentation index
│   ├── architecture.md          # A2A gateway architecture
│   ├── getting-started.md       # 5-minute quick start
│   ├── configuration.md         # Server and agent configuration
│   ├── patterns/                # Messaging pattern guides
│   ├── guides/                  # How-to guides
│   └── reference/               # API and protocol reference
├── examples/                    # Code examples (5 languages)
│   ├── python/                  # Python examples
│   ├── typescript/              # TypeScript examples
│   ├── java/                    # Java examples
│   ├── go/                      # Go examples
│   └── csharp/                  # C# examples
└── burnin/                      # Python burn-in test suite
    ├── burnin-config.yaml       # Test configuration
    └── src/                     # Test harness source
```

## Documentation

See [docs/README.md](docs/README.md) for the full documentation index.

## Examples

See [examples/README.md](examples/README.md) for the example matrix across all languages.

## Burn-in

See [burnin/README.md](burnin/README.md) for soak testing and validation.

## License

Apache 2.0 — see [LICENSE](LICENSE).
