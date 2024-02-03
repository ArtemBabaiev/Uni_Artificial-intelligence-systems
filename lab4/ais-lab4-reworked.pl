:- dynamic is_a/2.

% is_a(class, superclass)
% university declaration
is_a(knu, university).
is_a(chnu, university).
is_a(lnu, university).
% types of person
is_a(student, person).
% declaration of students
is_a(artem, student).
is_a(anna, student).
is_a(petro, student).
is_a(bob, student).
% declaration of specializations
is_a(soft_eng, specialization).
is_a(mathematics, specialization).
is_a(medicine, specialization).
% declaration of subjects
is_a(databases, subject).
is_a(java_tech, subject).
is_a(high_math, subject).
is_a(math_analysis, subject).
is_a(anotomy, subject).
is_a(advanced_chemistry, subject).
% part_of(subject, specialization)
part_of(databases, soft_eng).
part_of(java_tech, soft_eng).
part_of(java_tech, mathematics).
part_of(high_math, mathematics).
part_of(math_analysis, mathematics).
part_of(anotomy, medicine).
part_of(advanced_chemistry, medicine).
% part_of(student, university)
part_of(artem, chnu).
part_of(bob, chnu).
part_of(anna, knu).
part_of(petro, lnu).

studies(artem,soft_eng).
studies(bob,mathematics).
studies(anna,medicine).
studies(petro,soft_eng).

% has_property(Person, Property, Value)
has_property(artem, age, 25).
has_property(anna, age, 22).
has_property(petro, age, 23).
has_property(bob, age, 24).
has_property(artem, gender, male).
has_property(anna, gender, female).
has_property(petro, gender, male).
has_property(bob, gender, male).

extends(X,Y):-is_a(X,Y).
extends(X,Y):-extends(X,Z), is_a(Z,Y).

enrolled_in(Student, University, Specialization) :-
    extends(Student, student),
    part_of(Student, University),
    studies(Student, Specialization).

students_studying_subject(Student, Subject) :-
    extends(Student, student),
    studies(Student, Specialization),
    part_of(Subject, Specialization).

male_student(Student) :-
    extends(Student, student),
    has_property(Student, gender, male).
female_student(Student) :-
    extends(Student, student),
    has_property(Student, gender, female).