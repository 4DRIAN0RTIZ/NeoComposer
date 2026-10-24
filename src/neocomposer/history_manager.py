import json
import os
from datetime import datetime, timezone
from typing import Any

from .exceptions import HistoryError


class HistoryManager:
    """Persists and retrieves metadata for successfully sent emails."""

    def __init__(self, history_path: str):
        self.history_path = history_path

    def _load_data(self) -> dict[str, list[dict[str, Any]]]:
        try:
            with open(self.history_path, "r", encoding="utf-8") as history_file:
                data = json.load(history_file)
        except FileNotFoundError:
            return {"sent": []}
        except json.JSONDecodeError as error:
            raise HistoryError(f"Invalid history file: {error.msg}") from error
        except OSError as error:
            raise HistoryError(f"Unable to read history: {error}") from error

        if not isinstance(data, dict) or not isinstance(data.get("sent", []), list):
            raise HistoryError("Invalid history format: 'sent' must be a list")
        if "sent" not in data:
            data["sent"] = []

        required_fields = {"sent_at", "recipient", "subject", "attachments", "result"}
        for email in data["sent"]:
            if (
                not isinstance(email, dict)
                or not required_fields.issubset(email)
                or not isinstance(email["attachments"], list)
            ):
                raise HistoryError("Invalid history format: malformed sent email record")
        return data

    def record_sent_email(
        self, recipient: str, subject: str, attachments: list[str]
    ) -> None:
        """Appends metadata for a successfully sent email to persistent history."""
        data = self._load_data()
        data["sent"].append(
            {
                "sent_at": datetime.now(timezone.utc).isoformat(),
                "recipient": recipient,
                "subject": subject,
                "attachments": attachments,
                "result": "success",
            }
        )

        try:
            os.makedirs(os.path.dirname(self.history_path) or ".", exist_ok=True)
            with open(self.history_path, "w", encoding="utf-8") as history_file:
                json.dump(data, history_file, indent=2)
                history_file.write("\n")
        except OSError as error:
            raise HistoryError(f"Unable to save history: {error}") from error

    def get_sent_emails(self) -> list[dict[str, Any]]:
        """Returns sent email records from newest to oldest."""
        return list(reversed(self._load_data()["sent"]))
