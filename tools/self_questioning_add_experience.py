from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningAddExperience(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        task_type = str(self.args.get("task_type", "")).strip()
        task_description = str(self.args.get("task_description", "")).strip()
        actions = self.args.get("actions", [])
        outcome = str(self.args.get("outcome", "")).strip()
        lessons_learned = self.args.get("lessons_learned", [])
        metadata = self.args.get("metadata", {}) or {}

        if not task_type or not task_description or not outcome:
            return self._ok("Error: task_type, task_description, and outcome are required.")
        if not isinstance(actions, list) or not isinstance(lessons_learned, list):
            return self._ok("Error: actions and lessons_learned must be lists.")

        exp = self._engine().add_experience(
            task_type=task_type,
            task_description=task_description,
            actions=[str(x) for x in actions],
            outcome=outcome,
            lessons_learned=[str(x) for x in lessons_learned],
            metadata=metadata if isinstance(metadata, dict) else {},
        )
        return self._ok(
            f"Added experience:\n"
            f"- task_type: {exp.task_type}\n"
            f"- outcome: {exp.outcome}\n"
            f"- timestamp: {exp.timestamp}\n"
            f"- lessons_learned: {exp.lessons_learned}"
        )
