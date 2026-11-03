# Adaptive Developer Harness

Передайте coding agent **свій PRD + посилання на цей репозиторій**. Агент підбере мінімально потрібні Skills, правила й перевірки, пояснить вибір і після вашого погодження встановить їх у проєкт.

**Почніть тут:** [інструкція для користувача українською](START_HERE_UA.md) — з готовим текстом для агента.

Змінюєте чат або coding agent? [Як передати проєкт і продовжити роботу](START_HERE_UA.md#5-як-змінити-чат-модель-або-coding-agent).

Для coding agent: [BOOTSTRAP.md](BOOTSTRAP.md). Актуальна версія — у `main`: https://github.com/chetrik/adaptive-developer-harness .

## Перевірено в Claude Code на macOS

**Реальний тест встановлення та нативного виклику Skill пройдено** — за звітом власниці проєкту від 3 листопада 2026 року, Python 3.14.7, Harness 0.5.1.

| Перевірка | Результат |
|---|---|
| PRD → план → погодження → встановлення | PASS: створено 9 погоджених файлів |
| Цілісність Harness | PASS: 9 хеш-перевірок; `Harness integrity: PASS`, exit 0 |
| Виявлення `adh-implement` та `adh-verify` у новій сесії проєкту | PASS: обидва Skills у списку |
| Нативний виклик `adh-verify` через Skill tool | PASS: інструкції завантажено, перевірку цілісності виконано без зміни файлів |

Тест підтверджує встановлення, виявлення Skills і нативний запуск `adh-verify`. Реалізацію застосунку через `adh-implement`, його тести та UI в цьому сценарії ще не перевіряли. [Подробиці тесту та межі перевірки](docs/VERIFICATION.md#claude-code-macos-native-test-2026-11-03).

## Що працює

- Спільний генератор: аналіз структурованих вимог → мінімальний вибір → зрозумілий план → preview → погодження → встановлення й перевірка файлів.
- Нативні формати Codex, Claude Code, Cursor та Antigravity; Lovable import packages. Точні межі перевірок: [платформи](docs/PLATFORM_DELIVERY.md). Створення конфігурацій не означає підтверджену роботу кожного host.
- Оновлення без мовчазного перезапису користувацьких правок; погоджене видалення, inventory, recovery і міграції.
- PRD у Markdown/PDF/DOCX через reader агента. Локальний Ollama може запропонувати assessment для Markdown; агент його перевіряє.
- Перевірка отриманого ZIP, аналіз існуючого проєкту, вибірковий export із handoff для продовження роботи в іншому середовищі.

Ви не мусите запускати CLI чи вручну встановлювати Skills. Агент виконує технічні кроки в межах дозволів. Для малих змін досить короткого циклу в чаті й справжніх тестів застосунку. Великі/ризикові зміни отримують відповідні специфікації й перевірки.

**Ще не підтверджено в реальних account-сесіях:** виклик `adh-implement` і reviewer у Claude, invocation Skills/subagents у Cursor/Antigravity, імпорт і застосування у Lovable, експорт конкретного проєкту AI Studio. Конфігурації та пакування реалізовано й перевірено автоматизовано. Деталі й конкретні blockers наведено в таблиці платформ. Ми не називаємо це завершеною підтримкою лише на підставі unit tests.

## Для розробки генератора

Python 3.11+, POSIX, dependencies із requirements.lock; запуск із checkout, standalone wheel не підтримується.

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_package.py
python3 -m adaptive_harness doctor --platform claude-code
```

[Contributor instructions](AGENTS.md) · [Architecture](docs/ARCHITECTURE.md) · [Requirements](docs/PRD.md) · [Verification](docs/VERIFICATION.md) · [Updates/recovery](docs/UPDATES_AND_SESSIONS.md) · [Engineering Gates](docs/ENGINEERING_GATES.md).

[Third-party notices](THIRD_PARTY_NOTICES.md) · [Reference audit](docs/REFERENCE_AUDIT.md). Generated components are original MIT-licensed assets. Historical documents and generator internals are not installed in customer projects.
