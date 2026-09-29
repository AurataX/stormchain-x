# Local Docker storage policy

The user authorized removing STORMCHAIN-X Docker artifacts after verification
because local storage is limited. This includes disposable demo/test database
volumes. Save verification evidence before cleanup; committed fixtures rebuild data.

1. Inspect `docker compose ps -a`, `docker image ls`, `docker volume ls`, and
   `docker system df` to confirm ownership and record initial storage.
2. Run `docker compose down --volumes --rmi all --remove-orphans` from this repository.
3. Inspect remaining images/cache. Remove only project-owned or exclusively
   project-used artifacts. Do not force-remove shared images.
4. Recheck container/image/volume counts and report actual reclaimed storage.

Do not run global `docker system prune --all --volumes` without explicit scope
and ownership checks. This policy never authorizes deleting other projects,
source code, `.env`, or cloud resources.

After cleanup the API will be offline. Use `docker compose up --build -d`
when needed, or SQLite development to avoid Docker storage. Tests and seed data
remain in Git; the temporary database is intentionally not backed up.
