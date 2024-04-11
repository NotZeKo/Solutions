"""Opgave: Objektorienteret rollespil, afsnit 1 :

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Del 1:
    Definer en klasse "Character" med attributterne "name", "max_health", "_current_health", "attackpower".
    _current_health skal være en protected attribut, det er ikke meningen at den skal kunne ændres udefra i klassen.

Del 2:
    Tilføj en konstruktor (__init__), der accepterer klassens attributter som parametre.

Del 3:
    Tilføj en metode til udskrivning af klasseobjekter (__repr__).

Del 4:
    Tilføj en metode "hit", som reducerer _current_health af en anden karakter med attackpower.
    Eksempel: _current_health=80 og attackpower=10: et hit reducerer _current_health til 70.
    Metoden hit må ikke ændre den private attribut _current_health i en (potentielt) fremmed klasse.
    Definer derfor en anden metode get_hit, som reducerer _current_health for det objekt, som den tilhører, med attackpower.

Del 5:
    Tilføj en klasse "Healer", som arver fra klassen Character.
    En healer har attackpower=0 men den har en ekstra attribut "healpower".

Del 6:
    Tilføj en metode "heal" til "Healer", som fungerer som "hit" men forbedrer sundheden med healpower.
    For at undgå at "heal" forandrer den protected attribut "_current_health" direkte,
    tilføj en metode get_healed til klassen Character, som fungerer lige som get_hit.

Hvis du er gået i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).
Hvis du ikke aner, hvordan du skal begynde, kan du åbne S0720_rpg1_help.py og starte derfra.

Når dit program er færdigt, skal du skubbe det til dit github-repository
og sammenlign det med lærerens løsning i S0730_rpg1_solution.py

Send derefter denne Teams-besked til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

class Character:
    def __init__(self, name, max_health, _current_health, attackpower, heal_power=0):
        self.name = name
        self.max_health = max_health
        self._current_health = _current_health
        self.attackpower = attackpower
        self.heal_power = heal_power



    def __repr__(self):
        return f'Name: {self.name}\nCurrent Health: {self._current_health}\\{self.max_health}\nAttackpower: {self.attackpower}\n'

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

class Healer(Character):
    def __init__(self, name, max_health, _current_health, attack_power, heal_power):
        super().__init__(name, max_health, _current_health, attack_power)
        self.heal_power = heal_power

    def heal(self, character_heal):
        character_heal.get_healed(self.heal_power)

kaneki = Healer("Kaneki", 120, 120, 0, 31)
tara = Character("Tara", 100, 100, 10)
masuke = Character("Masuke", 130, 130, 13)

print(kaneki)
print(tara)
masuke.hit(tara)
print(masuke)
print(tara)
kaneki.heal(tara)
print(tara)



