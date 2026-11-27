---
name: app-store-release
description: Prepare, complete, or finalize an iOS App Store release, including production configuration, App Store Connect metadata, review authorization boundaries, Git release finalization, and cleanup of release branches and temporary artifacts.
---

# App Store Release

Use this skill when a user asks to release an iOS app to the App Store, continue an existing release toward App Store submission, or finish and clean up a release. It covers project preparation, App Store Connect metadata, submission support, and repository follow-up.

Do not use it for a TestFlight-only build, a single unrelated App Store Connect edit, or a non-iOS App Store distribution workflow.

## Team Release Model

All iOS applications that use this skill follow this release model:

- `develop` is the beta line. Beta builds use `*` in their display name and `.beta` in their bundle identifier, with corresponding beta or test service and storage configuration where applicable.
- `release/x.y` is the temporary production-release branch. Before building or uploading from it, remove the beta markers and use the production configuration.
- `main` receives the released production state. After release finalization, `develop` keeps the released code but restores its beta-only configuration by reverting only the production-configuration commit.
- A project may have no widget. When it does, the widget must use the same environment-specific identifier convention as its parent app: the beta widget belongs to the beta parent identifier, and the production widget belongs to the production parent identifier.

Before changing source, configuration, App Store Connect, or Git state, inspect the target project's release instructions and current repository state. Confirm:

- the target version and the expected `release/x.y` branch;
- the app target and every shipped extension or companion target;
- the project-specific source of its beta and production configuration;
- the configured build or archive validation command; and
- which actions the user has authorized for this release.

Do not assume the configuration-file layout, the exact beta service or storage settings, or that an extension exists. Preserve unrelated working-tree changes and do not treat a clean tree as implicit.

Track the branches, worktrees, and temporary files or directories created for this release, including those created outside the repository. Prefer a dedicated temporary directory for disposable build output, logs, downloads, and metadata drafts so cleanup can identify them reliably. Record any artifacts the user asks to keep.

## Prepare The Production Build

Read the actual project configuration before editing it. Change the smallest shared configuration source that correctly affects the release, following project conventions.

On `release/x.y`, check the release version and all user-visible and distribution-critical settings that apply to the project, such as:

- marketing and build versions;
- bundle identifiers without `.beta`, including parent-child identifier relationships;
- display names and localized names without `*`;
- production service or storage configuration instead of beta or test configuration; and
- target membership and signing or export configuration required by the project's archive process.

If the project includes a widget, verify that its production identifier matches the production parent-app namespace. Verify that all shipped targets form a coherent production build.

Run the project's prescribed local build or archive validation after configuration changes and before App Store Connect work. If validation is blocked by the local environment, report the exact limitation and the configuration evidence already checked; do not claim the build is verified.

## App Store Connect

When the user has made App Store Connect access available, inspect the target app and version record before editing. Confirm the intended build and the metadata required for that version.

For each supported locale:

- read the existing fields before changing them;
- update release notes and Promotional Text when they are part of the requested release;
- save the locale; and
- reread the saved fields to confirm the update persisted.

Only update descriptions, screenshots, review notes, age ratings, pricing, availability, or other unrelated metadata when the user asks for it or the version record requires it.

Write release notes in the product's established voice. Emphasize user-visible improvements, keep claims supportable, and adapt each language naturally rather than translating word for word. Review prior published notes when the user asks to continue an existing style.

Uploading a build, adding a version to review, submitting it for review, and releasing it are external state changes. Perform each only when the user's request explicitly includes that action. Otherwise, stop after preparation and state the remaining action clearly.

## Repository Follow-Up

Run release finalization and cleanup when either condition applies:

- The user explicitly asks to finish, wrap up, or clean up the release, including requests such as “收尾”, “结束发布”, or “清理发布分支”.
- The requested release workflow has reached its agreed App Store endpoint and the build has been confirmed. For a submission workflow, this means successful submission for review; wait for public availability only when that is the requested endpoint.

An end-to-end release request includes this repository finalization and cleanup once that endpoint is reached. Do not require a second request to delete the release branch or remove disposable artifacts. A request limited to preparation, metadata, or inspection does not authorize an App Store submission or expand into a full release. An explicit cleanup request authorizes cleanup of completed release work, not an unrequested submission, release, or merge of unfinished work.

