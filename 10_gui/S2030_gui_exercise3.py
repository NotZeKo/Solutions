"""Opgave "GUI step 3":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2030.png

Genbrug din kode fra "GUI step 2".

GUI-strukturen bør være som følger:
    main window
        labelframe
            frame
                treeview and scrollbar
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
from tkinter import ttk

def empty_entry():
    print("button_1 was pressed")
    IdEntry.delete(0, tk.END)
    WeightEntry.delete(0, tk.END)
    DestinationEntry.delete(0, tk.END)
    WeatherEntry.delete(0, tk.END)

padx = 8
pady = 4
rowheight = 24  # rowheight in treeview
treeview_background = "#eeeeee"  # color of background in treeview
treeview_foreground = "black"  # color of foreground in treeview
treeview_selected = "#773333"  # color of selected row in treeview

main_window = tk.Tk()
main_window.title('GUI step 1')
main_window.geometry("900x500")
#350x150

#Main frame
labelframe1 = tk.LabelFrame(main_window, text="Container")
labelframe1.grid(row=0, column=0, padx=padx, pady=pady)

#TreeFrame
TreeFrame = tk.Frame(labelframe1)
TreeFrame.grid(row=0, column=0, padx=padx, pady=pady)

style = ttk.Style()  # Add style
style.theme_use('default')  # Pick theme
style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=rowheight, fieldbackground=treeview_background)
style.map('Treeview', background=[('selected', treeview_selected)])  # Define color of selected row in treeview

tree_1_scrollbar = tk.Scrollbar(TreeFrame)  # create a scrollbar and a treeview
tree_1_scrollbar.grid(row=0, column=1, padx=padx, pady=pady, sticky='ns')
tree_1 = ttk.Treeview(TreeFrame, yscrollcommand=tree_1_scrollbar.set, selectmode="browse")
tree_1.grid(row=0, column=0, padx=0, pady=pady)
tree_1_scrollbar.config(command=tree_1.yview)

tree_1['columns'] = ("col1", "col2", "col3")  # Define treeview columns
tree_1.column("#0", width=0, stretch=tk.NO)
tree_1.column("col1", anchor=tk.E, width=90)
tree_1.column("col2", anchor=tk.W, width=130)
tree_1.column("col3", anchor=tk.W, width=180)

tree_1.heading("#0", text="", anchor=tk.W) # Create treeview column headings
tree_1.heading("col1", text="Id", anchor=tk.CENTER)
tree_1.heading("col2", text="Weight", anchor=tk.CENTER)
tree_1.heading("col3", text="Destination", anchor=tk.CENTER)

#TextFrame
TextFrame = tk.Frame(labelframe1)
TextFrame.grid(row=1, column=0, padx=padx, pady=pady)

IdLabel = tk.Label(TextFrame, text="Id")
IdLabel.grid(row=1, column=0, padx=padx, pady=pady)

WeightLabel = tk.Label(TextFrame, text="Weight")
WeightLabel.grid(row=1, column=1, padx=padx, pady=pady)

DestinationLabel = tk.Label(TextFrame, text="Destination")
DestinationLabel.grid(row=1, column=2, padx=padx, pady=pady)

WeatherLabel = tk.Label(TextFrame, text="Weather")
WeatherLabel.grid(row=1, column=3, padx=padx, pady=pady)

#EntryFrame
EntryFrame = tk.Frame(labelframe1)
EntryFrame.grid(row=2, column=0, padx=padx, pady=pady)

IdEntry = tk.Entry(EntryFrame, width=5, justify="right")
IdEntry.grid(row=2, column=0, padx=padx, pady=pady)

WeightEntry = tk.Entry(EntryFrame, width=8, justify="right")
WeightEntry.grid(row=2, column=1, padx=padx, pady=pady)

DestinationEntry = tk.Entry(EntryFrame, width=13, justify="right")
DestinationEntry.grid(row=2, column=2, padx=padx, pady=pady)

WeatherEntry = tk.Entry(EntryFrame, width=10, justify="right")
WeatherEntry.grid(row=2, column=3, padx=padx, pady=pady)

#ButtonFrame
ButtonFrame = tk.Frame(labelframe1)
ButtonFrame.grid(row=3, column=0, padx=padx, pady=pady)

CreateButton = tk.Button(ButtonFrame, text="Create")
CreateButton.grid(row=3, column=0, padx=padx, pady=pady)

UpdateButton = tk.Button(ButtonFrame, text="Update")
UpdateButton.grid(row=3, column=1, padx=padx, pady=pady)

DeleteButton = tk.Button(ButtonFrame, text="Delete")
DeleteButton.grid(row=3, column=2, padx=padx, pady=pady)

ClearButton = tk.Button(ButtonFrame, text="Clear Entry Boxes", command=empty_entry)
ClearButton.grid(row=3, column=4, padx=padx, pady=pady)

# empty_entry_button = tk.Button(main_window, text="Click me, I am a button", command=empty_entry)
# empty_entry_button.grid(row=0, column=1, padx=padx, pady=pady)


if __name__ == "__main__":  # Executed only when this file is run.
    main_window.mainloop()  # Wait for button clicks and act upon them

