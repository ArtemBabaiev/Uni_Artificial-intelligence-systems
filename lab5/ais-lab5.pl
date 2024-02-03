:- use_module(library(lists)).

frame(building,
    []
).

frame(house,
    [ako - building,
     type - residential,
     construction_material - wood,
     number_of_rooms - 4,
     floors - 2
    ]).

frame(apartment_building,
    [ako - building,
     type - residential,
     construction_material - concrete,
     number_of_apartments - 20,
     floors - 5
    ]).

frame(skyscraper,
    [ako - building,
     type - commercial,
     construction_material - steel,
     number_of_floors - 50
    ]).

frame(construction_material,
    []
).

frame(wood,
    [ako - construction_material,
     properties - natural,
     durability - low
    ]).

frame(concrete,
    [ako - construction_material,
     properties - artificial,
     durability - high
    ]).

frame(steel,
    [ako - construction_material,
     properties - artificial,
     durability - very_high
    ]).

query(ID, Slot, Value) :-
    frame(ID, Slots),
    member(Slot-Value, Slots).

query(ID, Slot, Value) :-
    frame(ID, Slots),
    member(ako-Parent, Slots),
    query(Parent, Slot, Value).

get_durability(Construction, Durability) :-
    query(Construction, construction_material, Material),
    query(Material, durability, Durability).
get_construction_with_properties(Properties, Construction) :-
    query(Construction, construction_material, Material),
    query(Material, properties, Properties).

% get_durability(house, Durability)
% query(CONST, type, residential)
% get_construction_with_properties(natural, Construction)