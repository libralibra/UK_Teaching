:- use_module(library(clpq)).

head(C,R,H) :- {C+R=H}.
leg(C,R,L) :- {2*C+4*R=L}.

solution(C,R,H,L) :- head(C,R,H), leg(C,R,L), C>0, C<H, R>0, R<H,
    write('If there are '), write(H), write(' head and '), write(L), write(' legs:'), nl,
    write('Chicken: '), write(C), nl,
    write('Rabbit: '), write(R).
