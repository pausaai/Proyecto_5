from tkinter import *
from airport import *

root = Tk()
root.title("Airport Management")
root.configure(bg='#f5e8c3', padx=15, pady=15)

FONT = ("Helvetica", 10)
FONT_B = ("Helvetica", 10, "bold")
FONT_TITLE = ("Helvetica", 11, "bold")

def load():
    file = entry.get()
    LoadAirports(file)
def plot():
    file = entry.get()
    PlotAirports(file)
def Map():
    file = entry.get()
    MapAirports(file)
def Save():
    file = filename.get()
    airports = icao.get()
    SaveSchengenAirports(airports, file)
def Add():
    file = filename.get()
    airports = icao.get()
    AddAirport(file, airports)
def Remove():
    file = filename.get()
    airport = icao.get()
    RemoveAirport(file, airport)

Label(root, text="Airport Management", bg='#f5e8c3', fg='#ff5c3b', font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

frame1 = LabelFrame(root, text="Existing File Operations", font=FONT_TITLE)
frame1.configure(bg='#f5e8c3', fg="#ff5c3b")
frame1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
Label(frame1, text="Input File: (without '.txt')", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=0, column=0)
entry = Entry(frame1, width=40, font=FONT, bg='#e7ceb1')
entry.grid(row=1, column=0, padx=5, pady=5)
Button(frame1, text="Load", command=load, bg="#d4664b", fg="white", font=FONT_B).grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot", command=plot, bg='#d4664b', fg="white", font=FONT_B).grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map", command=Map,  bg='#d4664b', fg="white", font=FONT_B).grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

frame2 = LabelFrame(root, text="Add / Save / Remove:", font=FONT_TITLE)
frame2.configure(bg='#f5e8c3', fg="#ff5c3b")
frame2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
Label(frame2, text="Enter Airports:", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=0, column=0)
icao = Entry(frame2, width=40, font=FONT, bg='#e7ceb1')
icao.grid(row=1, column=0, padx=5, pady=5)
Label(frame2, text="Enter File Name:", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=2, column=0)
filename = Entry(frame2, width=40, font=FONT, bg='#e7ceb1')
filename.grid(row=3, column=0, padx=5, pady=5)
Button(frame2, text="Save Schengen Airports Only", command=Save, bg="#d4664b", fg="white", font=FONT_B).grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame2, text="Add Airport list to File", command=Add,  bg="#d4664b", fg="white", font=FONT_B).grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame2, text="Remove Airport", command=Remove, bg="#d4664b", fg="white", font=FONT_B).grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

root.mainloop()
