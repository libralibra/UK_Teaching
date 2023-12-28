color(red).
color(green).
color(blue).

colorify(WA,OR,CA,ID,NV,UT,AZ,MT,WY,CO,NM,ND,SD,NE,KS,OK) :-
    color(WA), color(OR), color(CA), color(ID), color(NV), color(UT), color(AZ), color(MT), color(WY), color(CO), color(NM), color(ND), color(SD), color(NE), color(KS), color(OK),
    \+ WA=OR, \+ WA=ID, \+ ID=MT, \+ ID=WY, \+ ID=NV, \+ ID=UT, \+ OR=CA, \+ OR=NV,
    \+ NV=AZ, \+ NV=UT, \+ MT=WY, \+ MT=ND, \+ MT=SD, \+ WY=UT, \+ WY=CO, \+ WY=SD,
    \+ WY=NE, \+ UT=AZ, \+ UT=CO, \+ AZ=NM, \+ CO=NE, \+ CO=KS, \+ CO=NM, \+ CO=OK,
    \+ ND=SD, \+ SD=NE, \+ NE=KS, \+ KS=OK.
