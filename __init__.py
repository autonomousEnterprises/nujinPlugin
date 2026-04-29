"""Dynamic Dashboard Plugin — registration."""
import logging
from pathlib import Path
from . import schemas, tools

logger = logging.getLogger(__name__)

def _on_session_start(session_id, **kwargs):
    """Hook: runs when a new session starts. Initialize the dashboard state if it doesn't exist."""
    logger.debug("Session started: %s - initializing workspace", session_id)
    tools.init_workspace(session_id)

def register(ctx):
    """Wire schemas to handlers, register hooks, and load skills."""
    
    # 1. Register tools
    ctx.register_tool(
        name="create_widget",
        toolset="dynamic-dashboard",
        schema=schemas.CREATE_WIDGET,
        handler=tools.create_widget
    )

    ctx.register_tool(
        name="remove_widget",
        toolset="dynamic-dashboard",
        schema=schemas.REMOVE_WIDGET,
        handler=tools.remove_widget
    )
    
    ctx.register_tool(
        name="schedule_monitoring_job",
        toolset="dynamic-dashboard",
        schema=schemas.SCHEDULE_MONITORING_JOB,
        handler=tools.schedule_monitoring_job
    )

    # 2. Register hooks
    ctx.register_hook("on_session_start", _on_session_start)
    
    # 3. Register bundled skills
    skills_dir = Path(__file__).parent / "skills"
    if skills_dir.exists() and skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                ctx.register_skill(child.name, skill_md)
