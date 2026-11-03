# Платформи та готовність до роботи — 0.5.0

Один Selection Engine, один Harness Plan, один Apply. Поточні результати нижче розрізняють створення файлів, нативне виявлення та фактичну роботу агента.

| Середовище | Що реалізовано | Що ще потребує підтвердження |
|---|---|---|
| Codex | AGENTS.md, .agents/skills, conditional reviewer, install/update/recovery | Новий native probe у цьому середовищі завершується read-only filesystem; раніше discovery підтверджено, новий model turn не виконано |
| Claude Code | CLAUDE.md entry, .claude/skills, read-only .claude/agents/adh-reviewer.md; спільний Plan/Apply | Формати підтверджено офіційними GitHub-прикладами; Claude CLI 2.1.317 doctor пройшов у generated project; invocation Skills/reviewer потребує sign-in і не виконаний |
| Cursor | Спільні .agents/skills, .cursor/rules/adh.mdc, readonly .cursor/agents/adh-reviewer.md | Офіційні формати й автоматизовані install/update тести підтверджено; native invocation на macOS не виконаний |
| Antigravity | AGENTS.md, .agents/skills, always_on .agents/rules/adh.md, reviewer із view_file/grep_search | Офіційні формати й автоматизовані тести підтверджено; native invocation не виконаний |
| Lovable | Project Instructions, AGENTS.md, вибрані Workspace Skills, окремі import ZIP, порівняння інструкцій, code handoff | Формат імпорту підтверджено документацією; потрібен owner/admin для фактичного імпорту та task test у workspace |
| Google AI Studio Build | Export & Continue: ZIP inspection, залежності/env/services, handoff, встановлення destination adapter | Офіційно підтверджено ZIP і GitHub sync; експорт конкретного проєкту потребує доступу до його account. Custom Skills не заявляються |
| Ollama | Локальний /api/chat, structured proposal → schema validation → agent review | HTTP-контракт перевірено локальним тестовим сервером; запуск реальної моделі потребує встановленого Ollama/model |

Ця таблиця не називає заплановані або лише contract-tested інтеграції повністю підтриманими. Недоступний native adapter `doctor` показує як blocked; AI Studio має окремий export-required маршрут. Не використовуйте іншого host у assessment для обходу цього обмеження.

## Реальний вхід

Передайте агенту PRD та URL із гілкою: https://github.com/chetrik/adaptive-developer-harness/tree/feat/deterministic-harness-mvp . Агент читає [BOOTSTRAP](../BOOTSTRAP.md), готує середовище, інтерпретує PRD, перевіряє host, пропонує мінімальний Harness, після погодження встановлює його й виконує першу погоджену зміну застосунку. Без такого останнього кроку тестуємо інсталятор, а не повний досвід користувача.

На Claude Code після встановлення перевірте список Skills і виклик `/adh-implement` та `/adh-verify` відповідно до можливостей вашої версії. Якщо reviewer обраний, перевірте `/agents`: він має лише Read/Glob/Grep; не може виконувати тести чи редагувати файли. Передавайте йому фактичний diff і результати виконання через parent agent. Наявний чужий CLAUDE.md не перезаписується: конфлікт блокує встановлення до узгодженого об’єднання правил. Host permissions не змінюються.

Для невеликої задачі — короткий цикл у чаті з реальним runner застосунку: npm/node/pytest/go тощо. Формальні Engineering Gates залишаються додатковою перевіркою; unsupported runner не означає заборону розробки і не перетворюється на verified receipt. Великі/ризикові задачі потребують відповідної специфікації, доказів і handoff.

## Project Handoff / Export & Continue

Агент виконує команди з генератора, користувач не мусить оперувати CLI:

```text
python3 -m adaptive_harness inspect-export --archive /outside/export.zip
python3 -m adaptive_harness inspect-project --target /path/exported-app
python3 -m adaptive_harness export-project --target /path/app --files /outside/selection.json --output /outside/project.zip --confirmation 'actual export approval reference'
```

selection.json — явний масив відносних шляхів. Включіть PRD, вихідний код, manifests/lockfiles залежностей, потрібні ресурси, рішення й актуальний handoff. ZIP містить оригінальні bytes обраних файлів та HARNESS_HANDOFF.json. Невибрані файли не копіюються. Попередній перегляд — список шляхів та inspect-project; підтвердження експорту окреме від встановлення Harness. Існуючий archive не перезаписується. Необхідні файли не визначаються досконало автоматично: агент має звірити entrypoints/imports/dependencies.

Інспекція не виконує код, не встановлює залежності й не читає credential-файли. Виявляє назви environment variables, відомі external services, dependency files, доступні test script names, відсутній JS lockfile і відсутні обрані dependency/context files у пакеті. ZIP із traversal, symlinks, duplicates, encryption чи перевищенням лімітів відхиляється. Потенційні credentials блокують їх експорт. Це обмежена перевірка, не гарантія виявлення всіх секретів. Вміст PRD/code потрібно перевірити перед зовнішньою публікацією.

Дані БД, accounts, hosted configuration та chat history **не переносяться разом із кодом автоматично**. Список env names не містить значень. Секрети налаштовуються в новому середовищі окремо. Без наданого експорту історія чату невідома. Використовуйте наявний код, не починайте переписування лише через зміну coding agent.

