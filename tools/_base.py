from __future__ import annotations

from pathlib import Path
from typing import Any

from helpers.plugins import get_plugin_config
from helpers.tool import Tool, Response
from usr.plugins.agentevolver_self_improvement.helpers.self_improvement import SelfImprovementEngine


class SelfImprovementBaseTool(Tool):
    PLUGIN_NAME = "agentevolver_self_improvement"

    def _plugin_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def _engine(self) -> SelfImprovementEngine:
        return SelfImprovementEngine(self._plugin_dir(), config=self._config())

    def _config(self) -> dict[str, Any]:
        config = get_plugin_config(self.PLUGIN_NAME, agent=self.agent)
        return config if isinstance(config, dict) else {}

    def _config_bool(self, key: str, default: bool = False) -> bool:
        value = self._config().get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on"}
        return bool(value)

    def _config_int(self, key: str, default: int) -> int:
        value = self._config().get(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _ok(self, message: str) -> Response:
        return Response(message=message, break_loop=False)
