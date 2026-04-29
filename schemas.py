"""Tool schemas — what the LLM sees."""

CREATE_WIDGET = {
    "name": "create_widget",
    "description": (
        "Creates or updates a widget on the dynamic dashboard. "
        "The `config` MUST be a generic JSON React Tree mapping to Tremor components or HTML tags. "
        "Example: {'type': 'Card', 'props': {'className': 'p-4'}, 'children': [{'type': 'Title', 'children': ['Sales']}, {'type': 'Metric', 'children': ['$10k']}]}"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "The current session ID.",
            },
            "widget_id": {
                "type": "string",
                "description": "A unique identifier for this widget (e.g., 'btc_chart').",
            },
            "config": {
                "type": "object",
                "description": "The generic JSON React tree that defines the UI for this widget.",
            },
            "col_span": {
                "type": "integer",
                "description": "The number of grid columns this widget spans (1 to 4). Defaults to 1.",
            }
        },
        "required": ["session_id", "widget_id", "config"],
    },
}

REMOVE_WIDGET = {
    "name": "remove_widget",
    "description": "Removes a widget from the dynamic dashboard.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "The current session ID.",
            },
            "widget_id": {
                "type": "string",
                "description": "The unique identifier of the widget to remove.",
            }
        },
        "required": ["session_id", "widget_id"],
    },
}

SCHEDULE_MONITORING_JOB = {
    "name": "schedule_monitoring_job",
    "description": (
        "Schedules a background cron job that executes python code. "
        "The python code you provide will be saved to a script and executed on schedule. "
        "The code can import `from dynamic_dashboard_sdk import update_widget_config` to easily update a widget's config JSON tree."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "The current session ID.",
            },
            "job_id": {
                "type": "string",
                "description": "A unique identifier for the cron job.",
            },
            "target_widget_id": {
                "type": "string",
                "description": "The ID of the widget this job intends to update.",
            },
            "python_code": {
                "type": "string",
                "description": "The full python code to execute. Use the SDK to push updates to the dashboard.",
            },
            "cron_expression": {
                "type": "string",
                "description": "The cron expression (e.g., '*/5 * * * *' for every 5 minutes).",
            }
        },
        "required": ["session_id", "job_id", "target_widget_id", "python_code", "cron_expression"],
    },
}
