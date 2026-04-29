"""Example plugin — registration."""
import logging
from pathlib import Path
from . import schemas, tools

logger = logging.getLogger(__name__)

# Track tool usage via hooks
_call_log = []

def _on_post_tool_call(tool_name, args, result, task_id, **kwargs):
    """Hook: runs after every tool call (not just ours)."""
    _call_log.append({"tool": tool_name, "session": task_id})
    if len(_call_log) > 100:
        _call_log.pop(0)
    logger.debug("Tool called: %s (session %s)", tool_name, task_id)


def register(ctx):
    """Wire schemas to handlers, register hooks, and load skills."""
    
    # 1. Register tools
    ctx.register_tool(
        name="example_tool",
        toolset="example-plugin",
        schema=schemas.EXAMPLE_TOOL,
        handler=tools.example_tool
    )

    # 2. Register hooks
    # This hook fires for ALL tool calls
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    
    # 3. Register bundled skills
    skills_dir = Path(__file__).parent / "skills"
    if skills_dir.exists() and skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                ctx.register_skill(child.name, skill_md)
