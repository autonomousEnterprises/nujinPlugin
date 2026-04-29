import json
from pathlib import Path

WORKSPACES_DIR = Path(__file__).parent / "workspaces"

def update_widget_config(session_id: str, widget_id: str, new_config: dict):
    """
    Update a widget's config. Use this in your cron scripts to push new data to the dashboard.
    """
    workspace_path = WORKSPACES_DIR / f"{session_id}.json"
    if not workspace_path.exists():
        return
        
    with open(workspace_path, "r", encoding="utf-8") as f:
        workspace = json.load(f)
        
    for widget in workspace.get("widgets", []):
        if widget.get("widget_id") == widget_id:
            widget["config"] = new_config
            break
            
    with open(workspace_path, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2)
