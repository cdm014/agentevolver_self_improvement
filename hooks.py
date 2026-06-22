#!/usr/bin/env python3
"""Hooks for AgentEvolver Self-Improvement plugin."""

from __future__ import annotations

import logging
from pathlib import Path

from helpers.plugins import get_default_plugin_config

logger = logging.getLogger(__name__)
PLUGIN_NAME = "agentevolver_self_improvement"


def _normalize_config(config: dict | None) -> dict:
    normalized = dict(get_default_plugin_config(PLUGIN_NAME) or {})
    normalized.update(config or {})
    return normalized


def install():
    """Called after plugin installation."""
    plugin_dir = Path(__file__).parent
    logger.info(f"Installing AgentEvolver Self-Improvement plugin in {plugin_dir}")
    (plugin_dir / "data").mkdir(exist_ok=True)
    (plugin_dir / "logs").mkdir(exist_ok=True)
    logger.info("AgentEvolver Self-Improvement plugin installed successfully")
    return True


def get_plugin_config(default=None, **kwargs):
    return _normalize_config(default)


def save_plugin_config(default=None, settings=None, project_name="", agent_profile="", **kwargs):
    normalized = _normalize_config(settings or default)
    try:
        from usr.plugins.agentevolver_self_improvement.helpers.scheduler import sync_scheduler
        sync_scheduler(normalized, agent_profile=agent_profile or "", project_name=project_name or "")
    except Exception as exc:
        logger.exception("Failed to sync self-improvement scheduler from config save: %s", exc)
    return normalized


def pre_update():
    """Called before plugin update."""
    logger.info("Preparing AgentEvolver Self-Improvement plugin for update")
    return True


def uninstall():
    """Called before plugin removal."""
    try:
        from usr.plugins.agentevolver_self_improvement.helpers.scheduler import remove_scheduled_task
        removed = remove_scheduled_task()
        logger.info("Removed scheduled self-improvement task: %s", removed)
    except Exception as exc:
        logger.exception("Failed to remove scheduled self-improvement task during uninstall: %s", exc)
    return True


def cleanup():
    """Optional cleanup hook (not currently called by framework)."""
    pass
