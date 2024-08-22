"""
Opgave "Test pycharm og github":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe.
    I opgaver-projektet skal du klikke på filnavnet i vinduet Project og trykke CTRL+C.
    Skift til løsningsprojektet, klik på hovedmappen i vinduet Project og tryk CTRL+V.

Rediger kun din kopi.

Kør programmet med shift+f10 (eller klik på det grønne "play"-ikon)

I programkoden ændre teksten mellem anførselstegnene

Commit filen til dit eget git-repository (commit betyder: sikkerhedskopier den aktuelle tilstand af dine filer som en ny version)
    Git, Commit (eller klik på det grønne flueben)
    skriv en meningsfuld kommentar
    klik på "commit and push" (push betyder: upload dette commit til github)
    push

Kontroller i din webbrowser på github.com, at den ændrede fil er til stede i dit repository på github.

På GitHub-websiden for dit repository skal du klikke på "Settings" (indstillinger) og sikre dig, at dit repository er offentligt (General, Change repository visibility).

Hvis du ikke allerede har gjort det, skal du sende din lærer url'en til dit github-løsningsrepositorium via Teams-chat.
URL'en ser ud som https://github.com/dit_brugernavn/Solutions.git

Derefter går du videre med den næste fil.
"""


class car1:
    def __init__(self, wheels, speed):
        self.wheels = wheels
        self.speed = speed

    def drive_car(self):
        print(f"Car1 have {self.wheels} wheels and can drive {self.speed}KMH")
        print("Wroooom")
class car2(car1):
    def __init__(self, wheels, speed):
        super().__init__(wheels, speed)

    def drive_car(self):
        print(f"Car2 have {self.wheels} wheels and can drive {self.speed}KMH")
        print("Wroooom")


c1 = car1(4, 200)
c2 = car2(8, 200)
c2.drive_car()
c1.drive_car()
