# AgentAssets

Shared, source-controlled AI resources for product teams. Resources here are reusable upstream artifacts; consuming projects install them through their own resource manager and keep project-specific rules, credentials, release settings, and product knowledge local.

## Layout

Use one top-level directory per resource type. Add a directory only when it contains a real resource.

```text
skills/<name>/SKILL.md     Reusable task guidance
rules/<name>/RULE.md       Reusable constraints or conventions
specs/<name>/README.md     Reusable product or technical specifications
prompts/<name>/PROMPT.md   Reusable prompt templates
memories/<name>/MEMORY.md  Curated reusable knowledge
mcp/<name>/                Reusable MCP configuration or integration assets
```

Each resource directory is independently versioned by its path. Consumers should reference the resource root, rather than this repository root, so unrelated asset updates do not change their resolved dependency version. For example, the App Store release skill is rooted at `skills/app-store-release`.

Keep assets self-contained and generic. Put product-specific procedures, identifiers, credentials, account state, and local workflow exceptions in the consuming project.
