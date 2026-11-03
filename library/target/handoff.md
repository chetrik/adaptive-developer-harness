# Session Handoff

Після явного завершення сесії/етапу запиши: session_id, phase (Specification/Implementation/Verification), task, decisions, completed, unfinished, changed_files, tests, risks, next_step.

Масив tests має містити фактичні command/status/exit_code/detail. Якщо тест не виконувався — status not-verified або skipped, exit_code null; не вигадуй PASS. Рішення й завершені дії можуть посилатися на специфікацію та документацію. Не копіюй секрети, приватні логи чи повний чат.

Coding agent використовує генератор: handoff-plan --assessment <поточний assessment> --record <JSON> --target <проєкт>, далі preview → погодження → apply. Це той самий Harness Plan/Apply, не інший механізм запису. Генератор фіксує відбиток робочих файлів; session_id позначає незмінний checkpoint. Спочатку заверши всі окремо погоджені оновлення Harness.

На початку наступної сесії: resume --target <проєкт> --session-id <id>. Для stale перечитай актуальні файли, рішення й тести, звір розбіжності перед продовженням. Не вважай минуле погодження дозволом на нову задачу. Новий чат не обов’язковий; для XS/S достатньо одного короткого циклу без додаткової специфікації.

Це шаблон, не доказ виконання. Автоматичного перехоплення закриття чату немає; при аварії доступний лише останній записаний checkpoint.

Для задач із Engineering Gates передай `--engineering <request.json>` у handoff-plan: readiness обчислить генератор. Поле completed залишається звітом агента; воно не замінює формальний gate. Зберігай evidence-dir поза target і передай його доступний шлях наступній сесії. Старі handoff без observed receipts не стають verified автоматично.
