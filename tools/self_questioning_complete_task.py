from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningCompleteTask(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        task_id = str(self.args.get("task_id", "")).strip()
        if not task_id:
            return self._ok("Error: task_id is required.")
        score = float(self.args.get("score", 1.0))
        ok = self._engine().complete_task(task_id, score)
        if not ok:
            return self._ok(f"Task not found: {task_id}")
        return self._ok(f"Task completed: {task_id} with score {score}")
