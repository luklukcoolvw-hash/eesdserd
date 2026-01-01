import random
print("Lottozahlen:")
lottozahlen = random.sample(range(1, 50), 6)
lottozahlen.sort()  # Sortieren der Zahlen
#print(lottozahlen)
print("Geben Sie ihre Lottozahlen ein:")
#n = int(input("Wie viele Zahlen? "))
zahlen = []

for i in range(6):
    zahl = int(input(f"Zahl {i+1}: "))
    zahlen.append(zahl)
zahlen.sort()
for i in range(6):
    if zahlen[i] > 49:
        print("Zahl muss kleiner als 49 sein!")
        exit() 
    else:
        continue
for i in range(5):
    if zahlen[i] == zahlen[i+1]:
        print("Zahl darf nicht doppelt vorkommen!")
        exit()
    else:
        continue
a = 0

b = 0
f = 0
i = 0
print("Deine Zahlen:")
print(zahlen)
print("\nLottozahlen:")
print(lottozahlen)
while i < 6:
    if zahlen[i] in lottozahlen:
        a += 1
        i+= 1
    else:
        i+= 1
        continue
print(f"\nDu hast {a} Richtige!")

x1 = 0
x2 = 0
x3 = 0
zahlene = []
print("\nÜbereinstimmende Zahlen:")
while x3 < 6:
    if x3 == a:
        break    
    if zahlen[x1] == lottozahlen[x2]:
        x3 += 1
        x1 += 1
        x2 += 1
        zahlene.append(zahlen[x1-1])
    elif zahlen[x1] < lottozahlen[x2]:
        x1 += 1
    elif zahlen[x1] > lottozahlen[x2]:
        x2 += 1
print(zahlene)
print("")
if a == 1:
    print("Du hast 1 Zahl richtig!")
    print("Leider kein Gewinn.")
elif a == 2:
    print("Du hast 2 Zahlen richtig!")
    print("Leider kein Gewinn.")
elif a == 3:
    print("Du hast 3 Zahlen richtig!")
    print("Du gewinnst 15 Euro!")
elif a == 4:
    print("Du hast 4 Zahlen richtig!")
    print("Du gewinnst 75,90 Euro!")  
elif a == 5:  
    print("Du hast 5 Zahlen richtig!")
    print("Du gewinnst 6257,80 Euro!")
elif a == 6:
    print("Du hast 6 Zahlen richtig!")
    print("Du gewinnst 1 Million Euro!")
else:
    print("Leider kein Gewinn.")
input("Drücke Enter zum Beenden...")