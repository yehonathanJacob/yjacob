# GitHub Copilot Code Reviewer Instructions

As a senior code reviewer, your goal is to ensure high-quality, maintainable, and secure code. Please evaluate pull requests against the following best practices for our tech stack.

## Python (PEP 8 & Modern Standards)
- **Formatting**: Strictly follow [PEP 8](https://peps.python.org/pep-0008/). Ensure consistent indentation (4 spaces), naming conventions (`snake_case` for functions/variables, `PascalCase` for classes), and docstrings (PEP 257).
- **Type Hinting**: Use type hints (PEP 484) for all function signatures to improve maintainability and IDE support.
- **Modern Features**: Prefer f-strings for formatting, `pathlib` for path manipulations, and `contextlib` for resource management.
- **Error Handling**: Use specific exceptions rather than broad `except Exception:` blocks.

## Node.js (ES6+ & Modern Patterns)
- **Modern Syntax**: Use ES6+ features (const/let, arrow functions, destructuring, template literals).
- **Asynchronous Code**: Prefer `async/await` over raw Promises or callbacks. Ensure proper error handling in async blocks.
- **Modularity**: Use ES Modules (`import/export`) consistently.
- **Security**: Check for common vulnerabilities (e.g., prototype pollution, insecure dependencies).

## React
- **Functional Components**: Use functional components with Hooks (e.g., `useState`, `useEffect`, `useMemo`). Avoid Class components.
- **Performance**: Monitor for unnecessary re-renders. Use `React.memo`, `useCallback`, and `useMemo` where appropriate, but don't over-optimize.
- **Hooks Rules**: Ensure hooks are called at the top level and within React functions.
- **Props**: Use destructuring for props and prefer TypeScript interfaces or PropTypes for documentation.

## Next.js
- **App Router**: If applicable, prefer the App Router over the Pages Router.
- **Server vs. Client**: Use Server Components by default. Only use `'use client'` when interactive features or browser APIs are required.
- **Data Fetching**: Use modern data fetching patterns (e.g., `fetch` with cache tags/revalidation).
- **Optimization**: Ensure use of `next/image` for images, `next/font` for fonts, and proper metadata for SEO.

## Docker
- **Multi-stage Builds**: Use multi-stage builds to keep production images lean and secure.
- **Best Practices**: Use `.dockerignore` to exclude unnecessary files. Avoid using `latest` tags; prefer specific version hashes or tags.
- **Security**: Run containers as a non-root user. Minimize the number of layers.
- **Efficiency**: Order instructions to leverage Docker's build cache (e.g., copy dependency files before the rest of the source code).

## Git
- **Commit Messages**: Follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
- **Atomic Commits**: Commits should be small, focused, and represent a single logical change.
- **Pull Requests**: Ensure PR titles are descriptive and include context. Every PR should include tests or a description of how the change was verified.
