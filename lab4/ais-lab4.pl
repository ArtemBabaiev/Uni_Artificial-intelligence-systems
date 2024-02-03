% has_student(educational_institution, student_name).
has_student(kyiv_university, anna).
has_student(lviv_university, petro).
has_student(chnu, artem).
has_student(chnu, bob).

% student_specialization(student_name, specialization).
student_specialization(anna, mathematics).
student_specialization(petro, physics).
student_specialization(artem, informatics).
student_specialization(bob, mathematics).

% educational_institution(educational_institution, city).
educational_institution(kyiv_university, kyiv).
educational_institution(lviv_university, lviv).
educational_institution(chnu, chernivtsy).

% subject(specialization, subject_name).
subject(mathematics, algebra).
subject(physics, mechanics).
subject(informatics, programming).
subject(informatics, databases).

enrolled_in(Student, Educational_Institution, Specialization) :-
    has_student(Educational_Institution, Student),
    student_specialization(Student, Specialization),
    educational_institution(Educational_Institution, _).

subjects_in_educational_institution(Educational_Institution, Subjects) :-
    educational_institution(Educational_Institution, _),
    findall(Subject, subject(_, Subject), Subjects).

students_on_subject(Subject, Students) :-
    subject(Specialization, Subject),
    findall(Student, enrolled_in(Student, _, Specialization), Students).
