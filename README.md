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

## Resources

| Resource | Purpose |
| --- | --- |
| [App Store screenshots](skills/app-store-screenshots/SKILL.md) | 产品介绍研究、真实截图编排、现代视觉设计、多语言、尺寸适配与上传验证。 |
| [上架图片制作说明文档](skills/app-store-screenshots/references/production-guide.zh-CN.md) | 可独立阅读或交给其他 AI 使用的完整流程，包含浅色科技感配方、制作简报和验收标准。 |
| [App Store release](skills/app-store-release/SKILL.md) | 正式版发布、元数据、提审边界与分支收尾。 |
