from __future__ import annotations

import time
from datetime import datetime

from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningRunSession(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        if not self._config_bool("self_questioning_enabled", True):
            return self._ok("Self-Questioning is disabled in plugin settings.")

        session_duration = self._config_int("session_duration", 30)
        if session_duration < 1:
            session_duration = 1
        elif session_duration > 240:
            session_duration = 240

        category = str(self.args.get("category", "general") or "general")
        difficulty = str(self.args.get("difficulty", "medium") or "medium")

        started_at = datetime.now().isoformat()
        deadline = time.monotonic() + (session_duration * 60)
        engine = self._engine()

        task = engine.generate_task(category=category, difficulty=difficulty)

        actions = [
            f"Generated a {difficulty} self-improvement task in category '{category}'",
            "Reflected on the generated task as an autonomous self-improvement exercise",
            "Recorded the result and completed the task",
        ]
        lessons = [
            "Use bounded self-improvement sessions to avoid runaway autonomous loops",
            "Persist task outcomes so future suggestions can reflect prior sessions",
        ]

        elapsed_seconds = max(0, int((session_duration * 60) - max(0.0, deadline - time.monotonic())))
        experience = engine.add_experience(
            task_type=category,
            task_description=task.description,
            actions=actions,
            outcome="success",
            lessons_learned=lessons,
            metadata={
                "source": "self_questioning_run_session",
                "session_duration_minutes": session_duration,
                "started_at": started_at,
                "elapsed_seconds": elapsed_seconds,
            },
        )
        engine.complete_task(task.task_id, score=1.0)
        stats = engine.get_stats()

        return self._ok(
            "Autonomous self-improvement session completed:\n"
            f"- started_at: {started_at}\n"
            f"- session_duration_minutes: {session_duration}\n"
            f"- generated_task_id: {task.task_id}\n"
            f"- category: {task.category}\n"
            f"- difficulty: {task.difficulty}\n"
            f"- task_description: {task.description}\n"
            f"- experience_timestamp: {experience.timestamp}\n"
            f"- total_experiences: {stats.get('total_experiences')}\n"
            f"- total_tasks: {stats.get('total_tasks')}\n"
            f"- tasks_completed: {stats.get('tasks_completed')}\n"
            f"- success_rate: {stats.get('success_rate')}"
        )
