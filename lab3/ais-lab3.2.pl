causes_no_power("Відключений шнур живлення").
causes_no_power("Пошкоджений блок живлення").

causes_not_working("Пошкоджена плата керування").
causes_not_working("Відсутність сигналу від датчика").
causes_not_working("Пошкоджений мотор").

diagnose(Device, Symptom, Cause) :-
    causes_no_power(Cause),
    symptom(Device, Symptom),
    write('Причина несправності: '), write(Cause), nl.

diagnose(Device, Symptom, Cause) :-
    causes_not_working(Cause),
    symptom(Device, Symptom),
    write('Причина несправності: '), write(Cause), nl.

symptom(computer, "Не запускається").
symptom(computer, "Немає живлення").
symptom(printer, "Не друкує").
symptom(printer, "Зажурилася").
