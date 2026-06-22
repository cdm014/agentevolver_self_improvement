from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningGetImprovementSuggestions(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        suggestions = self._engine().get_improvement_suggestions()
        if not suggestions:
            return self._ok("No improvement suggestions right now.")
        return self._ok("Improvement suggestions:\n" + "\n".join(f"- {s}" for s in suggestions))
