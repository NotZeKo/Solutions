"""
Opgave "Tom the Turtle":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Funktionen "demo" introducerer dig til alle de kommandoer, du skal bruge for at interagere med Tom i de følgende øvelser.

Kun hvis du er nysgerrig og elsker detaljer:
    Her er den fulde dokumentation for turtle graphics:
    https://docs.python.org/3.3/library/turtle.html

Del 1:
    Skriv en funktion "square", som accepterer en parameter "length".
    Hvis denne funktion kaldes, får skildpadden til at tegne en firkant med en sidelængde på "længde" pixels.

Del 2:
     Færdiggør funktionen "visible", som skal returnere en boolsk værdi,
     der angiver, om skildpadden befinder sig i det synlige område af skærmen.
     Brug denne funktion i de følgende dele af denne øvelse
     til at få skildpadden tilbage til skærmen, når den er vandret væk.

Del 3:
    Skriv en funktion "many_squares" med en for-loop, som kalder square gentagne gange.
    Brug denne funktion til at tegne flere firkanter af forskellig størrelse i forskellige positioner.
    Funktionen skal have nogle parametre. F.eks:
        antal: hvor mange firkanter skal der tegnes?
        størrelse: hvor store er firkanterne?
        afstand: hvor langt væk fra den sidste firkant er den næste firkant placeret?

Del 4:
    Skriv en funktion, der producerer mønstre, der ligner dette:
    https://pixabay.com/vectors/spiral-square-pattern-black-white-154465/

Del 5:
    Skriv en funktion, der producerer mønstre svarende til dette:
    https://www.101computing.net/2d-shapes-using-python-turtle/star-polygons/
    Funktionen skal have en parameter, som påvirker mønsterets form.

Del 6:
    Opret din egen funktion, der producerer et sejt mønster.
    Senere, hvis du har lyst, kan du præsentere dit mønster på storskærmen for de andre.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""

import turtle  # this imports a library called "turtle". A library is (someone else's) python code, that you can use in your own program.

# Opgave 2
# def visible(tom):
#     if tom.position()[0] > 480 or tom.position()[0] < -480:
#         tom.home()
#     if tom.position()[1] > 480 or tom.position()[1] < -480:
#         tom.home()
#         return True
#     else:
#         return False



# Opgave 3
# def many_squares(antal, size, afstand):
#     for x in range(antal):
#         square(size)
#         turtle.penup()
#         turtle.forward(afstand)
#         turtle.pendown()
#
# def square(size):
#     for x in range(4):
#         turtle.forward(size)
#         turtle.left(90)
#
# many_squares(20, 20, 50)

# Opgave 1-2
# def demo(lenght, squares, distance):
#     tom = turtle.Turtle()
#     print(type(tom))
#     tom.speed(3)
#     if tom.position()[0]:
#         tom.left(180)
#     for x in range(squares):
#         if visible(tom) == True:
#             return
#         tom.forward(lenght)
#         tom.left(90)
#     turtle.done()
# demo(75, 4, 100)


# Opgave 4
# def monster(lenght):
#     tom = turtle.Turtle()
#     print(type(tom))
#     tom.speed(5)
#     for x in range(33):
#         tom.forward(lenght)
#         tom.left(90)
#         lenght -= 10
#     turtle.done()
#
# monster(333)





# Opgave 6
# def sej_star(lenght):
#     tom = turtle.Turtle()
#     print(type(tom))
#     tom.speed(7)
#     for z in range(12):
#         tom.pensize(4)
#         tom.pencolor("red")
#         tom.left(180)
#         tom.left(30)
#         tom.forward(lenght)
#         tom.right(120)
#         tom.forward(lenght)
#         tom.right(120)
#         tom.forward(lenght)
#
#     turtle.done()
# sej_star(100)

# Opgave 5
# def draw_star(points):
#     tom = turtle.Turtle()
#     print(type(tom))
#     tom.speed(7)
#     if points % 2 == 0:
#         for x in range(points):
#             tom.pencolor("green")
#             tom.pensize(3)
#             tom.forward(100)
#             tom.left(-1080 / points)
#     else:
#         for x in range(points):
#             tom.pencolor("red")
#             tom.pensize(3)
#             tom.forward(100)
#             tom.left(-1080/points)
#
#
#
#
# draw_star(13)
