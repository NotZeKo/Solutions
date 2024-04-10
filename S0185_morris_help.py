"""
Opgave "Morris the Miner":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Udgangssituation:
Morris har egenskaberne sleepiness, thirst, hunger, whisky, gold.
Alle attributter har startværdien 0.

Regler:
Hvis sleepiness, thirst eller hunger kommer over 100, dør Morris.
Morris kan ikke opbevare mere end 10 flasker whisky.
Ingen attribut kan gå under 0.

Ved hver omgang kan Morris udføre præcis én af disse aktiviteter:
sleep:      sleepiness-=10, thirst+=1,  hunger+=1,  whisky+=0, gold+=0
mine:       sleepiness+=5,  thirst+=5,  hunger+=5,  whisky+=0, gold+=5
eat:        sleepiness+=5,  thirst-=5,  hunger-=20, whisky+=0, gold-=2
buy_whisky: sleepiness+=5,  thirst+=1,  hunger+=1,  whisky+=1, gold-=1
drink:      sleepiness+=5,  thirst-=15, hunger-=1,  whisky-=1, gold+=0

Din opgave:
Skriv et program, der giver Morris så meget guld som muligt på 1000 omgange.

Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

class colors: #Dette var chatgpt der tilføjede farve fordi jeg syntes det kunne være sjovt/fedt :3
    RESET = "\033[0m"
    RED = "\033[91m"
def sleep():
    morris["sleepiness"] -= 10  # update sleepiness
    morris["thirst"] += 1 # update thirts
    morris["hunger"] +=1 # update hunger
    # check for values out of boundaries
def mine():
    morris["sleepiness"] += 5  # update sleepiness
    morris["thirst"] += 5 # update thirts
    morris["hunger"] +=5 # update hunger
    morris["gold"] +=5 # update gold

def eat():
    morris["sleepiness"] += 5  # update sleepiness
    morris["thirst"] -= 5  # update thirts
    morris["hunger"] -= 20  # update hunger
    morris["gold"] -= 2  # update gold

def buy_whiskey():
    morris["sleepiness"] += 5  # update sleepiness
    morris["thirst"] -= 15  # update thirts
    morris["hunger"] += 1  # update hunger
    morris["gold"] -= 1  # update gold

def drink():
    morris["sleepiness"] += 5  # update sleepiness
    morris["thirst"] -= 15  # update thirts
    morris["hunger"] -= 1  # update hunger
    morris["gold"] += 0  # update gold





def dead():
    return morris["sleepiness"] > 100 or morris["thirst"] > 100 or morris["hunger"] > 100


morris = {"turn": 0, "sleepiness": 0, "thirst": 0, "hunger": 0, "whisky": 0, "gold": 0}  # dictionary



while not dead() and morris["turn"] < 1000:
    morris["turn"] += 1
    print(morris)
    mine()
    if morris["sleepiness"] > 90:
        sleep()
    if morris["thirst"] > 90:
        drink()
    if morris["hunger"] > 90:
        eat()
if morris["sleepiness"] > 100:
    print("Morris got too tired")
    print(colors.RED + "TRY AGAIN" + colors.RESET)
elif morris["thirst"] > 100 and morris["hunger"] > 100:
    print("Morris got too thirsty and hungry")
    print(colors.RED + "TRY AGAIN" + colors.RESET)
elif morris["hunger"] > 100:
    print("Morris got too hungry")
    print(colors.RED + "TRY AGAIN" + colors.RESET)
elif morris["thirst"] > 100:
    print("Morris got too thirsty")
    print(colors.RED + "TRY AGAIN" + colors.RESET)



