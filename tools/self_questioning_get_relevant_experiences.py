from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningGetRelevantExperiences(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        task_type = str(self.args.get("task_type", "")).strip()
        if not task_type:
            return self._ok("Error: task_type is required.")
        max_results = int(self.args.get("max_results", 5))
        experiences = self._engine().get_relevant_experiences(task_type, max_results)
        if not experiences:
            return self._ok(f"No relevant experiences found for task type '{task_type}'.")
        lines = [f"Relevant experiences for '{task_type}' ({len(experiences)}):"]
        for i, exp in enumerate(experiences, 1):
            lines.extend([
                f"{i}. {exp.task_description}",
                f"   - outcome: {exp.outcome}",
                f"   - timestamp: {exp.timestamp}",
                f"   - lessons: {', '.join(exp.lessons_learned) if exp.lessons_learned else '(none)'}",
            ])
        return self._ok("\n".join(lines))
