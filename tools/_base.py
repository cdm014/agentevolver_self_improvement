from __future__ import annotations

from pathlib import Path

from helpers.tool import Tool, Response
from usr.plugins.agentevolver_self_improvement.helpers.self_improvement import SelfImprovementEngine


class SelfImprovementBaseTool(Tool):
    def _engine(self) -> SelfImprovementEngine:
        plugin_dir = Path(__file__).resolve().parent.parent
        return SelfImprovementEngine(plugin_dir)

    def _ok(self, message: str) -> Response:
        return Response(message=message, break_loop=False)
