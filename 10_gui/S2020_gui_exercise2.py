""" Opgave "GUI step 2":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2020.png

Genbrug din kode fra "GUI step 1".

GUI-strukturen bør være som følger:
    main window
        labelframe
            frame
                labels and entries
            frame
                buttons

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""
import tkinter as tk

def empty_entry():
    print("button_1 was pressed")
    IdEntry.delete(0, tk.END)
    WeightEntry.delete(0, tk.END)
    DestinationEntry.delete(0, tk.END)
    WeatherEntry.delete(0, tk.END)

padx = 8
pady = 4

main_window = tk.Tk()
main_window.title('GUI step 1')
main_window.geometry("370x150")
#350x150


labelframe1 = tk.LabelFrame(main_window, text="Container")
labelframe1.grid(row=0, column=0, padx=padx, pady=pady)

IdLabel = tk.Label(labelframe1, text="Id")
IdLabel.grid(row=0, column=0, padx=padx, pady=pady)

WeightLabel = tk.Label(labelframe1, text="Weight")
WeightLabel.grid(row=0, column=1, padx=padx, pady=pady)

DestinationLabel = tk.Label(labelframe1, text="Destination")
DestinationLabel.grid(row=0, column=2, padx=padx, pady=pady)

WeatherLabel = tk.Label(labelframe1, text="Weather")
WeatherLabel.grid(row=0, column=3, padx=padx, pady=pady)

IdEntry = tk.Entry(labelframe1, width=5, justify="right")
IdEntry.grid(row=1, column=0, padx=padx, pady=pady)

WeightEntry = tk.Entry(labelframe1, width=8, justify="right")
WeightEntry.grid(row=1, column=1, padx=padx, pady=pady)

DestinationEntry = tk.Entry(labelframe1, width=13, justify="right")
DestinationEntry.grid(row=1, column=2, padx=padx, pady=pady)

WeatherEntry = tk.Entry(labelframe1, width=10, justify="right")
WeatherEntry.grid(row=1, column=3, padx=padx, pady=pady)


CreateButton = tk.Button(labelframe1, text="Create")
CreateButton.grid(row=2, column=0, padx=padx, pady=pady)

UpdateButton = tk.Button(labelframe1, text="Update")
UpdateButton.grid(row=2, column=1, padx=padx, pady=pady)

DeleteButton = tk.Button(labelframe1, text="Delete")
DeleteButton.grid(row=2, column=2, padx=padx, pady=pady)

ClearButton = tk.Button(labelframe1, text="Clear Entry Boxes", command=empty_entry)
ClearButton.grid(row=2, column=3, padx=padx, pady=pady)

# empty_entry_button = tk.Button(main_window, text="Click me, I am a button", command=empty_entry)
# empty_entry_button.grid(row=0, column=1, padx=padx, pady=pady)


if __name__ == "__main__":  # Executed only when this file is run.
    main_window.mainloop()  # Wait for button clicks and act upon them
