# n8n Docker quick-start: contributor brief

Source: art_01M6W20A2JVVK9Q1A3JBG629TQ r1 (documentary, not run).
This brief is MIT. n8n itself is under the Sustainable Use License — read LICENCE_DECISION.md first.

## What exists

The article gives two shell commands sourced from the n8n README at commit 3895cb31:

```sh
docker volume create n8n_data
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

Outputs are **expected, not observed**. No contributor has yet reported a successful run.

## The three decisions before you start

1. **Port conflict** — is 5678 already in use on your machine?
   Check: `lsof -i :5678` (macOS/Linux) or `netstat -an | findstr 5678` (Windows).
   If yes, change the left side of `-p`: e.g. `-p 5679:5678`, then open port 5679 in the browser.

2. **Volume name** — `n8n_data` is arbitrary. Choose a name that won't collide with other projects.
   The name matters only for `docker volume rm` later; the container path `/home/node/.n8n` is fixed.

3. **Licence scope** — see LICENCE_DECISION.md before building anything for a client or product.

## What to report if you run this

- Docker version and OS
- Whether the editor loaded at port 5678
- Whether workflows persisted after stopping and restarting the container
- Any error output verbatim

This upgrades the article's evidence status from `not_run` to observed — the clearest gap in the current research.