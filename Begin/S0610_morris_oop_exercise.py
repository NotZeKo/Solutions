"""
Opgave "Morris The Miner" (denne gang objekt orienteret)

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Genbrug din oprindelige Morris-kode og omskriv den til en objektorienteret version.

Definer en klasse Miner med attributter som sleepiness, thirst osv.
og metoder som sleep, drink osv.
Opret Morris og initialiser hans attributter ved at kalde konstruktoren for Miner:
morris = Miner()

Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

class Miner:
    # morris = {"turn": 0, "sleepiness": 0, "thirst": 0, "hunger": 0, "whisky": 0, "gold": 0}  # dictionary

    def __init__(self, turn=0,  sleepiness=0, thirst=0, hunger=0, buy_whiskey=0, gold=0):
        self.turn = turn
        self.sleepiness = sleepiness
        self.thirst = thirst
        self.hunger = hunger
        self.gold = gold
        self.whiskey = buy_whiskey

    def sleep(self):
        self.sleepiness -= 10
        self.thirst += 1
        self.hunger += 1

    def mine(self):
        self.sleepiness += 5
        self.thirst += 5
        self.hunger += 5
        self.gold += 5

    def eat(self):
        self.sleepiness += 5
        self.thirst -= 5
        self.hunger -= 20
        self.gold -= 2

    def buy_whiskey(self):
        self.sleepiness += 5
        self.thirst += 1
        self.hunger += 1
        self.gold -= 1

    def drink(self):
        self.sleepiness += 5
        self.thirst -= 15
        self.hunger -= 1
        self.gold += 0

    def dead(self):
        return self.sleepiness > 100 or self.thirst > 100 or self.hunger > 100

    def __str__(self):
        return f"Turn: {self.turn}, Sleepiness: {self.sleepiness}, Thirst: {self.thirst}, Hunger: {self.hunger}, Gold: {self.gold}, Whiskey: {self.whiskey}"




class colors: #Dette var chatgpt der tilføjede farve fordi jeg syntes det kunne være sjovt/fedt :3
    RESET = "\033[0m"
    RED = "\033[91m"



morris = Miner()

print(morris)
while not morris.dead() and morris.turn < 1000:
    morris.turn += 1
    print(morris)
    if morris.thirst > 80:
        morris.buy_whiskey()
        morris.turn += 1
        morris.drink()
    elif morris.sleepiness > 88:
        morris.sleep()
    elif morris.hunger > 80:
        morris.eat()
    else:
        morris.mine()
if morris.sleepiness > 100:
    print("Morris got too tired")
    print(colors.RED + "TRY AGAIN" + colors.RESET)
elif morris.thirst > 100 and morris.hunger > 100:
    print("Morris got too thirsty and hungry")
    print(colors.RED + "TRY AGAIN" + colors.RESET)
elif morris.hunger > 100:
    print("Morris got too hungry")
    print(colors.RED + "TRY AGAIN" + colors.RESET)
elif morris.thirst > 100:
    print("Morris got too thirsty")
    print(colors.RED + "TRY AGAIN" + colors.RESET)



