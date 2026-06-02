# MaintainerForge

MaintainerForge is a small, auditable maintainer automation toolkit for open source projects. It helps maintainers classify issues, review pull request risk, generate release notes, and keep repository workflows consistent without giving an AI agent write access to production code by default.

## Why this exists

Open source maintainers spend a lot of time on repetitive work: issue triage, pull request review, release notes, security notes, and contributor guidance. MaintainerForge is designed to make those workflows reproducible, reviewable, and safe for small maintainers.

## Core features

- Rule based issue classification from title and body
- Pull request risk scoring from changed file paths
- Release note generation from commit messages
- JSON output for GitHub Actions and CI workflows
- Safe by default: no secrets required, no mutation unless explicitly wired by the maintainer

## Install

```bash
pip install git+https://github.com/0xbonson/maintainerforge.git
```

For local development:

```bash
git clone https://github.com/0xbonson/maintainerforge.git
cd maintainerforge
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Usage

Classify an issue:

```bash
maintainerforge classify-issue --title "Bug: crash on startup" --body "The CLI exits with traceback"
```

Score PR risk:

```bash
maintainerforge score-pr --files src/auth.py pyproject.toml docs/usage.md
```

Generate release notes:

```bash
maintainerforge release-notes --commits "fix: handle empty token" "feat: add JSON output"
```

## GitHub Action example

```yaml
name: MaintainerForge
on:
  issues:
    types: [opened, edited]
  pull_request:
    types: [opened, synchronize]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: 0xbonson/maintainerforge@v0.1.1
```

## OpenAI Codex usage plan

MaintainerForge is intentionally built for maintainer workflows. API credits would be used for optional, reviewable automation such as PR summaries, security-focused review notes, release note drafts, test repair suggestions, and issue deduplication. Human maintainers remain in control.

## Security model

MaintainerForge does not need access to private keys, production credentials, or user secrets. For security-sensitive analysis, maintainers should run it only on repositories they own or are authorized to review.

See [SECURITY.md](SECURITY.md).

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT
