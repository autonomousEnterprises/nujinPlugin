"""Tool schemas — what the LLM sees."""

EXAMPLE_TOOL = {
    "name": "example_tool",
    "description": (
        "An example tool that returns a friendly greeting and repeats the provided input. "
        "Use this tool to verify that the example-plugin is functioning correctly."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the user or entity to greet.",
            },
            "message": {
                "type": "string",
                "description": "An optional message to repeat back.",
            },
        },
        "required": ["name"],
    },
}
