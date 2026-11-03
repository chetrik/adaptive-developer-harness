# Activate selected Harness Skills in Lovable

The generator runs outside Lovable. First review the generated AGENTS.md, Project Instructions and selected Skills together with existing Workspace/Project Instructions. Do not upload private instructions to public GitHub without permission. Resolve contradictions before activation; a matching file hash cannot prove semantic compatibility.

1. With project edit permission, paste project-instructions.md into Project settings → Instructions (limit 10,000 characters). Preserve existing project-specific guidance and review the combined text.
2. Keep the generated root AGENTS.md in the project repository. Lovable documents that it reads this root file; verify actual behavior in your session.
3. An owner/admin imports each selected Skill separately: Workspace settings → Skills → Add → Upload ZIP, or Import from GitHub. Generate one-Skill archives with the generator's package-skills command after approved Apply. Each ZIP has SKILL.md at its root. For GitHub, use the URL of the generated skill's folder containing SKILL.md, not the generator repository root.
4. Check each adh-* Skill appears in the / Skills list. Automatic use is a separate workspace setting; manual invocation still works when automatic use is disabled. Do not enable project-specific automation across other projects without reviewing scope.
5. Invoke the relevant Skill on a harmless task, inspect the actual edit/check outcome, and report discovered, invoked and applied separately. A stored Skill is not proof of correct behavior.
6. Use the GitHub integration to continue in Codex, Claude Code, Cursor or Antigravity. Git authorization is a user/account step. Use inspect-project and Project Handoff after export; database migration and chat/context transfer remain separate.
