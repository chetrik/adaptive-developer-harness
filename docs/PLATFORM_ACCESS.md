# Джерела та необхідний мережевий доступ

Ця зміна не змінює мережевих дозволів. Раніше підготовлена чернетка allowlist не означає погодження. Нижче точні домени, без wildcard; нові redirect-домени потребують окремого обґрунтування.

| Домен | Для чого |
|---|---|
| cursor.com | Поточна офіційна документація правил, Skills, субагентів, permissions |
| docs.cursor.com | Старі офіційні посилання/redirect на документацію Cursor |
| developers.openai.com | Контракти Codex, регресійна сумісність |
| code.claude.com | Claude Code: Skills, agents, rules, Hooks |
| antigravity.google | Офіційна документація Antigravity |
| docs.lovable.dev | Knowledge/Project Instructions, Workspace Skills, GitHub integration |
| ai.google.dev | AI Studio Build: ZIP/GitHub export та обмеження |
| docs.ollama.com | Локальний API, structured outputs, OpenAI compatibility |
| github.com | Офіційні source repositories, точні commits, ліцензії; checkout генератора |
| raw.githubusercontent.com | Оригінальні файли тих самих pinned repositories |

Для встановлення Python-залежностей у venv окремо використовуються `pypi.org` і `files.pythonhosted.org`; це package registry, не доказ контрактів платформ. Доступ визначає користувач/host.

У цій сесії Cursor rules/skills/subagents pages повернули proxy HTTP 403. Публічний getcursor/cursor README не містить достатнього контракту native rules/subagents. Спільний `.agents/skills/` підтверджений лише наданою користувачем діагностикою; кожне реальне середовище все одно проходить capability gate. Жодних непідтверджених `.cursor/rules` чи agent-конфігурацій не реалізовано. Інші платформи лишаються запланованими.

Відомі цільові сторінки для наступного дослідження: https://docs.lovable.dev/features/knowledge, https://docs.lovable.dev/features/skills, https://docs.lovable.dev/integrations/github, https://ai.google.dev/gemini-api/docs/aistudio-build-mode. Саме посилання не є підтвердженням доступності функції.
