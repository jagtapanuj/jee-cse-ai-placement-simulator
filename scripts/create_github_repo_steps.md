# Manual GitHub/Codex Setup Steps

I could not push to GitHub automatically because no target repository was provided in the chat.

## Steps

1. Create a new GitHub repository, for example: `jee-maharashtra-simulator`.
2. Upload the contents of this folder.
3. Open Codex on the repository.
4. Ask Codex to run:

```bash
python -m unittest discover -s tests -v
python -m app.pure_http_server
```

5. Then ask Codex to implement the next task from `docs/CODEX_HANDOFF.md`.
