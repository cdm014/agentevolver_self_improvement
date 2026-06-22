from __future__ import annotations

import asyncio
from typing import Any

from helpers.localization import Localization
from helpers.task_scheduler import SchedulerTaskList, ScheduledTask, TaskSchedule, TaskState

PLUGIN_NAME = "agentevolver_self_improvement"
TASK_NAME = f"{PLUGIN_NAME}_auto_session"
DEFAULT_FREQUENCY_MINUTES = 60
MIN_FREQUENCY_MINUTES = 5
MAX_FREQUENCY_MINUTES = 1440
DEFAULT_TIMEZONE = "America/New_York"


def _run(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.run(coro)
    if loop.is_running():
        return loop.run_until_complete(coro)
    return loop.run_until_complete(coro)


def _config_bool(config: dict[str, Any], key: str, default: bool = False) -> bool:
    value = config.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _config_int(config: dict[str, Any], key: str, default: int, minimum: int | None = None, maximum: int | None = None) -> int:
    value = config.get(key, default)
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    if minimum is not None and parsed < minimum:
        parsed = minimum
    if maximum is not None and parsed > maximum:
        parsed = maximum
    return parsed


def scheduled_task_name(agent_profile: str = "") -> str:
    profile = str(agent_profile or "default").strip() or "default"
    return f"{TASK_NAME}_{profile}"


def build_schedule_from_frequency(minutes: int, timezone: str | None = None) -> TaskSchedule:
    normalized = max(MIN_FREQUENCY_MINUTES, min(MAX_FREQUENCY_MINUTES, int(minutes)))
    tz = str(timezone or "").strip() or Localization.get().get_timezone() or DEFAULT_TIMEZONE

    if normalized % 60 == 0:
        hours = max(1, normalized // 60)
        if 24 % hours == 0:
            return TaskSchedule(minute="0", hour=f"*/{hours}", day="*", month="*", weekday="*", timezone=tz)

    if normalized < 60 and 60 % normalized == 0:
        return TaskSchedule(minute=f"*/{normalized}", hour="*", day="*", month="*", weekday="*", timezone=tz)

    return TaskSchedule(minute="*/5", hour="*", day="*", month="*", weekday="*", timezone=tz)


def build_prompt(session_duration: int) -> str:
    return (
        "Use the AgentEvolver self-improvement plugin to improve yourself. "
        "Run exactly one autonomous self-improvement session with the "
        f"self_questioning_run_session tool using a duration budget of {session_duration} minutes. "
        "Record the experience, complete any generated task, and summarize what you learned."
    )


def build_system_prompt() -> str:
    return "Run the plugin's autonomous self-improvement session exactly once and report the result."


def find_existing_task(agent_profile: str = ""):
    scheduler = SchedulerTaskList.get()
    return scheduler.get_task_by_name(scheduled_task_name(agent_profile))


def _ensure_scheduled_task_sync(config: dict[str, Any], agent_profile: str = "", project_name: str = "") -> str:
    scheduler = SchedulerTaskList.get()
    name = scheduled_task_name(agent_profile)
    enabled = _config_bool(config, "auto_schedule", False)
    frequency = _config_int(config, "task_generation_frequency", DEFAULT_FREQUENCY_MINUTES, MIN_FREQUENCY_MINUTES, MAX_FREQUENCY_MINUTES)
    session_duration = _config_int(config, "session_duration", 30, 1, 240)
    timezone = Localization.get().get_timezone() or DEFAULT_TIMEZONE
    existing = scheduler.get_task_by_name(name)

    if not enabled:
        if existing:
            scheduler.tasks = [task for task in scheduler.get_tasks() if task.name != name]
            _run(scheduler.save())
            return "removed"
        return "absent"

    schedule = build_schedule_from_frequency(frequency, timezone=timezone)
    prompt = build_prompt(session_duration)
    system_prompt = build_system_prompt()

    if existing:
        _run(scheduler.update_task(existing.uuid, schedule=schedule, prompt=prompt, system_prompt=system_prompt, state=TaskState.IDLE))
        _run(scheduler.save())
        return "updated"

    task = ScheduledTask.create(
        name=name,
        system_prompt=system_prompt,
        prompt=prompt,
        schedule=schedule,
        project_name=project_name or None,
    )
    _run(scheduler.add_task(task))
    return "created"


def ensure_scheduled_task(config: dict[str, Any], agent_profile: str = "", project_name: str = "") -> str:
    return _ensure_scheduled_task_sync(config=config, agent_profile=agent_profile, project_name=project_name)


def remove_scheduled_task(agent_profile: str = "") -> bool:
    scheduler = SchedulerTaskList.get()
    name = scheduled_task_name(agent_profile)
    before = len(scheduler.get_tasks())
    scheduler.tasks = [task for task in scheduler.get_tasks() if task.name != name]
    if len(scheduler.tasks) != before:
        _run(scheduler.save())
        return True
    return False


def sync_scheduler(config: dict[str, Any], agent_profile: str = "", project_name: str = "") -> str:
    return ensure_scheduled_task(config=config, agent_profile=agent_profile, project_name=project_name)
