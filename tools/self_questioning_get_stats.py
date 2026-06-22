from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningGetStats(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        stats = self._engine().get_stats()
        lines = ["Self-improvement statistics:"]
        for key, value in stats.items():
            lines.append(f"- {key}: {value}")
        return self._ok("\n".join(lines))
