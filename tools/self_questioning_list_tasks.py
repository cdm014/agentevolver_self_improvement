from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningListTasks(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        tasks = self._engine().tasks
        completed = self.args.get("completed", None)
        category = self.args.get("category", None)
        if completed is not None:
            want = completed if isinstance(completed, bool) else str(completed).lower() == 'true'
            tasks = [t for t in tasks if t.completed == want]
        if category is not None:
            tasks = [t for t in tasks if t.category == category]
        if not tasks:
            return self._ok("No tasks found matching the filters.")
        lines = [f"Tasks ({len(tasks)}):"]
        for t in tasks:
            lines.extend([
                f"- {t.task_id}",
                f"  description: {t.description}",
                f"  category: {t.category}",
                f"  difficulty: {t.difficulty}",
                f"  completed: {t.completed}",
                f"  score: {t.score}",
            ])
        return self._ok("\n".join(lines))
