friend(john, julia).
friend(john, jack).
friend(julia, sam).
friend(julia, molly).
friend(jack, adam).
friend(adam, bill).
friend(bill, julia).
friend(molly,jack).
friend(julia, emma).
friend(emma,bill).
friend(sam,adam).
friend(jack,amy).
friend(amy,john).
friend(amy,bill).
friend(adam,amy).
friend(molly,bill).

loves(john, julia).
loves(julia, sam).
loves(sam, julia).
loves(emma,jack).
loves(adam,amy).
loves(molly,bill).
loves(bill,amy).
loves(amy,bill).
loves(jack,molly).

knows(X,Y) :- friend(X,Y); friend(Y,X).
lovers(X,Y) :- loves(X,Y), loves(Y,X).
