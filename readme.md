<p align="center">
  <img src="https://smolenv.com/smol-sand-a.webp" width="467" height="195" alt="smol agents in a sandbox">
</p>

# smol

smol is an agent

smol is smol

smol is so smol you can understand it in an afternoon

smol is fewer tokens

smol is fewer dependencies

smol is easy to adapt

smol is easy to build upon

## Python

[`smol.py`](smol.py) includes retries, context compaction, and shell output truncation.

## Golf

smol implementations with the essential agent loop, user input, and context window usage

without retries, compaction, or shell output truncation:

- [Python](golf/smol.py)
- [Go](golf/smol.go)
- [Clojure](golf/smol.clj)
- [PHP](golf/smol.php)

## Run

Pass URL of an endpoint that is compatible with the OpenAI Responses API

```sh
python3 smol.py http://127.0.0.1:8787/v1/responses

# golfed Go
go run golf/smol.go http://127.0.0.1:8787/v1/responses
```

- enter prompt at `>`
- empty input exits the Python implementation
- ctrl+d exits
- model requested commands get executed directly via `sh` (!)

Optional quality of life: rlwrap for line editing and persistent history

```sh
rlwrap -H ~/.smol_history python3 smol.py http://127.0.0.1:8787/v1/responses

# or
rlwrap -H ~/.smol_history go run golf/smol.go http://127.0.0.1:8787/v1/responses
```

`smol` does not add credentials to requests.

Run `smol` in an appropriate environment that has access to an API endpoint `smol` can reach

e.g. you can run a small proxy that handles your API key or ChatGPT/Codex session and forwards the requests

## Questions

Paste this into ChatGPT, Claude, Codex, Pi, or your favorite agent:

> Read the code of smol.py and answer all questions from the README:
> https://github.com/smol-env/smol

### Understand

> What does smol do?

> Why is less code useful?

> Why have no system prompt?

> Why have only one tool?

> Why is the context window precious?

> Why truncate shell output? Why in this way?

> Why does compaction keep history as a stable prefix? How does this affect caching and cost?

> What assumptions and failure modes does smol have?

> Why leave credentials and permissions to the environment?

> Explain this implementation line by line.

### Compare

> Compare smol with Pi, OpenCode, Codex, Hermes, and Claude Code by:
>
> - code size
> - third-party dependencies
> - runtime performance (time, tokens, RAM, CPU, tool use, requests, …)
> - cost per task
>
> How can we compare them fairly?

> How can we compare agent traces and VM resource usage quantitatively and qualitatively?

### Build

> What kind of apps could we build on top of smol?

> How can we use a different model with smol?

> How could we improve the terminal UI/UX with just a few changes?

> How could we add a minimal web UI instead of a terminal UI?

> How could we add a second tool without introducing a framework?

> How could we add session save and replay using the standard library?

> How could we build a minimal standard-library-only proxy that keeps API credentials outside smol?

> Port smol to another language while keeping it smol.
> Use only the standard library or minimal dependencies when necessary.
