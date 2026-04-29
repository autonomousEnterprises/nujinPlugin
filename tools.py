import json
import logging
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)

PLUGIN_DIR = Path(__file__).parent
WORKSPACES_DIR = PLUGIN_DIR / "workspaces"
SCRIPTS_DIR = PLUGIN_DIR / "scripts"

def _get_workspace_path(session_id: str) -> Path:
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
    return WORKSPACES_DIR / f"{session_id}.json"

def _load_workspace(session_id: str) -> dict:
    path = _get_workspace_path(session_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"widgets": []}

def _save_workspace(session_id: str, data: dict):
    path = _get_workspace_path(session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def init_workspace(session_id: str):
    path = _get_workspace_path(session_id)
    if not path.exists():
        _save_workspace(session_id, {"widgets": []})

def create_widget(args: dict, **kwargs) -> str:
    session_id = args.get("session_id")
    if not session_id:
        return json.dumps({"error": "session_id is required"})
        
    widget_id = args.get("widget_id")
    config = args.get("config", {})
    col_span = args.get("col_span", 1)
    
    workspace = _load_workspace(session_id)
    
    found = False
    for widget in workspace["widgets"]:
        if widget["widget_id"] == widget_id:
            widget["config"] = config
            widget["col_span"] = col_span
            found = True
            break
            
    if not found:
        workspace["widgets"].append({
            "widget_id": widget_id,
            "config": config,
            "col_span": col_span
        })
        
    _save_workspace(session_id, workspace)
    return json.dumps({"status": "success", "message": f"Widget '{widget_id}' created/updated."})

def remove_widget(args: dict, **kwargs) -> str:
    session_id = args.get("session_id")
    widget_id = args.get("widget_id")
    if not session_id or not widget_id:
        return json.dumps({"error": "session_id and widget_id are required"})
        
    workspace = _load_workspace(session_id)
    original_count = len(workspace["widgets"])
    workspace["widgets"] = [w for w in workspace["widgets"] if w["widget_id"] != widget_id]
    
    if len(workspace["widgets"]) < original_count:
        _save_workspace(session_id, workspace)
        return json.dumps({"status": "success", "message": f"Widget '{widget_id}' removed."})
    return json.dumps({"status": "error", "message": f"Widget '{widget_id}' not found."})

def schedule_monitoring_job(args: dict, **kwargs) -> str:
    session_id = args.get("session_id")
    job_id = args.get("job_id")
    python_code = args.get("python_code")
    cron_expr = args.get("cron_expression")
    
    if not all([session_id, job_id, python_code, cron_expr]):
        return json.dumps({"error": "session_id, job_id, python_code, and cron_expression are required"})
        
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    script_path = SCRIPTS_DIR / f"{session_id}_{job_id}.py"
    
    # Save the script
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(python_code)
        
    # Schedule the job via hermes cron CLI
    # To make sure it can import the SDK, we set PYTHONPATH
    sdk_path = str(PLUGIN_DIR)
    command = ["hermes", "cron", "add", cron_expr, f"PYTHONPATH={sdk_path} python3 {script_path}"]
    
    try:
        result = subprocess.run(" ".join(command), shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return json.dumps({
                "status": "success", 
                "message": f"Job '{job_id}' scheduled. Script saved to {script_path}"
            })
        else:
            return json.dumps({"error": f"Failed to schedule job: {result.stderr}"})
    except Exception as e:
        return json.dumps({"error": f"Exception scheduling job: {str(e)}"})
