from triageforge.core import classify_issue, generate_release_notes, score_pr


def test_classify_bug_issue():
    result = classify_issue("Bug: crash on startup", "Traceback appears after install")
    assert "bug" in result.labels
    assert result.confidence > 0.5


def test_classify_security_issue():
    result = classify_issue("Possible token leak", "A secret appears in logs")
    assert "security" in result.labels


def test_score_pr_sensitive_path():
    result = score_pr(["src/auth.py", "docs/usage.md"])
    assert result.level in {"medium", "high"}
    assert result.score >= 35


def test_release_notes_sections():
    notes = generate_release_notes(["feat: add JSON output", "fix: handle empty issue body"])
    assert "## Features" in notes
    assert "## Fixes" in notes
