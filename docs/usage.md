# Usage

MaintainerForge is designed for review-only maintainer automation.

## Local usage

```bash
maintainerforge classify-issue --title "Bug: crash on startup" --body "The CLI exits with traceback"
```

## Intended workflow

1. Maintainer receives a new issue or pull request.
2. MaintainerForge analyzes metadata and text.
3. The tool generates a suggested label, risk level, or release note.
4. The maintainer reviews the output before taking action.

MaintainerForge should not automatically merge code, approve pull requests, or perform destructive repository actions without human review.
