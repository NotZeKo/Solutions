"""
Opgave "GUI step 1":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2010.png

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import tkinter as tk


padx = 8
pady = 4

main_window = tk.Tk()
main_window.title('GUI step 1')
main_window.geometry("100x120")


frame_1 = tk.LabelFrame(main_window, text="Container")
frame_1.grid(row=0, column=0, padx=padx, pady=pady)

myLabel1 = tk.Label(frame_1, text="Id")
myLabel1.grid(row=0, column=0, padx=padx, pady=pady)

myEntry = tk.Entry(frame_1, width=2, justify="right")
myEntry.grid(row=1, column=0, padx=padx, pady=pady)

myButton1 = tk.Button(frame_1, text="Create")
myButton1.grid(row=2, column=0, padx=padx, pady=pady)




if __name__ == "__main__":  # Executed only when this file is run.
    main_window.mainloop()  # Wait for button clicks and act upon them