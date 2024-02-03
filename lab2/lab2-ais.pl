male("Б.Ілля.О").
male("Б.Артем.І").
male("Б.Єгор.І").
male("Б.Олексій.О").
male("Б.Віталій").
male("П.В'ячеслав").
male("П.Віктор.Вя").
male("С.Іван.В").
male("С.Владислав.І").
male("С.Віктор.І.м").
male("С.Віктор.І.с").
male("Б.Олександр").

female("Б.Наталія.В").
female("Б.Поліна.В").
female("Б.Ання.В").
female("Б.Юлія.О").
female("П.Ольга.Вя").
female("П.Ольга.Ві").
female("С.Світлана.І").
female("С.Ксенія").
female("С.Светлана.О").
female("Б.Наталія.І").

parent("Б.Ілля.О", "Б.Артем.І").
parent("Б.Ілля.О", "Б.Єгор.І").
parent("Б.Ілля.О", "Б.Олексій.О").
parent("Б.Наталія.В", "Б.Артем.І").
parent("Б.Наталія.В", "Б.Єгор.І").
parent("Б.Наталія.В", "Б.Олексій.О").

parent("Б.Віталій", "Б.Поліна.В").
parent("Б.Віталій", "Б.Ання.В").
parent("Б.Юлія.О", "Б.Поліна.В").
parent("Б.Юлія.О", "Б.Ання.В").

parent("П.В'ячеслав", "П.Ольга.Вя").
parent("П.В'ячеслав", "П.Віктор.Вя").
parent("П.Ольга.Ві", "П.Ольга.Вя").
parent("П.Ольга.Ві", "П.Віктор.Вя").

parent("С.Іван.В", "С.Віктор.І.м").
parent("С.Іван.В", "С.Світлана.І").
parent("С.Іван.В", "С.Владислав.І").
parent("С.Ксенія", "С.Віктор.І.м").
parent("С.Ксенія", "С.Світлана.І").
parent("С.Ксенія", "С.Владислав.І").

parent("С.Віктор.І.с", "С.Іван.В").
parent("С.Віктор.І.с", "П.Ольга.Ві").
parent("С.Віктор.І.с", "Б.Наталія.В").
parent("С.Светлана.О", "С.Іван.В").
parent("С.Светлана.О", "П.Ольга.Ві").
parent("С.Светлана.О", "Б.Наталія.В").

parent("Б.Олександр", "Б.Ілля.О").
parent("Б.Олександр", "Б.Юлія.О").
parent("Б.Наталія.І", "Б.Ілля.О").
parent("Б.Наталія.І", "Б.Юлія.О").

granddad(X, Z):-parent(X,Y),parent(Y,Z),male(X).
grandmom(X, Z):-parent(X,Y),parent(Y,Z),female(X).

mother(M,C):-parent(M,C),female(M).
father(F,C):-parent(F,C),male(F).

get_sisters(Person,List) :- 
    findall(X, sister(X, Person), TempList), 
    remove_duplicates(TempList, List).
get_brothers(Person,List) :- 
    findall(X, brother(X, Person), TempList), 
    remove_duplicates(TempList, List).

sister(X,Y) :- parent(Z,X), parent(Z,Y), female(X), X \== Y.
brother(X,Y) :- parent(Z,X), parent(Z,Y), male(X), X \== Y.

wife(X,Y) :- parent(X,Z),parent(Y,Z), female(X),male(Y).
husband(X,Y) :- parent(X,Z),parent(Y,Z), male(X),female(Y).

uncle(X,Z) :- brother(X,Y), parent(Y,Z).
aunt(X,Z) :- sister(X,Y), parent(Y,Z).



remove_duplicates([],[]).

remove_duplicates([H | T], List) :-    
     member(H, T),
     remove_duplicates( T, List).

remove_duplicates([H | T], [H|T1]) :- 
      \+member(H, T),
      remove_duplicates( T, T1).
