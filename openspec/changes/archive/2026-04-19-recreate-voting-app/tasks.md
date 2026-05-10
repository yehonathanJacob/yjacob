# Tasks: Recreate Voting App

## Phase 1: Scaffolding
- [x] Create base directory `JSLab/PersonalProjects/voting-app`
- [x] Initialize `vote` service: `npx create-next-app@latest vote --ts --no-tailwind --app --no-src-dir --import-alias "@/*"`
- [x] Initialize `result` service: `npx create-next-app@latest result --ts --no-tailwind --app --no-src-dir --import-alias "@/*"`
- [x] Initialize `worker` service: Create `worker` folder with `package.json` and basic TypeScript setup.

## Phase 2: Docker Configuration
- [x] Create `Dockerfile.dev` for `vote` service.
- [x] Create `Dockerfile.dev` for `result` service.
- [x] Create `Dockerfile.dev` for `worker` service.
- [x] Create root `docker-compose.yml` defining all 5 services (vote, result, worker, redis, postgres).

## Phase 3: Infrastructure Setup
- [x] Add `ioredis` to `vote` and `worker`.
- [x] Add `pg` to `result` and `worker`.
- [x] Implement Redis connection utility in `vote`.
- [x] Implement Postgres and Redis connection utility in `worker`.
- [x] Implement Postgres connection utility in `result`.

## Phase 4: Service Implementation
- [x] **Vote:** Create UI for voting and API route to push to Redis.
- [x] **Worker:** Implement the main loop to consume Redis and write to Postgres.
- [x] **Result:** Create dashboard to display vote tallies from Postgres.

## Phase 5: Testing & Validation
- [x] Ensure `docker-compose.yml` maps Postgres (5432) and Redis (6379) to localhost for local testing.
- [x] Initialize Playwright in the project root: `npm init playwright@latest`.
- [x] Implement local unit/integration tests for each service.
- [x] Implement E2E "Happy Path" test in Playwright.
- [x] Create `.vscode/launch.json` and verify breakpoints on ports 9229, 9230, and 9231.
