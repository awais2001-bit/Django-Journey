## GitHub Copilot Chat

- Extension Version: 0.22.4 (prod)
- VS Code: vscode/1.95.3
- OS: Mac

## Network

User Settings:

```json
  "github.copilot.advanced": {
    "debug.useElectronFetcher": true,
    "debug.useNodeFetcher": false
  }
```

Connecting to https://api.github.com:

- DNS ipv4 Lookup: 20.207.73.85 (148 ms)
- DNS ipv6 Lookup: ::ffff:20.207.73.85 (82 ms)
- Electron Fetcher (configured): HTTP 200 (652 ms)
- Node Fetcher: HTTP 200 (579 ms)
- Helix Fetcher: HTTP 200 (650 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:

- DNS ipv4 Lookup: 140.82.112.22 (8 ms)
- DNS ipv6 Lookup: ::ffff:140.82.112.22 (12 ms)
- Electron Fetcher (configured): HTTP 200 (807 ms)
- Node Fetcher: HTTP 200 (764 ms)
- Helix Fetcher: HTTP 200 (873 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).
