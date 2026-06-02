from __future__ import annotations

import argparse
import json
from typing import Any

from .core import classify_issue, generate_release_notes, score_pr


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(prog="triageforge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify = subparsers.add_parser("classify-issue", help="Classify an issue title and body")
    classify.add_argument("--title", required=True)
    classify.add_argument("--body", default="")

    score = subparsers.add_parser("score-pr", help="Score pull request risk from changed files")
    score.add_argument("--files", nargs="+", required=True)

    release = subparsers.add_parser("release-notes", help="Generate release notes from commits")
    release.add_argument("--commits", nargs="+", required=True)

    args = parser.parse_args()

    if args.command == "classify-issue":
        result = classify_issue(args.title, args.body)
        _print_json({"labels": result.labels, "confidence": result.confidence, "rationale": result.rationale})
    elif args.command == "score-pr":
        result = score_pr(args.files)
        _print_json({"score": result.score, "level": result.level, "reasons": result.reasons})
    elif args.command == "release-notes":
        print(generate_release_notes(args.commits), end="")


if __name__ == "__main__":
    main()
