from math import sqrt

In = input("In=")
Pn= input("Pn=")
Un= input("Un=")
cosFi= input("cosFi=")
KPD = input("KPD=")

if In== "x":
    formula = "In=Pn/(sqrt(3)*Un*cosFi*KPD"
    result = float(Pn)/(sqrt(3)*float(Un)*float(cosFi)*float(KPD))
elif Pn == "x":
    formula = "Pn=In*sqrt(3)*Un*cosFi*KPD"
    result = float(In)*sqrt(3)*float(Un)*float(cosFi)*float(KPD)
elif Un == "x":
    formula = "Un=Pn/(sqrt(3)*In*cosFi*KPD"
    result = float(Pn)/(sqrt(3)*float(In)*float(cosFi)*float(KPD))
elif cosFi == "x":
    formula = "cosFi=Pn/(sqrt(3)*In*Un*KPD"
    result = float(Pn)/(sqrt(3)*float(In)*float(Un)*float(KPD))
elif KPD == "x":
    formula = "KPD=Pn/(sqrt(3)*In*Un*cosFi"
    result = float(Pn)/(sqrt(3)*float(In)*float(Un)*float(cosFi))

print(f"{formula}\n{result}")