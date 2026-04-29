(async function () {
    "use strict";
    
    const SDK = window.__HERMES_PLUGIN_SDK__;
    const { React } = SDK;
    
    let Tremor = {};
    try {
        Tremor = await import('https://esm.sh/@tremor/react@3.14.0?external=react,react-dom');
    } catch (e) {
        console.error("Failed to load Tremor:", e);
    }
    
    function WorkspacePage() {
        const [session_id, setSessionId] = SDK.hooks.useState("default");
        const [workspace, setWorkspace] = SDK.hooks.useState({ widgets: [] });

        SDK.hooks.useEffect(() => {
            let interval;
            const fetchWorkspace = () => {
                SDK.fetchJSON(`/api/plugins/dynamic-dashboard/workspace/${session_id}`)
                    .then((data) => setWorkspace(data))
                    .catch((err) => console.error("Failed to fetch workspace:", err));
            };
            
            fetchWorkspace();
            interval = setInterval(fetchWorkspace, 5000);
            return () => clearInterval(interval);
        }, [session_id]);
        
        // Recursive JSON-to-React Renderer
        const renderNode = (node, index = 0) => {
            if (typeof node === "string" || typeof node === "number") return node;
            if (!node || typeof node !== "object") return null;

            // Map standard HTML tags or Tremor components
            const Component = Tremor[node.type] || node.type;
            const props = { ...node.props, key: index };
            
            const children = Array.isArray(node.children) 
                ? node.children.map((child, i) => renderNode(child, i))
                : [];
                
            // If there are no children, don't pass an empty array to createElement (some components might not like it)
            if (children.length > 0) {
                return React.createElement(Component, props, ...children);
            } else {
                return React.createElement(Component, props);
            }
        };

        const renderWidget = (widget) => {
            const { widget_id, config, col_span } = widget;
            
            const widthClass = col_span === 4 ? "w-full" :
                               col_span === 3 ? "w-3/4" :
                               col_span === 2 ? "w-1/2" :
                               col_span === 1 ? "w-1/4" : "flex-1";

            // If the config is a valid generic node, render it. 
            // Otherwise show a fallback.
            let content;
            if (config && config.type) {
                content = renderNode(config);
            } else {
                content = React.createElement("div", { className: "p-4 border rounded shadow-sm bg-card text-card-foreground" },
                    React.createElement("h3", { className: "font-semibold text-lg" }, "Invalid Widget Config"),
                    React.createElement("pre", { className: "text-xs mt-2 overflow-auto" }, JSON.stringify(config, null, 2))
                );
            }

            return React.createElement("div", { 
                key: widget_id, 
                className: `p-2 ${widthClass} min-w-[300px] flex-grow`
            }, content);
        };

        return React.createElement("div", { className: "p-6 flex flex-col h-full space-y-4" },
            React.createElement("div", { className: "flex justify-between items-center" },
                React.createElement("h1", { className: "text-2xl font-bold" }, "Workspace"),
                React.createElement("div", { className: "text-sm text-muted-foreground" }, "Session: ", session_id)
            ),
            
            React.createElement("div", { className: "flex flex-wrap -m-2 items-stretch" },
                workspace.widgets.map(renderWidget),
                workspace.widgets.length === 0 && React.createElement("div", { className: "p-4 text-muted-foreground w-full text-center" }, "No widgets yet. Ask the AI to build your dashboard!")
            )
        );
    }
    
    window.__HERMES_PLUGINS__.register("dynamic-dashboard", WorkspacePage);
})();
