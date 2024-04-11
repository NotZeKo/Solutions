"""
Opgave "Animals"

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Alt, hvad du har brug for at vide for at løse denne opgave, finder du i cars_oop-filerne.

Del 1:
    Definer en klasse ved navn Animal.
    Hvert objekt i denne klasse skal have attributterne name (str), sound (str), height (float),
    weight (float), legs (int), female (bool).
    I parentes står data typerne, dette attributterne typisk har.

Del 2:
    Tilføj til klassen meningsfulde metoder __init__ og __repr__.
    Kald disse metoder for at oprette objekter af klassen Animal og for at udskrive dem i hovedprogrammet.

Del 3:
    Skriv en klassemetode ved navn make_noise, som udskriver dyrets lyd i konsollen.
    Kald denne metode i hovedprogrammet.

Del 4:
    Definer en anden klasse Dog, som arver fra Animal.
    Hvert objekt af denne klasse skal have attributterne tail_length (int eller float)
    og hunts_sheep (typisk bool).

Del 5:
    Tilføj til klassen meningsfulde metoder __init__ og __repr__.
    Ved skrivning af konstruktoren for Dog skal du forsøge at genbruge kode fra klassen Animal.
    Kald disse metoder for at oprette objekter af klassen Hund og for at udskrive dem i hovedprogrammet.

Del 6:
    Kald metoden make_noise på Dog-objekter i hovedprogrammet.

Del 7:
    Skriv en klassemetode ved navn wag_tail for Dog.
    Denne metode udskriver i konsollen noget i stil med
    "Hunden Snoopy vifter med sin 32 cm lange hale"
    Kald denne metode i hovedprogrammet.

Del 8:
    Skriv en funktion mate(mother, father). Begge parametre er af typen Dog.
    Denne funktion skal returnere et nyt objekt af typen Dog.
    I denne funktion skal du lave meningsfulde regler for den nye hunds attributter.
    Hvis du har lyst, brug random numbers så mate() producerer tilfældige hunde.
    Sørg for, at denne funktion kun accepterer hunde med det korrekte køn som argumenter.

Del 9:
    I hovedprogrammet kalder du denne metode og udskriver den nye hund.

Del 10:
    Gør det muligt at skrive puppy = daisy + brutus i stedet for puppy = mate(daisy, brutus)
    for at opnå den samme effekt.  Du bliver nok nødt til at google det først.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import random


class Animal:
    def __init__(self, name, sound, height, weight, legs, female):
        self.name = name
        self.sound = sound
        self.height = height
        self.weight = weight
        self.legs = legs
        self.female = female

    def make_noise(self):
        print(self.sound)

    def __str__(self):
        return f"Name: {self.name}\nSound: {self.sound}\nHeight: {self.height}\nWeight: {self.weight}\nLegs: {self.legs}\nFemale: {self.female}\n"


class Dog(Animal):
    def __init__(self, name, sound, height, weight, legs, female, tail_length, hunts_sheep):
        super().__init__(name, sound, height, weight, legs, female)
        self.tail_length = tail_length
        self.hunts_sheep = hunts_sheep

    def __add__(self, other):
        if isinstance(other, Dog):
            return mate(self, other)
        else:
            raise ValueError("Fejl")

    def make_noise(self):
        print(self.sound)

    def wag_tail(self):
        print(f"{self.name} is wagging with his {self.tail_length} cm long tail")

    def __str__(self):
        return f"\nName: {self.name}\nSound: {self.sound}\nHeight: {self.height}\nWeight: {self.weight}\nLegs: {self.legs}\nFemale: {self.female}\nTail lenght: {self.tail_length}\nHunts sheep: {self.hunts_sheep}"

def mate(mother, father):
    if not isinstance(mother, Dog) or not isinstance(father, Dog):
        raise ValueError("Both dogs be!")
    if mother.female == father.female:
        raise ValueError("Wrong gender")
    child_name = "Jack"
    child_sound = "Bark"
    child_height = random.randint(10, 120)
    child_weight = random.randint(33, 100)
    child_legs = 4
    child_female = random.choice([True, False])
    child_tail_length = random.randint(5, 15)
    child_hunts_sheep = random.choice([True, False])

    child = Dog(child_name, child_sound, child_height, child_weight,
                child_legs, child_female, child_tail_length, child_hunts_sheep)
    return child


# animal = Animal("Lion", "Rooooar", 180, 150, 4, True)
mom = Dog("Mom", "Woof", 180, 150, 4, True, 6, False)
dad = Dog("Dad", "Woof", 180, 150, 4, False, 6, False)
puppy = mom + dad
print(puppy)
