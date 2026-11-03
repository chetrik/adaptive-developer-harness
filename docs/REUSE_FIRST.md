# Reuse-First Discovery Protocol

**Objective:** before developing a substantial commodity component, consider building from scratch, adapting verified OSS, buying/using a maintained service, or combining modules. Do not force research for a trivial fix or a clearly custom algorithm without plausible external alternatives.

## Trigger

- CRM, CMS, document processing, forms, authentication, e-commerce, calendaring, billing, search, admin panels, dashboards, automation, knowledge retrieval, UI component libraries or other widely implemented capabilities.
- During intake: also examine competitor/reference applications for user-visible behavior, especially if product is for external users. Distinguish UX inspiration from copying source/assets.
- Trigger again if scope changes materially, or integration effort proves larger than expected.

## Research record for every actual candidate

| Field | Required meaning |
|---|---|
| Name and source | Exact real GitHub URL or official product URL |
| Verification timestamp | Date inspected; `unverified` if host lacks network |
| License | SPDX, license file link, any separate asset/dependency terms |
| Maintenance | Last release/commit activity, support state; source and caveats |
| Functionality | Specific PRD requirements satisfied/missing |
| Technical fit | Stack, API, hosting, extensibility, data model, integration complexity |
| Security | Public advisories, dependency risk, handling of customer data, unknowns |
| Legal/operational | Commercial use, attribution, license notices, privacy/hosting, fees |
| Adaptation estimate | Work and uncertainty required to fit PRD |
| Evidence | Links, inspection notes, test or demo results |

## Output structure

1. Candidate comparison, with separate columns for **observed facts** and **estimates**.
2. Option A: adopt/adapt OSS; B: compose components; C: custom build; D: existing SaaS where appropriate.
3. Recommendation with constraints, cost implications and failure modes.
4. Explicit permission checkpoint before cloning, downloading, installing, executing, or copying source code.
5. Log sources in the project's inspiration/provenance register if used.

## Example: CRM

When asked to build a custom CRM, search for real repositories and commercial services first (when access allows). Compare user/role management, pipeline, activities, history, API, reporting, custom fields, localization, GDPR/data residency fit, technology and deployment needs. An old or abandoned CRM may cost more to maintain than creating a narrow internal tool. **Never fabricate a named candidate, recent activity, license or price**.

## Important distinction

Finding a GitHub repo does not confer a right to use it. Publicly readable code may have no license. Even MIT-licensed code can contain third-party components with different terms. Do not assume GitHub stars measure security.
