/* -*- Mode:Prolog; coding:iso-8859-1; indent-tabs-mode:nil; prolog-indent-width:8; prolog-paren-indent:4; tab-width:8; -*- 
Constraint store

Author: Tony Lindgren

*/
:- use_module([library(clpfd)]).

zebra:-
    House_colors = [Red, Green, White, Yellow, Blue],
    Nationality = [English, Swede, Dane, Norwegian, German],
    Pets = [Dog, Birds, Cats, Horse, Zebra],
    Drinks = [Tea, Coffee, Milk, Beer, Water],
    Smokes = [PallMall, Dunhill, Blend, BlueMaster, Prince],

    domain(House_colors, 1, 5),
    domain(Nationality, 1, 5),
    domain(Pets, 1, 5),
    domain(Drinks, 1, 5),
    domain(Smokes, 1, 5),

    all_different(House_colors),
    all_different(Nationality),
    all_different(Pets),
    all_different(Drinks),
    all_different(Smokes),

    Red #= English,
    Swede #= Dog,
    Dane #= Tea,
    Green #= White - 1,
    Coffee #= Green,
    PallMall #= Birds,
    Yellow #= Dunhill,
    Milk #= 3,
    Norwegian #= 1,
    (Cats #= Blend + 1) #\/ (Blend #= Cats + 1),
    (Yellow #= Horse + 1) #\/ (Horse #= Yellow + 1),
    BlueMaster #= Beer,
    German #= Prince,
    (Blue #= Norwegian + 1) #\/ (Norwegian #= Blue + 1),
    (Water #= Blend + 1) #\/ (Blend #= Water + 1),

    append(House_colors, Nationality, Temp1),
    append(Temp1, Pets, Temp2),
    append(Temp2, Drinks, Temp3),
    append(Temp3, Smokes, VariableList),

    labeling([], VariableList),

    sort([Red-red, Green-green, White-white, Yellow-yellow, Blue-blue], House_color_connection),
    sort([English-english, Swede-swede, Dane-dane, Norwegian-norwegian, German-german], Nation_connection),
    sort([Dog-dog, Birds-birds, Cats-cats, Horse-horse, Zebra-zebra], Pet_connection),
    sort([Tea-tea, Coffee-coffee, Milk-milk, Beer-beer, Water-water], Drink_connection),
    sort([PallMall-pallmall, Dunhill-dunhill, Blend-blend, BlueMaster-bluemaster, Prince-prince], Smoke_connection),

    Format = '~w~15|~w~30|~w~45|~w~60|~w~n',
    format(Format, ['house 1', 'house 2', 'house 3', 'house 4', 'house 5']),
    format(Format, House_color_connection),
    format(Format, Nation_connection),
    format(Format, Pet_connection),
    format(Format, Drink_connection),
    format(Format, Smoke_connection).
            
        