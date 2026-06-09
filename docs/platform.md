# Backing Platform — Arr Suite

`arr-mcp` is a **client** of the **Arr Suite** of media-automation services. This page
provides a Docker recipe for provisioning them locally to serve as the targets of the
`*_BASE_URL` / `*_TOKEN` connection variables. For production topologies, follow the
upstream documentation for each service.

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

The Arr Suite is published as the LinuxServer.io image family (and the maintainers'
images for Seerr and Chaptarr). The following stack provisions each service on its
conventional port with a persistent config volume:

```yaml
# docker/arr-stack.compose.yml
services:
  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - sonarr-config:/config
    ports:
      - "8989:8989"
    restart: unless-stopped

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - radarr-config:/config
    ports:
      - "7878:7878"
    restart: unless-stopped

  lidarr:
    image: lscr.io/linuxserver/lidarr:latest
    container_name: lidarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - lidarr-config:/config
    ports:
      - "8686:8686"
    restart: unless-stopped

  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - prowlarr-config:/config
    ports:
      - "9696:9696"
    restart: unless-stopped

  bazarr:
    image: lscr.io/linuxserver/bazarr:latest
    container_name: bazarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - bazarr-config:/config
    ports:
      - "6767:6767"
    restart: unless-stopped

  seerr:
    image: ghcr.io/seerr-team/seerr:latest
    container_name: seerr
    environment:
      - TZ=Etc/UTC
    volumes:
      - seerr-config:/app/config
    ports:
      - "5055:5055"
    restart: unless-stopped

volumes:
  sonarr-config:
  radarr-config:
  lidarr-config:
  prowlarr-config:
  bazarr-config:
  seerr-config:
```

```bash
docker compose -f docker/arr-stack.compose.yml up -d

# Each service exposes a ping/health endpoint, e.g. Sonarr:
curl -s http://localhost:8989/ping
```

Retrieve each service's API key from its **Settings → General** page; that value is
what you supply as the matching `*_TOKEN` / `*_API_KEY` to `arr-mcp`.

## Connect arr-mcp

```bash
export SONARR_BASE_URL=http://localhost:8989
export SONARR_TOKEN=your_sonarr_api_key
export RADARR_BASE_URL=http://localhost:7878
export RADARR_TOKEN=your_radarr_api_key
# …repeat for the services you run

arr-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places the Arr services and the MCP server on one Docker network, so
the server reaches each service by container name:

```yaml
# docker/stack.compose.yml
services:
  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    environment: [PUID=1000, PGID=1000, TZ=Etc/UTC]
    volumes: ["sonarr-config:/config"]
    ports: ["8989:8989"]

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    environment: [PUID=1000, PGID=1000, TZ=Etc/UTC]
    volumes: ["radarr-config:/config"]
    ports: ["7878:7878"]

  arr-mcp:
    image: knucklessg1/arr-mcp:latest
    depends_on: [sonarr, radarr]
    environment:
      - SONARR_BASE_URL=http://sonarr:8989
      - SONARR_TOKEN=your_sonarr_api_key
      - RADARR_BASE_URL=http://radarr:7878
      - RADARR_TOKEN=your_radarr_api_key
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  sonarr-config:
  radarr-config:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

The homelab reference deployment of the full Arr Suite (including VPN gateway,
indexer solver, and download client) is maintained in the ecosystem
[`arr-stack`](https://github.com/Knuckles-Team) services repository.
