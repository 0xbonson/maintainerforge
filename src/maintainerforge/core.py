from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class IssueClassification:
    labels: list[str]
    confidence: float
    rationale: str


@dataclass(frozen=True)
class PullRequestRisk:
    score: int
    level: str
    reasons: list[str]


BUG_TERMS = ("bug", "crash", "error", "traceback", "broken", "fail", "failure")
SECURITY_TERMS = ("security", "vulnerability", "cve", "xss", "sql injection", "secret", "token leak")
DOC_TERMS = ("docs", "documentation", "readme", "typo", "guide")
FEATURE_TERMS = ("feature", "request", "add", "support", "enhancement")
QUESTION_TERMS = ("question", "how", "help", "usage")


def classify_issue(title: str, body: str = "") -> IssueClassification:
    text = f"{title}\n{body}".lower()
    labels: list[str] = []
    reasons: list[str] = []

    if any(term in text for term in SECURITY_TERMS):
        labels.append("security")
        reasons.append("security-sensitive keywords found")
    if any(term in text for term in BUG_TERMS):
        labels.append("bug")
        reasons.append("bug or failure keywords found")
    if any(term in text for term in DOC_TERMS):
        labels.append("documentation")
        reasons.append("documentation keywords found")
    if any(term in text for term in FEATURE_TERMS):
        labels.append("enhancement")
        reasons.append("feature request keywords found")
    if any(term in text for term in QUESTION_TERMS):
        labels.append("question")
        reasons.append("question or usage keywords found")

    if not labels:
        labels.append("needs-triage")
        reasons.append("no strong rule matched")

    confidence = min(0.95, 0.45 + (len(labels) * 0.15))
    return IssueClassification(labels=labels, confidence=confidence, rationale="; ".join(reasons))


def score_pr(files: Iterable[str]) -> PullRequestRisk:
    score = 0
    reasons: list[str] = []
    file_list = list(files)

    sensitive_patterns = ("auth", "security", "crypto", "token", "secret", "permission")
    ci_patterns = (".github/workflows", "Dockerfile", "pyproject.toml", "package.json")

    for path in file_list:
        lowered = path.lower()
        if any(pattern in lowered for pattern in sensitive_patterns):
            score += 35
            reasons.append(f"security-sensitive path changed: {path}")
        elif any(pattern in lowered for pattern in ci_patterns):
            score += 20
            reasons.append(f"build or CI path changed: {path}")
        elif lowered.startswith("docs/") or lowered.endswith(".md"):
            score += 5
        else:
            score += 10

    if len(file_list) > 10:
        score += 20
        reasons.append("large change set")

    score = min(score, 100)
    if score >= 70:
        level = "high"
    elif score >= 35:
        level = "medium"
    else:
        level = "low"

    if not reasons:
        reasons.append("no high-risk file patterns detected")

    return PullRequestRisk(score=score, level=level, reasons=reasons)


def generate_release_notes(commits: Iterable[str]) -> str:
    sections = {"Features": [], "Fixes": [], "Documentation": [], "Maintenance": []}

    for commit in commits:
        entry = commit.strip()
        lowered = entry.lower()
        if lowered.startswith("feat"):
            sections["Features"].append(entry)
        elif lowered.startswith("fix"):
            sections["Fixes"].append(entry)
        elif lowered.startswith("docs"):
            sections["Documentation"].append(entry)
        else:
            sections["Maintenance"].append(entry)

    lines: list[str] = ["# Release Notes", ""]
    for section, items in sections.items():
        if items:
            lines.append(f"## {section}")
            lines.extend(f"- {item}" for item in items)
            lines.append("")

    if len(lines) == 2:
        lines.append("No notable changes detected.")

    return "\n".join(lines).rstrip() + "\n"
