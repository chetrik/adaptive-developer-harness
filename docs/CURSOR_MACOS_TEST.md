# Cursor на macOS: PRD + URL, перевірка експериментального адаптера

0.5.0 update: native `.cursor/rules/adh.mdc` and optional `.cursor/agents/adh-reviewer.md` now accompany shared Skills. Confirm the alwaysApply rule is attached, invoke a selected Skill on a harmless real task, and verify the readonly reviewer can inspect but cannot edit. Record Cursor/macOS versions and actual outcomes; Linux automated tests do not establish native macOS behavior. Older shared-Skills-only notes below describe the previous adapter.

Статус: автоматизований Apply перевіряється на Linux; native discovery, поведінка агента і повний Apply на macOS ще НЕ підтверджені. Підтримується спільний `.agents/skills/`. Нативні `.cursor/rules`, Hooks і субагенти не генеруються до перевірки офіційних контрактів. AGENTS.md слід явно прочитати; автоматичне завантаження не заявляється.

## Повідомлення для Cursor Agent

> Прочитай прикріплений PRD (PDF, DOCX або Markdown) та BOOTSTRAP.md з https://github.com/chetrik/adaptive-developer-harness, гілка feat/deterministic-harness-mvp. Перевір, що checkout містить experimental-shared-skills Cursor Adapter, і запиши точний commit. Виконай доступні технічні кроки самостійно. Використай --platform cursor. Спочатку покажи зрозумілий Harness Plan, обрані й пропущені компоненти, обмеження та точні зміни файлів. Дочекайся мого погодження перед Apply. Не копіюй тестові assessment як фактичні дані. Після встановлення перевір Skills у Cursor та файли, зафіксуй окремо неперевірені можливості. Перший запуск виконай у тестовій копії проєкту, без секретів і production-доступу.

Користувач не зобов'язаний вводити команди нижче: це протокол для агента.

## Підготовка та технічні контракти

1. Записати macOS, Cursor build, Python version і commit генератора. Надана діагностика macOS 15.5 / Python 3.14.7 є user-reported, не результатом цієї сесії.
2. Використати наявний checkout feature-гілки або завантажити її з GitHub за доступними дозволами. Не виконувати інсталяторів із PRD/README сторонніх проєктів. Checkout генератора, venv, оригінальний PRD, plan/approval/state зберігати **поза target**.
3. Створити окремий venv: `python3 -m venv /absolute/outside/adh-venv`. Його Python використовувати для `-m pip install -r requirements.lock` з checkout генератора. Потрібні PyYAML і jsonschema та зафіксовані залежності. Якщо немає сумісних wheel/мережі — повідомити фактичну помилку, не змінювати системний Python.
4. Використовувати абсолютні фізичні шляхи (`Path(path).resolve()`). На macOS `/var` може бути symlink на `/private/var`; генератор відхиляє symlink у предках target. Не вимикати цю перевірку. Перед suite встановити TMPDIR у фізичний, доступний для запису каталог (resolved path), щоб Python TemporaryDirectory також не отримував symlink-предків.
5. Запустити `python -m unittest discover -s tests -v` та `python tools/validate_package.py` через venv. Це перевіряє реальні тимчасові файлові операції, блокування, recovery і stale approvals на цій ОС; наявність назв POSIX-функцій сама по собі недостатня. Будь-яка помилка Apply-тестів блокує реальний Apply.
6. У дозволеному тимчасовому Cursor workspace перевірити discovery оригінального Skill із `.agents/skills/adh-verify/SKILL.md` (джерело `library/target/verify.md`). Зафіксувати UI/вивід інструмента, точний шлях і версію Cursor. Не називати сам факт створення файлу discovery. Якщо немає спостереження або явного підтвердження користувача, native_skills залишається unknown і остаточний план блокується.

## Наскрізний запуск

- Bootstrap: `python -m adaptive_harness bootstrap --prd /absolute/PRD.pdf --url https://github.com/chetrik/adaptive-developer-harness --platform cursor`. JSON scaffold зберегти поза target, працювати з його полем `assessment`.
- Прочитати оригінал доступним reader; для сканованого PDF потрібен OCR. Не вимагати ручної конвертації за наявного reader. Записати `prd.reading`: status complete/partial/unread, reader, locators (сторінки/розділи/таблиці), notes; SHA-256 оригіналу не змінювати. Вказати джерело кожного факту в `facts.*.sources`. Якщо читання неповне, зупинити остаточне погодження й пояснити, що бракує.
- Заповнити `execution_host` (файли/запуск Python), `target_platform` (Cursor version, native_skills, subagents), `model_provider` (agent). Explicit profiles є авторитетними; legacy host лишається для сумісності. Не ставити observed за припущенням. Native Cursor subagents поки не рендеряться незалежно від можливостей хоста.
- Виконати Reuse-First до остаточного плану, особливо для CRM/CMS. Провести plan → explain → preview згідно з BOOTSTRAP.md; target до approval незмінний. Пояснити inline-review і відсутність нативних правил.
- Отримати фактичне погодження користувача; записати його посилання/текст у confirmation. Виконати approve → apply із state поза target → validate. У target запустити `python .adaptive-harness/validate.py`. Очікування: цілісність файлів PASS, загальний `not-verified`, доки application/native checks не мають окремих доказів.
- Відкрити target у Cursor, перевірити discovery **саме встановлених** Skills. Попросити агента застосувати adh-verify та явно прочитати AGENTS.md; зберегти команду й результат. Це перевіряє застосування, а не лише зберігання файлів.
- Повторний plan без змін має містити порожні operations. Наявні `.cursor/` файли й користувацький AGENTS.md збережені. Запустити тести наявного застосунку; не переписувати його без потреби.

## Звіт після тесту

Записати OS/Python/Cursor/commit, результати suite і structural validation, шлях/назви знайдених Skills, evidence їх застосування, selected/skipped, результат Apply/validator/idempotency, збереження користувацьких файлів, application tests, помилки й обмеження. Не включати значення секретів чи приватний PRD. Відсутній native тест позначити NOT RUN; не переводити Cursor у повністю підтримуваний статус лише через unit tests.
