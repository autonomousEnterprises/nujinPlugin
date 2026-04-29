#!/usr/bin/env python3
import sys
import json
import logging
from pathlib import Path

# Provide basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("monitor_script")

# Example usage: python3 monitor_script.py <session_id> <job_id> [extra_args...]

def update_widget_state(session_id: str, widget_id: str, new_data: dict):
    """Utility to update a specific widget's config data."""
    # Assuming the workspaces dir is relative to the plugin directory
    workspaces_dir = Path(__file__).parent / "workspaces"
    workspace_path = workspaces_dir / f"{session_id}.json"
    
    if not workspace_path.exists():
        logger.error(f"Workspace {session_id} not found.")
        return
        
    with open(workspace_path, "r", encoding="utf-8") as f:
        workspace = json.load(f)
        
    for widget in workspace.get("widgets", []):
        if widget.get("widget_id") == widget_id:
            # Update the widget config
            widget["config"].update(new_data)
            logger.info(f"Updated widget {widget_id} for session {session_id}.")
            break
            
    with open(workspace_path, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2)

def main():
    if len(sys.argv) < 3:
        logger.error("Usage: python3 monitor_script.py <session_id> <job_id>")
        sys.exit(1)
        
    session_id = sys.argv[1]
    job_id = sys.argv[2]
    
    logger.info(f"Running monitor job {job_id} for session {session_id}")
    
    # ---------------------------------------------------------
    # YOUR MONITORING LOGIC HERE
    # Example: fetch an API, read a file, etc.
    # For demonstration, we'll just increment a random metric.
    # ---------------------------------------------------------
    import random
    
    # Example: If the job_id matches a widget_id, we update it directly
    # E.g., updating a TremorMetric
    fake_metric_value = random.randint(100, 5000)
    update_widget_state(session_id, job_id, {"value": f"${fake_metric_value}"})
    
    # You could also use Hermes gateway (if accessible) to inject a message:
    # hermes_inject_message(session_id, f"Metric updated to {fake_metric_value}")
    
if __name__ == "__main__":
    main()
