"""opgave: Objektorienteret rollespil, afsnit 2 :

Som altid skal du læse hele øvelsesbeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Byg videre på din løsning af afsnit 1.

Del 1:
    Opfind to nye klasser, som arver fra klassen Character. For eksempel Hunter og Magician.
    Dine nye klasser skal have deres egne ekstra metoder og/eller attributter.
    Måske overskriver de også metoder eller attributter fra klassen Character.

Del 2:
    Lad i hovedprogrammet objekter af dine nye klasser (dvs. rollespilfigurer) kæmpe mod hinanden,
    indtil den ene figur er død. Udskriv, hvad der sker under kampen.

I hver omgang bruger en figur en af sine evner (metoder). Derefter er det den anden figurs tur.
Det er op til dig, hvordan dit program i hver tur beslutter, hvilken evne der skal bruges.
Beslutningen kan f.eks. være baseret på tilfældighed eller på en smart strategi

Del 3:
    Hver gang en figur bruger en af sine evner, skal du tilføje noget tilfældighed til den anvendte evne.

Del 4:
    Lad dine figurer kæmpe mod hinanden 100 gange.
    Hold styr på resultaterne.
    Prøv at afbalancere dine figurers evner på en sådan måde, at hver figur vinder ca. halvdelen af kampene.

Hvis du går i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-besked til din lærer: <filename> done
Fortsæt derefter med den næste fil."""

import random


class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    GREY = "\033[90m"
    DARK_RED = "\033[31m"
    ORANGE = "\033[38;5;208m"


class Character:
    def __init__(self, name, max_health, _current_health, attackpower=0, heal_power=0, fire_damage=0):
        self.name = name
        self.max_health = max_health
        self._current_health = _current_health
        self.attackpower = attackpower
        self.heal_power = heal_power
        self.fire_damage = fire_damage

    def __repr__(self):
        return f'Name: {Color.GREY}{self.name}{Color.RESET}\nCurrent Health:{Color.GREEN} {self._current_health}\\{self.max_health}{Color.RESET}\nAttackpower: {Color.DARK_RED}{self.attackpower}{Color.RESET}\nFire power: {Color.ORANGE}{self.fire_damage}{Color.RESET}\n'

    def hit(self, other):
        self.attackpower = random.randint(10, 15)
        print(f'{Color.GREEN}{self.name}{Color.RESET} hit {other.name} for {Color.DARK_RED}{self.attackpower} Physical{Color.DARK_RED} DMG{Color.RESET}\n')
        other.get_hit(self.attackpower)

    def get_hit(self, attackpower):
        self._current_health -= attackpower

    def get_healed(self, amount):
        print(f'{self.name} healed for {amount}HP')
        self._current_health += amount
        if self._current_health > self.max_health:
            print(f"{self.name} is at max health and can't heal further\n")
            self._current_health = self.max_health

    def fire_hit(self, amount):
        print(f'{self.name} took {amount} fire damage')
        self._current_health -= amount

    def fight_hit(self, amount):
        print(f'{self.name} took {amount} fighting damage')
        self._current_health -= amount

    def dead(self):
        return self._current_health <= 0


class Healer(Character):
    def __init__(self, name, max_health, _current_health, attackpower, heal_power):
        super().__init__(name, max_health, _current_health, attackpower, )
        self.heal_power = heal_power

    def heal(self, character_heal):
        character_heal.get_healed(self.heal_power)


class Mage(Character):
    def __init__(self, name, max_health, _current_health, attackpower=0, fire_damage=0):
        super().__init__(name, max_health, _current_health, attackpower)
        self.fire_damage = fire_damage

    def fire_attack(self, other):
        self.fire_damage = random.randint(10,15)
        print(f'{Color.GREEN}{self.name}{Color.RESET} hit {other.name} for {Color.ORANGE}{self.fire_damage} Fire DMG{Color.RESET}\n')
        other.fire_hit(self.fire_damage)

class Brawler(Character):
    def __init__(self, name, max_health, _current_health, attackpower=0, fight_damage=0):
        super().__init__(name, max_health, _current_health, attackpower)
        self.fight_damage = fight_damage

    def fight_attack(self, other):
        self.fight_damage = random.randint(10, 15)
        print(f'{Color.GREEN}{self.name}{Color} hit {other.name} for {Color.RED} Fighting DMG{Color.RESET}\n')
        other.fight_hit(self.fight_attack)

# kaneki = Healer("Kaneki", 120, 120, 0, 20)
tara = Mage('Tara', 100, 100)
masuke = Brawler('Masuke', 100, 100)
# tara = Character("Tara", 100, 100, random.randint(10, 15))
# masuke = Character("Masuke", 100, 100, random.randint(10, 15))
turn = 0
fire_cooldown = 0 #Lav videre på cooldown
tara_win = 0
masuke_win = 0
print(tara)
print(masuke)
while turn < 1000:
    turn += 1
    print(f"Turn: {Color.BLUE}{turn}{Color.RESET}\n")
    if tara.dead():
        print(f"{Color.RED}Tara has died in turn: {turn}{Color.RESET}")
        masuke_win += 1
        print(f"Masuke has won {masuke_win} times")
        tara._current_health = tara.max_health
        masuke._current_health = masuke.max_health

    if masuke.dead():
        print(f"{Color.RED}Masuke has died in turn: {turn}{Color.RESET}")
        tara_win += 1
        print(tara_win)
        masuke._current_health = masuke.max_health
        tara._current_health = tara.max_health

    attackpower = random.randint(10, 20)

    if turn % 2 == 0:
        tara.fire_attack(masuke)
        print(masuke)
    else:
        masuke.hit(tara)
        print(tara)

if turn == 1000:
    print(f"After {Color.BLUE}{turn}{Color.RESET} turns\n{Color.RED}Masuke{Color.RESET} has won {Color.GREEN}{masuke_win}{Color.RESET} times\n{Color.RED}Tara{Color.RESET} has won {Color.GREEN}{tara_win}{Color.RESET} times")