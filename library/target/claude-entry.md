# Adaptive Harness for Claude Code

Read AGENTS.md in this project before making changes. It contains the selected workflow, project scope and constraints. Use only relevant adh-* Skills from .claude/skills/; do not install another workflow.

For a small change: clarify the intended behavior, make the smallest useful change, run the project's real tests and explain the result. Use existing user authorization; ask again only for changed scope or additional risk. Formal Python evidence is optional when appropriate, never a substitute for the application's own test runner.

Before claiming readiness, verify that Claude lists the installed Skills and can invoke the relevant Skill. If adh-reviewer is installed, confirm it appears in /agents before claiming independent review. Never claim a missing native test passed. This file grants no tool permissions.
