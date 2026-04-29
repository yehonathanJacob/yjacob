# Test Plan: Recreate Voting App

## 1. Local Development Testing (Unit & Integration)
Tests will be run directly on the host machine for a fast feedback loop.
- **Environment:** Node.js installed on the host.
- **Dependencies:** Databases (Redis/Postgres) must be running in Docker with ports mapped to localhost.
- **Command:** `npm test` inside each service directory.
- **Tooling:** Vitest/Jest.

## 2. End-to-End (E2E) Testing
Full system validation from the browser, run from the host machine.
- **Tooling:** Playwright.
- **Flow:**
    1. `docker-compose up` to start all services.
    2. Run Playwright on host: `npx playwright test`.
    3. Playwright interacts with `http://localhost:3000` (Vote) and verifies `http://localhost:3001` (Result).

## 4. Debugging Validation
- **Breakpoint Test:** Attach VS Code to each service (9229, 9230, 9231) and ensure breakpoints are hit during a vote cycle.

## 5. Failure Scenarios (Optional/Future)
- **Redis Down:** Ensure the Vote service handles Redis connection errors gracefully.
- **Postgres Down:** Ensure the Worker retries or handles DB connection failures.
