# Tasks: Recreate Voting App

## Phase 1: Scaffolding
- [ ] Create base directory `JSLab/PersonalProjects/voting-app`
- [ ] Initialize `vote` service: `npx create-next-app@latest vote --ts --no-tailwind --app --no-src-dir --import-alias "@/*"`
- [ ] Initialize `result` service: `npx create-next-app@latest result --ts --no-tailwind --app --no-src-dir --import-alias "@/*"`
- [ ] Initialize `worker` service: Create `worker` folder with `package.json` and basic TypeScript setup.

## Phase 2: Docker Configuration
- [ ] Create `Dockerfile.dev` for `vote` service.
- [ ] Create `Dockerfile.dev` for `result` service.
- [ ] Create `Dockerfile.dev` for `worker` service.
- [ ] Create root `docker-compose.yml` defining all 5 services (vote, result, worker, redis, postgres).

## Phase 3: Infrastructure Setup
- [ ] Add `ioredis` to `vote` and `worker`.
- [ ] Add `pg` to `result` and `worker`.
- [ ] Implement Redis connection utility in `vote`.
- [ ] Implement Postgres and Redis connection utility in `worker`.
- [ ] Implement Postgres connection utility in `result`.

## Phase 4: Service Implementation
- [ ] **Vote:** Create UI for voting and API route to push to Redis.
- [ ] **Worker:** Implement the main loop to consume Redis and write to Postgres.
- [ ] **Result:** Create dashboard to display vote tallies from Postgres.

## Phase 5: Testing & Validation
- [ ] Ensure `docker-compose.yml` maps Postgres (5432) and Redis (6379) to localhost for local testing.
- [ ] Initialize Playwright in the project root: `npm init playwright@latest`.
- [ ] Implement local unit/integration tests for each service.
- [ ] Implement E2E "Happy Path" test in Playwright.
- [ ] Create `.vscode/launch.json` and verify breakpoints on ports 9229, 9230, and 9231.