Inspect local and remote refs and the previous completed release before making changes. Determine the established tag format from the release history, not a truncated list or a single exceptional tag. Identify the production-configuration commit and avoid reverting feature or fix commits. Resume from the actual state: do not repeat completed merges, create duplicate tags, or change an existing correct tag.

1. Merge `release/x.y` into `main`.
2. Point the release tag directly at that existing production-release merge commit on `main`, using the repository's established version format (commonly `vX.Y`). Do not create an empty commit just for the tag, or point it at a later beta-restoration commit. Verify that its tree matches the released source.
3. Merge or fast-forward `main` into `develop` so the production-release merge commit and its tag are included in `develop`'s history as well.
4. Revert only the production-configuration commit on `develop` so its `*`, `.beta`, and related beta configuration return.
5. Push `main`, `develop`, and the tag, then verify the remote refs.
6. Complete the cleanup below unless the user explicitly asks to retain particular branches or artifacts.

### Cleanup Scope And Completion

Treat cleanup as part of finalization, not an optional offer after reporting the release complete:

- Remove the finished local and remote `release/x.y` branch and any other temporary branches created for this release after verifying their required changes are included in the retained release history. Preserve the release tag. Do not infer that every historical `release/*` branch or similarly named file belongs to this release.
- Remove temporary worktrees created for this release after their changes are integrated or preserved. Use the environment's managed-worktree archive mechanism when available. Switch the primary checkout to `develop` before deleting its release branch.
- Remove disposable release output created by this task, such as temporary build or DerivedData directories, exported upload copies, downloaded diagnostic files, scratch scripts, logs, and metadata drafts, wherever the task created them. Preserve source files, reusable screenshot artwork, requested deliverables, and the final release record or submission evidence. Do not delete the sole retained signed archive or symbols needed to reproduce or diagnose the release.
- Clean only artifacts attributable to this release. Inspect uncertain or modified artifacts before deleting them; preserve unmerged work and user-created files. Do not use a repository-wide clean, a broad wildcard deletion, or history rewriting as a cleanup shortcut.

Before declaring finalization complete, verify that `main` and its remote contain the production release, the remote tag points to the intended existing commit, `develop` and its remote include that commit and retain beta configuration, and the finished release branches are absent locally and remotely. Check for remaining task-created worktrees and disposable files, and confirm that the working tree has no changes introduced by this task.

If a specific artifact cannot be safely removed or an operation fails, complete the independent cleanup and report the exact remaining item and reason. Do not silently retain release branches or temporary output, or describe partial cleanup as complete.

## Bear.Best Website Changelog Sync

After a production release is finalized (not for preparation-only runs or TestFlight builds), update the product's changelog in the local `Bear.Best` website repository:

1. **Locate `Bear.Best` dynamically** (do not hardcode an absolute path): search relative to the current repository root across sibling directories and up to two directory levels above or below (e.g., `../Bear.Best`, `../../Bear.Best`, or nearby directories) for a repository containing both `src/data/productChangelog.ts` and `.ctxpm/packages/skills/add-product-changelog/SKILL.md`.
2. **Verify product registration**: inspect `src/data/productChangelog.ts` in `Bear.Best` to confirm the current app is registered. If the product is not registered yet, note that in the completion report and skip without modifying `productChangelog.ts`.
3. **Follow `Bear.Best`'s `add-product-changelog` skill**: read and follow `<Bear.Best>/.ctxpm/packages/skills/add-product-changelog/SKILL.md` using the released version and the finalized release notes from this release. Keep `Bear.Best`'s review and confirmation gate intact before committing, cherry-picking to `main`, and pushing.
4. If the local `Bear.Best` repository cannot be found, or if its working tree/branch state blocks the update, report the exact reason in the completion report instead of failing the app release.

## Completion Report

Summarize only the release facts that were verified:

- version, branch, and production-build validation result;
- App Store Connect metadata and build status;
- whether review submission or release was actually performed;
- repository refs pushed, the tag's target commit, configuration restored, release branches removed, and temporary artifacts cleaned or explicitly retained; and
- `Bear.Best` website changelog sync status (updated/pushed, awaiting confirmation, skipped because unregistered, or blocked with reason).

Separate local preparation from changes already made in App Store Connect or the remote repository. Name any remaining manual confirmation or authorization.
