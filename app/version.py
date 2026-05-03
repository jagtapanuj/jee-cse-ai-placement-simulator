from __future__ import annotations

APP_VERSION = "maharashtra-local-beta-v1"
DATA_VERSION = "maharashtra-pilot-dataset-v1"
DATA_SCOPE = "Maharashtra-only CSE/IT/AI/DS local beta"
DEFAULT_VISIBILITY_RULE = "Only publish_default=yes rows are visible by default."


def version_payload() -> dict:
    return {
        "status": "ok",
        "app_version": APP_VERSION,
        "data_version": DATA_VERSION,
        "data_scope": DATA_SCOPE,
        "default_visibility_rule": DEFAULT_VISIBILITY_RULE,
    }
