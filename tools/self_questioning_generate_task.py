from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningGenerateTask(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        if not self._config_bool("self_questioning_enabled", True):
            return self._ok("Self-Questioning is disabled in plugin settings.")

        category = str(self.args.get("category", "general"))
        difficulty = str(self.args.get("difficulty", "medium"))
        task = self._engine().generate_task(category=category, difficulty=difficulty)
        return self._ok(
            f"Generated task:\n"
            f"- task_id: {task.task_id}\n"
            f"- category: {task.category}\n"
            f"- difficulty: {task.difficulty}\n"
            f"- description: {task.description}\n"
            f"- created_at: {task.created_at}"
        )
