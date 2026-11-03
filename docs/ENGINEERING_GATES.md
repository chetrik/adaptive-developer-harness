# Engineering Gates — optional formal evidence

In 0.5.0, ordinary XS/S work uses inline scope and the application’s real tests without mandatory task JSON/receipts. The formal API below is retained for additional evidence; unsupported runners cannot receive verified receipts but do not prohibit development. This supersedes mandatory use in the original 0.4.0 workflow.

Це перевірки готовності всередині наявного Specification → Implementation → Verification. Selection Engine, Harness Plan та Apply залишаються спільними для Codex/Cursor. Gate не є host hook і не може заборонити всі сторонні дії coding agent.

## Шлях користувача

Людина передає PRD + URL через [BOOTSTRAP](../BOOTSTRAP.md). Агент встановлює погоджений Harness, уточнює задачу, читає потрібні джерела й показує конкретні причини готовності або блокування. Користувач не зобов’язаний запускати CLI. Для XS/S досить короткого завдання в поточному чаті: агент передає структурований task через API або тимчасовий файл поза проєктом. Окремі spec-документи та сесії не потрібні. Чинний запит користувача може бути посиланням на погодження специфікації; повторно питати без зміни scope/ризику не потрібно.

Існують три різні дозволи: встановити компоненти (`approve`), виконати погоджену задачу (`approve-spec`), запускати код з відповідними правами host (`test-run --execution-confirmation`). Один не дає решти автоматично. Confirmation — посилання на реальну подію дозволу, а не довільна вигадана фраза. Автентифікація людини залишається відповідальністю host.

## Контракти та маршрут агента

[engineering-task.schema.json](../schemas/engineering-task.schema.json) містить goal/scope, Given/When/Then acceptance, edge cases, NFR, critical questions, джерело специфікації, bounded context, implementation/test/config paths, AC → unittest ID, вплив на документацію, необов’язковий handoff ID. Приклад конструкції task і виконання API — [test_engineering_gates.py](../tests/test_engineering_gates.py). Це synthetic fixture, не свідчення користувацького погодження.

1. Агент формує task із реальних вимог. Для M/L/XL потрібні edge cases та error AC; security/API/migration критерії випливають із чинних вибраних модулів. NFR з unknown дає not-verified; критичні питання блокують. Формат перевіряється кодом, зміст потребує review.
2. `read-context --task TASK --target PROJECT --evidence-dir STATE` повертає лише погоджені діапазони рядків та receipt IDs. До 32 джерел, 1 MiB на джерело, 32 KiB сумарно доставленого тексту. Rules та наявний пов’язаний code обов’язкові; зовнішня spec має збігатися з hash і контекстом. Для нового коду не вигадується читання ще неіснуючого файла. Architecture/handoff додаються за релевантністю. Читання захищених шляхів і symlinks відхиляється.
3. `approve-spec --task TASK --target PROJECT --evidence-dir STATE --confirmation EVENT` фіксує task hash, початковий code і docs, актуальний handoff. Агент зберігає ID як `spec_approval`, context IDs як масив `context` у RECEIPTS.
4. `gate --assessment ASSESSMENT --task TASK --target PROJECT --evidence-dir STATE --receipts RECEIPTS --transition implementation` перевіряє поточні джерела та дозвіл. `pass` дозволяє заявити формальну готовність; `blocked` має конкретну перешкоду; `not-verified` означає відсутність доказу. Окремий нерелевантний check має `not-applicable`. Неготовий gate повертає exit 2.
5. Для bugfix агент спочатку відтворює дефект тестом: `test-run ... --phase red --execution-confirmation EVENT`. Усі команди викликаються як `python -m adaptive_harness COMMAND`; спільні параметри task/target/evidence-dir ті самі. RED — assertion failure цільового тесту на початковій реалізації. Crash, import error, skip, timeout, empty suite або initial GREEN не є RED. Неможливість відтворити означає діагностику й not-verified.
6. Після зміни лише погодженої реалізації агент перевіряє `gate ... --transition verification`, запускає `test-run ... --phase green --execution-confirmation EVENT`, додає `red`/`green` receipt IDs та перевіряє `gate ... --transition complete`. GREEN повинен належати поточним bytes проєкту; усі AC-mapped tests мають пройти. Між RED/GREEN незмінні tests, configs, undeclared fixtures/inputs, selection і набір тестів. Код повинен змінитися, запуск GREEN відбутися пізніше. Зміна очікувань потребує повторного RED на вихідному коді. Вплив на документацію має погоджену причину `none` або фактичні зміни зазначених документів.
7. За потреби агент передає [engineering-request](../schemas/engineering-request.schema.json) (`task`, `receipts`, `state_dir`, `transition`) через `plan --engineering` або `handoff-plan --engineering`. Звіт додається до спільного Harness Plan/Session Handoff. Усі записи компонентів і handoff проходять чинний Apply. Погодження повторно обчислює readiness. Неготовність задачі не забороняє встановлення інструментів Harness. Звіт у handoff є історичним: при продовженні потрібна повторна перевірка джерел і receipts.

## Докази та обмеження

STATE — приватна директорія поза customer project; task/receipt input файли також краще тримати поза проєктом, щоб не змінювати snapshot результату. HMAC receipts відхиляють довільні або змінені JSON; вони не захищають від зловмисного власника host, ключа чи тестового процесу. Тести — довірений для запуску код під sandbox/дозволами host, не ізоляція нашого runner. Спостереження виконання не є незалежним security review або доказом семантичної повноти AC.

Реалізований observer підтримує Python unittest, POSIX process groups, 120 s maximum timeout та 128 KiB output limit. Інші test runners/CI й native read receipts поки не реалізовані: використовуйте not-verified, не підмінюйте їх self-report. Тести, які змінюють проєкт, не отримують verified receipt; використовуйте зовнішню тимчасову директорію для артефактів. Застосовуються чинні обмеження snapshot; hash scan прив’язує виконання до bytes, але не завантажує весь код у контекст моделі. Захищені secrets представлені metadata, не прочитаним вмістом.

PDF/DOCX intake залишається через доступний reader агента з provenance. Новий receipt reader працює лише з UTF-8 текстом; він не видає verified native PDF/DOCX evidence. Потрібна перевірна текстова специфікація/джерело або not-verified. Це обмеження evidence інтеграції, не вимога до новачка вручну конвертувати документ.

## Оновлення 0.3.0 → 0.4.0

Змінено generated AGENTS block і чотири наявні assets: feature, implement, verify, handoff. Нових сторонніх Skills/фреймворків немає. Формат manifest залишається 2.0; існуючий inventory знає точні історичні hashes. Старі user edits блокують оновлення; немає автоматичного перезапису. Preview та install approval охоплюють мінімальний diff; повторне планування дає нуль операцій.

Engine hash змінюється навмисно; старі плани не застосовуються новим engine. Зберігайте початковий checkout та state-dir для операцій, розпочатих 0.3.0. Спочатку `recover` тим самим reviewed engine, потім новий plan/approval. Новий Apply відмовляється випереджати незавершений journal у переданому state-dir. Він не знаходить journals в інших довільних директоріях. Перевірка запускає справжній попередній код commit `63dc1bd47e0ef9b3002ada24127c5a5ba2853f90`; regression потребує цього Git object. Downgrade та невідомі версії не підтримуються.
