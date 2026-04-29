"""Tool handlers — the code that runs when the LLM calls each tool."""
import json
import logging

logger = logging.getLogger(__name__)

def example_tool(args: dict, **kwargs) -> str:
    """An example tool implementation.
    
    Rules for handlers:
    1. Receive args (dict) — the parameters the LLM passed
    2. Do the work
    3. Return a JSON string — ALWAYS, even on error
    4. Accept **kwargs for forward compatibility
    """
    name = args.get("name", "").strip()
    message = args.get("message", "").strip()
    
    if not name:
        return json.dumps({"error": "No name provided"})
        
    try:
        greeting = f"Hello, {name}! Welcome to the Hermes Plugin System."
        if message:
            greeting += f" You also said: '{message}'"
            
        logger.info(f"example_tool called for {name}")
        
        return json.dumps({
            "status": "success",
            "greeting": greeting,
            "source": "example-plugin"
        })
    except Exception as e:
        return json.dumps({"error": f"Tool execution failed: {e}"})
