from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

import importlib.util

# Load the plugin's tools.py explicitly to avoid conflicts with any system 'tools' modules
plugin_dir = Path(__file__).parent.parent
tools_path = plugin_dir / "tools.py"

spec = importlib.util.spec_from_file_location("plugin_tools", str(tools_path))
plugin_tools = importlib.util.module_from_spec(spec)
sys.modules["plugin_tools"] = plugin_tools
spec.loader.exec_module(plugin_tools)

router = APIRouter()

class WidgetConfig(BaseModel):
    widget_id: str
    widget_type: str
    title: str
    config: dict
    col_span: int = 1

@router.get("/workspaces")
async def list_workspaces():
    """Returns a list of all available session IDs that have workspaces."""
    import os
    workspaces_dir = plugin_tools.WORKSPACES_DIR
    if not workspaces_dir.exists():
        return []
    
    sessions = []
    for f in workspaces_dir.glob("*.json"):
        sessions.append(f.stem)
    return sessions

@router.get("/workspace/{session_id}")
async def get_workspace(session_id: str):
    """Returns the workspace configuration for a given session."""
    workspace = plugin_tools._load_workspace(session_id)
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
    result_str = plugin_tools.create_widget(args)
    import json
    return json.loads(result_str)

@router.delete("/workspace/{session_id}/widget/{widget_id}")
async def delete_widget(session_id: str, widget_id: str):
    """Remove a widget via API."""
    args = {"session_id": session_id, "widget_id": widget_id}
    result_str = plugin_tools.remove_widget(args)
    import json
    return json.loads(result_str)
