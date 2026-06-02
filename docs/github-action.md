# GitHub Action Example

This example shows how MaintainerForge can be used in a review-only workflow.

```yaml
name: MaintainerForge

on:
  issues:
    types: [opened, edited]
  pull_request:
    types: [opened, synchronize]

jobs:
  maintainerforge:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: read
      pull-requests: read
    steps:
      - uses: actions/checkout@v4
      - uses: 0xbonson/maintainerforge@v0.1.1
```

## Safety note

The recommended default is read-only permissions. MaintainerForge should generate suggestions for maintainers to review, not automatically modify issues, approve pull requests, or merge code.
