---
name: tremor-dashboard
description: Guidelines and patterns for creating completely autonomous, dynamic dashboard widgets using Tremor React components.
---

# Tremor Dashboard Skill

This skill empowers you (the AI) to be fully autonomous in designing, rendering, and monitoring data for the `dynamic-dashboard` plugin. You do not need the user to micromanage you. When asked a high-level prompt like "Trade Crypto" or "Portfolio Management", you must design a complete dashboard on your own.

## The Bento Grid & Component Rendering

The dashboard uses a Flex Bento grid. You can control the size of widgets using the `col_span` parameter in `create_widget`:
- `col_span: 1` -> 1/4 width (small widgets like metrics)
- `col_span: 2` -> 1/2 width (medium charts)
- `col_span: 3` -> 3/4 width (large charts)
- `col_span: 4` -> full width (hero widgets or wide tables)

## Fully Dynamic JSON Rendering

The `config` parameter for `create_widget` is a **generic React Tree mapping** to Tremor components or HTML tags. You have the power to nest any components you want.

**Supported Components:**
You can use ANY component from `@tremor/react`. It is critical to know that **ALL Tremor charts** are available.
Here is a complete list of common components you can use as the `type`:
- **Charts:** `AreaChart`, `BarChart`, `LineChart`, `DonutChart`, `ScatterChart`, `SparkAreaChart`, `SparkBarChart`, `SparkLineChart`
- **Data Display:** `Metric`, `Table`, `TableHead`, `TableRow`, `TableHeaderCell`, `TableBody`, `TableCell`, `List`, `ListItem`, `Tracker`, `ProgressBar`, `MarkerBar`, `DeltaBar`
- **Layout/Containers:** `Card`, `Grid`, `Col`, `Flex`
- **Typography:** `Title`, `Text`, `Subtitle`, `Bold`, `Italic`
- **Standard HTML:** `div`, `span`, `p`, etc. 

**Config Schema Example:**
```json
{
  "type": "Card",
  "props": { "className": "p-4 space-y-4" },
  "children": [
    {
      "type": "Title",
      "children": ["Portfolio Value"]
    },
    {
      "type": "Metric",
      "children": ["$142,500"]
    },
    {
      "type": "LineChart",
      "props": {
        "data": [
          { "date": "Jan 22", "value": 2890 },
          { "date": "Feb 22", "value": 2756 }
        ],
        "index": "date",
        "categories": ["value"],
        "colors": ["indigo"],
        "className": "h-72 mt-4"
      }
    }
  ]
}
```

## Creating Automated Background Jobs

Widgets are useless without live data. You MUST automatically create cron jobs to fetch and push data to your widgets.
1. Use the `schedule_monitoring_job` tool.
2. Supply the `python_code`. The plugin saves this code and executes it.
3. Your python code MUST import `update_widget_config` from `dynamic_dashboard_sdk` to push new data to the UI.

**Example Python Script:**
```python
import random
from dynamic_dashboard_sdk import update_widget_config

# Assume session_id and widget_id are passed as args or hardcoded
session_id = "CURRENT_SESSION_ID"
widget_id = "portfolio_chart"

# Fetch your data here...
new_value = random.randint(1000, 5000)

# Reconstruct the widget's config JSON tree with the new data
new_config = {
    "type": "Card",
    "children": [
        {"type": "Title", "children": ["Live Metric"]},
        {"type": "Metric", "children": [f"${new_value}"]}
    ]
}

# Push update to the dashboard
update_widget_config(session_id, widget_id, new_config)
```

## Autonomous Orchestration Example

If the user says **"Market Report for AI"**:
1. You autonomously call `create_widget` multiple times to build a `col_span: 4` Title card, a `col_span: 2` LineChart for AI stock indices, and a `col_span: 2` DonutChart for sentiment analysis.
2. You autonomously call `schedule_monitoring_job` for each widget, providing the exact python logic to fetch the latest market data from Yahoo Finance or Twitter, and format it into the generic JSON tree for `update_widget_config`.
3. You inform the user that the dashboard is live and data is streaming.