## Local Ollama

```text
python3 -m adaptive_harness interpret --prd /path/PRD.md --model YOUR_INSTALLED_MODEL --platform claude-code
```

За замовчуванням http://127.0.0.1:11434; лише HTTP loopback, без proxy/redirect та віддаленого завантаження PRD. Моделі не встановлюються автоматично. Markdown до 64 KiB, timeout до 120 s, response до 1 MiB. PDF/DOCX читає агент доступним reader, зберігаючи походження. Усі модельні факти inferred, capabilities лишаються unknown, reading partial до перевірки агентом. Reuse-First, approval і selection policy не обходяться.

## Перевірені джерела форматів

Початковий proxy 403 усунуто після погодження й збереження користувачкою мережевих налаштувань. Нижче офіційні джерела контрактів, без копіювання реалізації чи prompt-текстів:

- [Anthropic claude-code @ 964d695](https://github.com/anthropics/claude-code/tree/964d69565952a176ac1975ed218362991db71433): CLAUDE.md project instructions.
- [Anthropic automation references @ a2e251d](https://github.com/anthropics/claude-plugins-official/blob/a2e251d9b97b909bf728b3e84fc8d17e6aba0063/plugins/claude-code-setup/skills/claude-automation-recommender/SKILL.md): project .claude/skills and .claude/agents locations; official agent frontmatter examples. Repository license Apache-2.0; no assets copied.
- [Ollama API @ 355eaee](https://github.com/ollama/ollama/blob/355eaee353f81f598932faf3226344d39e482860/docs/api.md): /api/chat, message.content, stream:false, JSON Schema format. No implementation copied.

## Міграції

0.3.0/0.4.0 → 0.5.0 використовують чинний inventory, точні історичні asset hashes, preview/approval, journal/recovery. Manifest лишається 2.0. Зміна host зберігає старі компоненти як pending removal до погодженого видалення. Чужі й змінені файли блокують оновлення. Старі плани не перевикористовуються новим engine; старі interrupted operations відновлює їхній початковий reviewed checkout зі своїм state-dir.


Після відкриття мережі прочитано й використано актуальні контракти:

- [Cursor rules](https://cursor.com/docs/context/rules): .mdc, alwaysApply; [Skills](https://cursor.com/docs/context/skills): shared Agent Skills; [subagents](https://cursor.com/docs/subagents): .cursor/agents markdown, readonly:true, model:inherit.
- [Antigravity rules](https://antigravity.google/docs/rules/): AGENTS.md + .agents/rules/*.md із trigger:always_on; [Skills](https://antigravity.google/docs/skills/): .agents/skills; [subagents](https://antigravity.google/docs/subagents/): .agents/agents, tools list, subagent/mainAgent, commandExecutionPolicy. Використано лише документовані view_file/grep_search; shell і writes не надаються.
- [Lovable Instructions](https://docs.lovable.dev/features/knowledge): Project settings → Instructions, limit 10,000 chars, root AGENTS always read; [Skills](https://docs.lovable.dev/features/skills): owner/admin import, SKILL.md root або one wrapper, GitHub folder/blob URL, workspace-wide auto-use; [GitHub](https://docs.lovable.dev/integrations/github): account authorization/sync.
- [AI Studio Build](https://ai.google.dev/gemini-api/docs/aistudio-build-mode): Add files → Import from GitHub; Settings → GitHub для sync; ZIP download для локального продовження. Не припускаємо виконання наших Skills.

## Lovable: згенерувати, імпортувати, перевірити

Агент зовні використовує bootstrap --platform lovable та звичайний plan/approve/apply. ExecutionHost має підтверджувати доступ до файлів і Python; native Skills discovery не є передумовою створення **import package**, оскільки ще нічого не імпортовано. Plan явно має import-required. Вибір модулів той самий; субагенти недоступні.

```text
python3 -m adaptive_harness package-skills --target /path/app --output-dir /outside/skill-packages --confirmation 'actual package export approval'
python3 -m adaptive_harness check-instructions --target /path/app --project-instructions /outside/current-project.txt --workspace-instructions /outside/current-workspace.txt
```

Команда створює по ZIP на активний вибраний Skill, SKILL.md у корені. Limits перевірено кодом; існуючі packages та змінені assets не перезаписуються. Project Instructions/IMPORT.md лежать у .adaptive-harness/integrations/lovable/. Імпортуйте через Workspace settings → Skills → Add → Upload ZIP або через GitHub URL **створеної папки конкретного Skill**. У публічному репозиторії не повинно бути private project context.

check-instructions відокремлює точний збіг від відмінностей та nonempty workspace context, що потребують semantic review. Він ніколи не називає довільні тексти безконфліктними лише за hashes. Агент перевіряє фактичні суперечності між Project/Workspace Instructions, AGENTS і вибраними Skills. Зміни полів UI потребують user/account access; Python не виконується всередині Lovable за припущенням.

Перевірка застосування: Skill є у списку `/` → явний виклик на безпечній задачі → фактичний результат відповідає інструкції → реальні тести застосунку. Auto-use окремо перевіряється після ввімкнення; manual invocation не доводить автоматичної активації. Код, база даних і історія розробки переносяться окремо.
