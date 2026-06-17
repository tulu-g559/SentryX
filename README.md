# SentryX 🛡️

An AI-powered "Mission Control" and autonomous observer for local microservices. SentryX acts as a local sentinel, scanning your docker networks, monitoring health, and streaming telemetry for AI-driven troubleshooting.

## Architecture
* **CLI Engine:** Python (Click, Rich)
* **Intelligence Core:** Flask, MongoDB, Docker
* **Dashboard:** React + Vite (Neobrutalist UI)

## Quick Start (Core Backend)
1. Ensure Docker daemon is active.
2. Run `make up` to deploy the SentryX Core and MongoDB containers.
3. Verify at `http://localhost:5000/health`.

## Command Line Interface (CLI)
Navigate to `sentryx-cli/` and install locally: `pip install -e .`

### Available Commands:

* `sentryx scout`
  Scans your local `docker-compose.yml` and outputs a high-contrast matrix of all detected service nodes, container IDs, and exposed ports.

* `sentryx status`
  Runs a localized diagnostic pinging both the host Docker daemon and the SentryX Intelligence Core to verify system health.

* `sentryx logs [SERVICE_NAME] --tail=50`
  Opens a secure telemetry channel to a specific service, pulling the latest terminal logs safely to avoid overwhelming the memory buffers.

---
*Built for resilient local development.*