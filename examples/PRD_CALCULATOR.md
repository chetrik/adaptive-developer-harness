# Test fixture — personal offline calculator

**User story:** I want a simple calculator that can estimate saved work hours and monthly/annual money saved from employee count, weekly hours saved per person and hourly euro rate. Use it for demonstrations and internal planning. No accounts, database, payment integration or customer PII. Runs locally.

**First version:** simple responsive web page; inputs validated as nonnegative; monthly estimate uses an explicit weeks/month assumption; display calculation assumptions; accessible button and readable results.

**Expected harness characteristics:** short PRD/agent entrypoint, simple test of arithmetic and input edge cases, safe local workflow; no enterprise architecture diagrams, migration scripts or independent security subagents by default.
