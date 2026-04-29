# Hermes Plugin Template

This is a template repository for building [Hermes Agent](https://hermes-agent.nousresearch.com/) plugins. It includes the necessary boilerplate structure to add custom tools, hooks, and skills to the Hermes ecosystem.

## Directory Structure

- `plugin.yaml`: The manifest file defining the plugin metadata, tools, and hooks.
- `__init__.py`: The entry point where tools and hooks are registered into Hermes.
- `schemas.py`: Contains the JSON schemas for the tools (what the LLM reads to understand the tool).
- `tools.py`: Contains the Python implementation of the tools (the logic that runs).
- `skills/`: A directory for bundled skills.
  - `example-skill/SKILL.md`: An example of a skill bundled within the plugin.

## Getting Started

1. **Clone the repository** (or generate from this template)
2. **Rename the plugin**: Update the name in `plugin.yaml` and any relevant namespaces.
3. **Add your logic**:
   - Write your tool implementations in `tools.py`.
   - Define the corresponding JSON schema in `schemas.py`.
   - Register them in the `register(ctx)` function in `__init__.py`.

## Installation

You can install this plugin locally for testing by either:

1. Copying or symlinking this directory into `~/.hermes/plugins/`:
   ```bash
   ln -s $(pwd) ~/.hermes/plugins/example-plugin
   ```
2. Or by enabling project-local plugins in your environment:
   ```bash
   export HERMES_ENABLE_PROJECT_PLUGINS=true
   # Assumes this template is cloned to .hermes/plugins/ inside a larger project
   ```

## Managing Plugins

Once you publish your plugin as a Git repository, users can install and manage it using the Hermes CLI:

```bash
hermes plugins                                # unified interactive UI
hermes plugins list                           # table: enabled / disabled / not enabled
hermes plugins install user/repo              # install from Git, then prompt Enable? [y/N]
hermes plugins install user/repo --enable     # install AND enable (no prompt)
hermes plugins install user/repo --no-enable  # install but leave disabled (no prompt)
hermes plugins update my-plugin               # pull latest
hermes plugins remove my-plugin               # uninstall
hermes plugins enable my-plugin               # add to allow-list
hermes plugins disable my-plugin              # remove from allow-list + add to disabled
```

By default, newly installed plugins are disabled. You must explicitly enable them using the UI or the `enable` command.

## Creating Skills

Plugins can bundle skills within the `skills/` directory. They are registered automatically by the `__init__.py` script. The agent can then access them using the namespace:

```
skill_view("example-plugin:example-skill")
```

For more details on plugin development, consult the [official Hermes Plugin documentation](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin).
