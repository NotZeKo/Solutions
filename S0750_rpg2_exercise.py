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

class Character:
    def __init__(self, name, max_health, _current_health, attackpower, heal_power=0, turn=1):
        self.name = name
        self.max_health = max_health
        self._current_health = _current_health
        self.attackpower = attackpower
        self.heal_power = heal_power
        self.turn = turn



    def __repr__(self):
        return f'Turn: {self.turn}\nName: {self.name}\nCurrent Health: {self._current_health}\\{self.max_health}\nAttackpower: {self.attackpower}\n'

    def hit(self, other):
        print(f'{self.name} hit {other.name} for {self.attackpower}DMG\n')
        other.get_hit(self.attackpower)
    def get_hit(self, attackpower):
        self._current_health -= attackpower

    def get_healed(self, amount):
        print(f'{self.name} healed for {amount}HP')
        self._current_health += amount
        if self._current_health > self.max_health:
            print(f"{self.name} is at max health and can't heal further\n")
            self._current_health = self.max_health

    def dead(self):
        return self._current_health <= 0

class Healer(Character):
    def __init__(self, name, max_health, _current_health, attack_power, heal_power):
        super().__init__(name, max_health, _current_health, attack_power,)
        self.heal_power = heal_power

    def heal(self, character_heal):
        character_heal.get_healed(self.heal_power)

# kaneki = Healer("Kaneki", 120, 120, 0, 20)
tara = Character("Tara", 100, 100, 10)
masuke = Character("Masuke", 130, 130, 13)

print(tara)
while tara.turn < 10:
    if tara.turn % 2 == 0:
        tara.turn += 1
        tara.hit(masuke)
        print(tara)
    else:
        print(masuke)
        tara.turn += 1





# print(kaneki)
# while not kaneki.dead() and kaneki.turn < 100:
#     kaneki.turn +=1
#     print(kaneki)
#     if tara._current_health <= 80:
#         kaneki.heal(tara)
#     elif kaneki._current_health <= 100:
#         kaneki.heal(kaneki)
# print(tara)
