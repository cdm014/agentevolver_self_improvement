from helpers.tool import Response
from usr.plugins.agentevolver_self_improvement.tools._base import SelfImprovementBaseTool


class SelfQuestioningAnalyzeActions(SelfImprovementBaseTool):
    async def execute(self, **kwargs) -> Response:
        actions = self.args.get("actions", [])
        outcomes = self.args.get("outcomes", [])
        if not isinstance(actions, list) or not isinstance(outcomes, list):
            return self._ok("Error: actions and outcomes must be lists.")
        scores = self._engine().analyze_actions([str(x) for x in actions], [str(x) for x in outcomes])
        lines = ["Action analysis:"]
        for action, score in scores.items():
            lines.append(f"- {action}: {score}")
        return self._ok("\n".join(lines))
