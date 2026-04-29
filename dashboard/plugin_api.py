from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

# Add the parent directory so we can import tools from the plugin
sys.path.append(str(Path(__file__).parent.parent))
import tools

router = APIRouter()

class WidgetConfig(BaseModel):
    widget_id: str
    widget_type: str
    title: str
    config: dict
    col_span: int = 1

@router.get("/workspace/{session_id}")
async def get_workspace(session_id: str):
    """Returns the workspace configuration for a given session."""
    workspace = tools._load_workspace(session_id)
    return workspace

@router.post("/workspace/{session_id}/widget")
async def add_or_update_widget(session_id: str, widget: WidgetConfig):
    """Add or update a widget from the UI directly."""
    args = {
        "session_id": session_id,
        "widget_id": widget.widget_id,
        "widget_type": widget.widget_type,
        "title": widget.title,
        "config": widget.config,
        "col_span": widget.col_span
    }
    result_str = tools.create_widget(args)
    import json
    return json.loads(result_str)

@router.delete("/workspace/{session_id}/widget/{widget_id}")
async def delete_widget(session_id: str, widget_id: str):
    """Remove a widget via API."""
    args = {"session_id": session_id, "widget_id": widget_id}
    result_str = tools.remove_widget(args)
    import json
    return json.loads(result_str)
