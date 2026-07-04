from __future__ import annotations

from typing import Any

from models.outputs import CancelToolResponse, ListModelsResponse, NormalizedToolResponse

ToolResult = NormalizedToolResponse | CancelToolResponse | ListModelsResponse | dict[str, Any]
