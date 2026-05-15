import os
import sys
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from airport import *
from aircraft import *
from LEBL import *

try:
    f = open("Airports.txt", "r")
    f.close()
except FileNotFoundError:
    messagebox.showerror("Error", "No Airports file found.\nPlease download Airports.txt")
    sys.exit(1)

root = Tk()
root.title("Airport Management")
root.configure(bg='#2a2a3d', padx=15, pady=15)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=2)
root.rowconfigure(3, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

FONT = ("Segoe UI", 10)
FONT_B = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 11, "bold")

bcn = None

def PlotAp():
    canvas = FigureCanvasTkAgg(PlotAirports(LoadAirports()), master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
def PlotAl():
    canvas = FigureCanvasTkAgg(PlotAirlines(LoadArrivals()), master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
def PlotArrRate():
    canvas = FigureCanvasTkAgg(PlotArrivals(LoadArrivals()), master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
def PlotFlTy():
    canvas = FigureCanvasTkAgg(PlotFlightsType(LoadArrivals()), master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
def MapAp():
    MapAirports(LoadAirports())
    os.system("Start Airports.kml")
def MapFl():
    MapFlights(LoadArrivals())
    os.system("Start Flights.kml")
def MapFlLong():
    MapFlights(LongDistanceArrivals(LoadArrivals()))
    os.system("Start Flights.kml")
def Save():
    try:
        if (latitude.get() == "") or (longitude.get() == ""):
            messagebox.showerror("Error", "Check coordinates")
            return
        a = Airport()
        a.icao = icao.get()
        a.latitude = ConvertCoordinates(latitude.get())
        a.longitude = ConvertCoordinates(longitude.get())
        SetSchengen(a)
        result = SaveSchengenAirports(a)
        if result == True:
            messagebox.showerror("Error", "Airport Already on the List")
            return
        elif result == False:
            messagebox.showerror("Error", "Check Airport Format")
        else:
            messagebox.showinfo("Success", "Airport Added Successfully")
    except ValueError:
        messagebox.showerror("Error", "No Airports found.\n Please input a valid Airport")
        return
def Add():
    try:
        if (latitude.get() == "") or (longitude.get() == ""):
            messagebox.showerror("Error", "Check coordinates")
            return
        a = Airport()
        a.icao = icao.get()
        a.latitude = ConvertCoordinates(latitude.get())
        a.longitude = ConvertCoordinates(longitude.get())
        if (a.latitude == "") or (a.longitude == ""):
            messagebox.showerror("Error", "Check coordinates")
            return
        SetSchengen(a)
        result = AddAirport(a)
        if result == True:
            messagebox.showerror("Error", "Airport Already on the List")
            return
        elif result == False:
            messagebox.showerror("Error", "Check Airport Format")
            return
        else:
            messagebox.showinfo("Success", "Airport Added Successfully")
    except ValueError:
        messagebox.showerror("Error", "No Airports found.\n Please input a valid Airport")
        return
def Remove():
    if icao.get() == "":
        messagebox.showerror("Error", "Check code")
        return
    airport = icao.get()
    RemoveAirport(LoadAirports(), airport)
    messagebox.showinfo("Success", "Airport Removed Successfully")

def LoadAP():
    global bcn
    result = LoadAirportStructure("LEBL.txt")
    if result == -1:
        messagebox.showerror("Error", "LEBL.txt not found")
        return
    bcn = result
    messagebox.showinfo("Success", "Airport structure loaded successfully")
def ShowOccupancy():
    global bcn
    if bcn == None:
        messagebox.showerror("Error", "Load airport structure first")
        return
    occupancy = GateOccupancy(bcn)
    canvas = FigureCanvasTkAgg(PlotGateOccupancy(occupancy), master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
def SearchAirline():
    global bcn
    if bcn == None:
        messagebox.showerror("Error", "Load airport structure first")
        return
    name = airline_entry.get()
    if name == "":
        messagebox.showerror("Error", "Enter an airline name")
        return
    terminal_name = SearchTerminal(bcn, name)
    if terminal_name == "":
        messagebox.showerror("Not found", name + " not found in any terminal")
    else:
        messagebox.showinfo("Terminal found", name + " boards at terminal " + terminal_name)

Label(root, text="Airport Management", bg='#2a2a3d', fg='#c084fc', font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

frame1 = LabelFrame(root, text="Existing File Operations", font=FONT_TITLE)
frame1.configure(bg='#2a2a3d', fg="#c084fc")
frame1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
frame1.columnconfigure(0, weight=1)
Button(frame1, text="Plot Airports",              command=PlotAp,     bg='#7c3aed', fg="white", font=FONT_B).grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot Arrivals by type",      command=PlotFlTy,   bg='#7c3aed', fg="white", font=FONT_B).grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot Airlines",              command=PlotAl,     bg='#7c3aed', fg="white", font=FONT_B).grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot Arrivals",              command=PlotArrRate, bg='#7c3aed', fg="white", font=FONT_B).grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map Airports",               command=MapAp,      bg='#7c3aed', fg="white", font=FONT_B).grid(row=7, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map Arrivals",               command=MapFl,      bg='#7c3aed', fg="white", font=FONT_B).grid(row=8, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map Long Distance Arrivals", command=MapFlLong,  bg='#7c3aed', fg="white", font=FONT_B).grid(row=9, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

frame2 = LabelFrame(root, text="Add / Save / Remove:", font=FONT_TITLE)
frame2.configure(bg='#2a2a3d', fg="#c084fc")
frame2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
frame2.columnconfigure(0, weight=1)
Label(frame2, text="Enter Airport:",               bg="#2a2a3d", fg="#c084fc", font=FONT_B).grid(row=0, column=0, columnspan=2)
Label(frame2, text="ICAO code: (e.g. 'LEBL.txt')",    bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=1, column=0)
icao = Entry(frame2, width=40, font=FONT, bg='#c084fc')
icao.grid(row=1, column=1, padx=5, pady=5)
Label(frame2, text="Latitude: (e.g. 'N411749')",   bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=2, column=0)
latitude = Entry(frame2, width=40, font=FONT, bg='#c084fc')
latitude.grid(row=2, column=1, padx=5, pady=5)
Label(frame2, text="Longitude: (e.g. 'E0020442')", bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=3, column=0)
longitude = Entry(frame2, width=40, font=FONT, bg='#c084fc')
longitude.grid(row=3, column=1, padx=5, pady=5)
Button(frame2, text="Save Schengen Airports Only", command=Save,   bg="#7c3aed", fg="white", font=FONT_B).grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame2, text="Add Airport list to File",    command=Add,    bg="#7c3aed", fg="white", font=FONT_B).grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame2, text="Remove Airport",              command=Remove, bg="#7c3aed", fg="white", font=FONT_B).grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

frame3 = LabelFrame(root, text="Figure Visualizer", font=FONT_TITLE)
frame3.configure(bg='#2a2a3d', fg="#c084fc")
frame3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
frame3.rowconfigure(0, weight=1)
frame3.columnconfigure(0, weight=1)
Label(frame3, text="Press any 'Plot' button to display", bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=0, column=0)

frame4 = LabelFrame(root, text="Airport Operations", font=FONT_TITLE)
frame4.configure(bg='#2a2a3d', fg="#c084fc")
frame4.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
frame4.columnconfigure(0, weight=1)
frame4.columnconfigure(1, weight=1)
Button(frame4, text="Load Airport Structure", command=LoadAP,        bg='#7c3aed', fg="white", font=FONT_B).grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame4, text="Show Gate Occupancy",    command=ShowOccupancy, bg='#7c3aed', fg="white", font=FONT_B).grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Label(frame4,  text="Airline name:",          bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=2, column=0, padx=5, pady=5)
airline_entry = Entry(frame4, width=20, font=FONT, bg='#c084fc')
airline_entry.grid(row=2, column=1, padx=5, pady=5)
Button(frame4, text="Search Terminal",        command=SearchAirline, bg='#7c3aed', fg="white", font=FONT_B).grid(row=3, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

root.mainloop()
