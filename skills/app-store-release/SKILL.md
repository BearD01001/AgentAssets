---
name: app-store-release
description: Prepare and complete a conventional iOS App Store release, including project release checks, App Store Connect metadata, review authorization boundaries, and repository release follow-up.
---

# App Store Release

Use this skill when a user asks to release an iOS app to the App Store, or to continue an existing release toward App Store submission. It covers project preparation, App Store Connect metadata, submission support, and repository follow-up.

Do not use it for a TestFlight-only build, a single unrelated App Store Connect edit, or a non-iOS App Store distribution workflow.

## Establish The Release Model

Before changing source, configuration, App Store Connect, or Git state, inspect the target project's release instructions and current repository state. Identify:

- the target version, source branch, and the project's release model;
- the app target and every shipped extension or companion target;
- the project's production versus development or beta configuration mechanism;
- the configured build or archive validation command; and
- which actions the user has authorized for this release.

Do not assume branch names, a Git Flow model, beta suffixes, bundle identifier patterns, store names, or a particular configuration-file layout. Preserve unrelated working-tree changes and do not treat a clean tree as implicit.

## Prepare The Production Build

Read the actual project configuration before editing it. Change the smallest shared configuration source that correctly affects the release, following project conventions.

Check the release version and all user-visible and distribution-critical settings that apply to the project, such as:

- marketing and build versions;
- bundle identifiers and parent-child identifier relationships;
- display names and localized names;
- release, beta, staging, feature-flag, service, or storage configuration; and
- target membership and signing or export configuration required by the project's archive process.

Verify that all shipped targets form a coherent production build. Do not remove a development marker merely because it exists; first establish whether it is intentionally retained for the release model.

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

After the user confirms the build and the requested App Store submission stage is complete, follow the repository's documented release model. Inspect the commit history before choosing a merge, tag, rollback, push, or branch-cleanup operation.

For repositories that use a temporary release branch, the usual sequence is to merge the released work into the stable branch, tag it according to repository convention, bring release fixes back to the development branch, and restore only the development-only configuration that the release required to change. This is a pattern, not a universal command sequence: retain project-specific work that belongs on the development branch.

Pushing refs, deleting local or remote branches, and creating tags change shared repository state. Do these only when the user has requested the corresponding release finalization, and verify remote state afterward.

## Completion Report

Summarize only the release facts that were verified:

- version, branch, and production-build validation result;
- App Store Connect metadata and build status;
- whether review submission or release was actually performed; and
- repository refs pushed, configuration restored, and release branches retained or removed.

Separate local preparation from changes already made in App Store Connect or the remote repository. Name any remaining manual confirmation or authorization.
