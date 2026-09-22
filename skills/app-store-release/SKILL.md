---
name: app-store-release
description: Prepare and complete a conventional iOS App Store release, including project release checks, App Store Connect metadata, review authorization boundaries, and repository release follow-up.
---

# App Store Release

Use this skill when a user asks to release an iOS app to the App Store, or to continue an existing release toward App Store submission. It covers project preparation, App Store Connect metadata, submission support, and repository follow-up.

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

After the user confirms the build and the requested App Store submission stage is complete, finish the release using the team model. Inspect the commit history first to identify the production-configuration commit and avoid reverting feature or fix commits.

1. Merge `release/x.y` into `main`.
2. Tag the release using the repository's established version format.
3. Merge or fast-forward the release work into `develop`.
4. Revert only the production-configuration commit on `develop` so its `*`, `.beta`, and related beta configuration return.
5. Push `main`, `develop`, and the tag, then verify the remote refs.
6. Delete the finished local and remote `release/x.y` branch unless the user asks to retain it.

Pushing refs, deleting local or remote branches, and creating tags change shared repository state. Do these only when the user has requested the corresponding release finalization.

## Completion Report

Summarize only the release facts that were verified:

- version, branch, and production-build validation result;
- App Store Connect metadata and build status;
- whether review submission or release was actually performed; and
- repository refs pushed, configuration restored, and release branches retained or removed.

Separate local preparation from changes already made in App Store Connect or the remote repository. Name any remaining manual confirmation or authorization.
