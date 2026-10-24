import json

import pytest

from neocomposer.exceptions import HistoryError
from neocomposer.history_manager import HistoryManager


def test_record_sent_email_creates_persistent_history(tmp_path):
    history_path = tmp_path / "config" / "history.json"
    manager = HistoryManager(str(history_path))

    manager.record_sent_email("you@example.com", "Hello", ["report.pdf"])

    stored_history = json.loads(history_path.read_text())
    entry = stored_history["sent"][0]
    assert entry["recipient"] == "you@example.com"
    assert entry["subject"] == "Hello"
    assert entry["attachments"] == ["report.pdf"]
    assert entry["result"] == "success"
    assert entry["sent_at"].endswith("+00:00")


def test_get_sent_emails_returns_newest_first(tmp_path):
    history_path = tmp_path / "history.json"
    history_path.write_text(
        json.dumps(
            {
                "sent": [
                    {
                        "sent_at": "2026-09-03T00:00:00+00:00",
                        "recipient": "old@example.com",
                        "subject": "Older",
                        "attachments": [],
                        "result": "success",
                    },
                    {
                        "sent_at": "2026-09-04T00:00:00+00:00",
                        "recipient": "new@example.com",
                        "subject": "Newer",
                        "attachments": [],
                        "result": "success",
                    },
                ]
            }
        )
    )

    sent_emails = HistoryManager(str(history_path)).get_sent_emails()

    assert [email["subject"] for email in sent_emails] == ["Newer", "Older"]


def test_missing_history_returns_no_sent_emails(tmp_path):
    assert HistoryManager(str(tmp_path / "history.json")).get_sent_emails() == []


def test_corrupt_history_raises_clear_error(tmp_path):
    history_path = tmp_path / "history.json"
    history_path.write_text("not valid json")

    with pytest.raises(HistoryError, match="Invalid history file"):
        HistoryManager(str(history_path)).get_sent_emails()


def test_malformed_history_record_raises_clear_error(tmp_path):
    history_path = tmp_path / "history.json"
    history_path.write_text(json.dumps({"sent": [{"subject": "Missing metadata"}]}))

    with pytest.raises(HistoryError, match="malformed sent email record"):
        HistoryManager(str(history_path)).get_sent_emails()


def test_invalid_history_structure_raises_clear_error(tmp_path):
    history_path = tmp_path / "history.json"
    history_path.write_text(json.dumps({"sent": {}}))

    with pytest.raises(HistoryError, match="'sent' must be a list"):
        HistoryManager(str(history_path)).get_sent_emails()
