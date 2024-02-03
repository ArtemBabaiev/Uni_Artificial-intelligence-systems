:- dynamic state/1.
:- dynamic problem/1.

what_problem :- write("What is the problem"), nl, read(X), (
    X == 'Overheating' -> assertz(problem(overheating)), overheating_question;
    X == 'Not powering up' -> assertz(problem(no_power)), no_power_question
), diagnose(Solution), write(Solution), retractall(state(_)), retractall(problem(_)).

overheating_question :- write("How long ago did you clean your PC?"), nl, read(X), X >= 1, assertz(state(requires_cleaning)), fail.
overheating_question.

no_power_question :- write("Is your power cord plugged in?"), nl, read(X), X == no, assertz(state(power_cord)), fail.
no_power_question :- write("Is your power supply starting?"), nl, read(X), X == no, assertz(state(power_supply)), fail.
no_power_question.

diagnose(clean_pc) :- problem(overheating), state(requires_cleaning).
diagnose(check_cpu_heatplate) :- problem(overheating), not(state(requires_cleaning)).

diagnose(plug_in_power_cord) :- problem(no_power), state(power_cord).
diagnose(replace_power_supply) :- problem(no_power), state(power_supply).

diagnose(unknown_problem) :- not(problem(no_power)), not(problem(overheating)).
