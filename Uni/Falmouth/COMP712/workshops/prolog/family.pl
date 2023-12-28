male(brad).
male(john).
male(jim).
male(alfred).
female(marry).
child(brad, alfred).
child(john, jim).
child(john, marry).

% relationships
mom(X,Y) :- female(X), child(Y,X).
dad(X,Y) :- male(X), child(Y,X).
parent(X,Y) :- mom(X,Y) ; dad(X,Y).
grandma(X,Y) :- female(X), parent(X,Z), parent(Z,Y).
grandpa(X,Y) :- male(X), parent(X,Z), parent(Z,Y).
grandparent(X,Y) :- grandma(X,Y) ; grandpa(X,Y).

