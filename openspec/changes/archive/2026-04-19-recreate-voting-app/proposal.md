# Proposal: Recreate Voting App with Node.js/Next.js

## Goal
Recreate the classic Docker voting application using a modern Node.js and Next.js stack. This project will be located in `JSLab/PersonalProjects/voting-app` and will feature a 5-service architecture managed by Docker Compose.

## Scope
- Initialize the project structure in `JSLab/PersonalProjects/voting-app`.
- Create a `vote` service (Next.js).
- Create a `result` service (Next.js).
- Create a `worker` service (Node.js).
- Configure `docker-compose.yml` with Redis and Postgres.
- Implement basic voting logic and result display.
- Ensure debuggability for each service.

## Tech Stack
- **Next.js** (TypeScript) for Vote and Result services.
- **Node.js** (TypeScript) for Worker service.
- **Redis** for the queue.
- **Postgres** for the database.
- **Docker** and **Docker Compose** for containerization.

## Key Changes
- Project scaffolding.
- Dockerfile for each service.
- Docker Compose configuration.
- Shared types/interfaces (if needed).

## Non-Goals
- Authentication (for now).
- Advanced UI/UX (keep it simple for the initial prototype).
- Production-grade deployment configuration.
