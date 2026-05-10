# Voting App

A multi-service voting application — a containerized Redis/Postgres-backed setup with portless local domains served via nginx.

## Architecture

| Service | Description | Stack |
|---------|-------------|-------|
| **vote** | Voting frontend | Next.js 16 |
| **result** | Live results dashboard | Next.js 16 |
| **worker** | Background tally worker | Node.js + tsx |
| **redis** | Vote queue | Redis |
| **db** | Result store | PostgreSQL |
| **nginx** | Reverse proxy → portless `.test` domains | nginx:alpine |

## Prerequisites

- Docker + Docker Compose
- macOS or Linux (the install script uses `sudo` to edit `/etc/hosts`)
- Port 80 free on the host (nginx binds it)

## Repo layout

Local-dev-only files (nginx config, install script, this README) live in `local-debug/` so they're separated from production-relevant files. The `docker-compose.yml` at the project root mounts `local-debug/nginx.conf` into the nginx container.

## Setup

Run once to add the local domains to `/etc/hosts`. From the project root (`voting-app/`):

```bash
./local-debug/install.sh
```

Or, if you're already inside `local-debug/`:

```bash
./install.sh
```

You'll be prompted for your sudo password. The script is idempotent — running it again with all entries already present is a no-op.

## Start the app

From the project root (`voting-app/`):

```bash
docker-compose up -d
```

Tear down:

```bash
docker-compose down
```

## Available URLs

| URL | What it serves |
|-----|----------------|
| http://vote.test | Voting UI |
| http://result.test | Results UI |

The original host-port mappings (`localhost:3000`, `localhost:3001`) also work if you want to bypass nginx. The Node inspector ports (`9229`, `9230`, `9231`) are exposed directly on the host — see below.

## Debugging with `chrome://inspect`

The inspector ports are mapped straight to the host by `docker-compose.yml` (`9229` → vote, `9230` → result, `9231` → worker). Wire them into Chrome:

1. Open `chrome://inspect` in Chrome.
2. Click **Configure...** next to "Discover network targets".
3. Add these entries (one per line):
   ```
   localhost:9229
   localhost:9230
   localhost:9231
   ```
4. Click **Done**.
5. Within a few seconds, the `vote`, `result`, and `worker` services should appear under **Remote Target**. Click **inspect** to open DevTools.

> Portless debug names (e.g. `vote.debug`) aren't possible because Chrome's `chrome://inspect` discovery probes don't send a Host header that name-based proxies can route on.

## Troubleshooting

**Port 80 already in use**

```text
Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use
```

Something else is bound to port 80. Find and stop it:

```bash
sudo lsof -iTCP:80 -sTCP:LISTEN     # find the offender
sudo apachectl stop                 # macOS Apache, common culprit
```

**`vote.test` doesn't resolve**

Check `/etc/hosts`:

```bash
grep -E 'vote\.test|result\.test' /etc/hosts
```

If empty, re-run `./local-debug/install.sh`. If a corporate MDM keeps overwriting `/etc/hosts`, configure the entries through your local DNS (e.g. dnsmasq) instead.

**`chrome://inspect` doesn't show targets**

- Confirm the containers are up: `docker-compose ps`
- Hit each inspector port directly to make sure it's reachable:
  ```bash
  curl http://localhost:9229/json/version
  curl http://localhost:9230/json/version
  curl http://localhost:9231/json/version
  ```
  Each should return Node version JSON. If a port is unreachable, check that container's logs (e.g. `docker-compose logs vote`) — the inspector might not be bound.
- In Chrome's Configure dialog, the entries must be `host:port` (`localhost:9229`, not bare `localhost`).

**Edits to `local-debug/nginx.conf` aren't picked up**

The file is bind-mounted, but nginx parses it at startup. Reload (from the project root):

```bash
docker-compose restart nginx
```
