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

def ShowPlot(fig):
    for widget in frame3.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
#Asignamos para cada funcion donde se nos muestre una grafica dentro de una funciona que se dedica a ajustar estas funciones dentro del marco disponible
#esto es para que podamos ver bien toda la grafica problema comentado en la version 2 pero encontramos una solucion aun mejor que es esta


def PlotAp():
    ShowPlot(PlotAirports(LoadAirports()))
def PlotAl():
    ShowPlot(PlotAirlines(LoadArrivals()))
def PlotArrRate():
    ShowPlot(PlotArrivals(LoadArrivals()))
def PlotFlTy():
    ShowPlot(PlotFlightsType(LoadArrivals()))
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
    result = LoadAirportStructure("Terminals.txt")
    if result == -1:
        messagebox.showerror("Error", "Terminals.txt not found")
        return
    bcn = result
    messagebox.showinfo("Success", "Airport structure loaded successfully")
def ShowOccupancy():
    global bcn
    if bcn == None:
        messagebox.showerror("Error", "Load airport structure first")
        return
    occupancy = GateOccupancy(bcn)
    canvas = FigureCanvasTkAgg( GateOccupancy(), master=frame3)
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

def CheckIsAirlineInTerminal():
    global bcn
    if bcn == None:
        messagebox.showerror("Error", "Load airport structure first")
        return
    t_name = terminal_entry.get()
    airline_code = airline_entry.get()
    terminal_obj = ()
    i = 0
    while i < len(bcn.terminals):
        if bcn.terminals[i].name == t_name:
            terminal_obj = bcn.terminals[i]
        i = i + 1
    if terminal_obj == None:
        messagebox.showerror("Error", "Terminal not found")
        return
    result = IsAirlineInTerminal(terminal_obj , airline_code)
    if result == True:
        messagebox.showinfo("Result", airline_code + " IS in terminal " + t_name)
    else:
        messagebox.showinfo("Result", airline_code + " is NOT in terminal " + t_name)
def AssignGateUI():
    global bcn
    if bcn == None:
        messagebox.showerror("Error", "Load airport structure first")
        return
    aircraft_id = aircraft_entry.get()
    if aircraft_id == "":
        messagebox.showerror("Error", "Enter an aircraft ID")
        return
    arrivals = LoadArrivals()
    target = None
    i = 0
    while i < len(arrivals):
        if arrivals[i].id == aircraft_id:
            target = arrivals[i]
        i = i + 1
    if target == None:
        messagebox.showerror("Not Found", "Aircraft " + aircraft_id + " not found in Arrivals.txt")
        return
    result = AssignGate(bcn, target)
    if result == -1:
        messagebox.showerror("Failed", "No free gate available for " + aircraft_id)
        return
    gate_name = ""
    t = 0
    while t < len(bcn.terminals):
        a = 0
        while a < len(bcn.terminals[t].areas):
            g = 0
            while g < len(bcn.terminals[t].areas[a].gates):
                if bcn.terminals[t].areas[a].gates[g].ID == aircraft_id:
                    gate_name = bcn.terminals[t].areas[a].gates[g].name
                g = g + 1
            a = a + 1
        t = t + 1
    messagebox.showinfo("Gate Assigned", "Aircraft: " + aircraft_id + "\nAirline: " + target.company + "\nOrigin: " + target.origin + "\nGate: " + gate_name)


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
Button(frame4, text="Load Airport Structure",  command=LoadAP,        bg='#7c3aed', fg="white", font=FONT_B).grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame4, text="Show Gate Occupancy",     command=ShowOccupancy, bg='#7c3aed', fg="white", font=FONT_B).grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Label(frame4, text="Terminal (e.g. T1):",      bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=2, column=0, sticky="w", padx=5)
terminal_entry = Entry(frame4, width=10, font=FONT, bg='#c084fc')
terminal_entry.grid(row=2, column=1, padx=5, pady=3, sticky="ew")
Label(frame4, text="Airline ICAO (e.g. VLG):", bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=3, column=0, sticky="w", padx=5)
airline_entry = Entry(frame4, width=10, font=FONT, bg='#c084fc')
airline_entry.grid(row=3, column=1, padx=5, pady=3, sticky="ew")
Button(frame4, text="Is Airline in Terminal?",     command=CheckIsAirlineInTerminal, bg='#7c3aed', fg="white", font=FONT_B).grid(row=4, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame4, text="Search Terminal for Airline", command=SearchAirline,            bg='#7c3aed', fg="white", font=FONT_B).grid(row=5, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Label(frame4, text="Aircraft ID (e.g. ECMKV):",   bg="#2a2a3d", fg="#c084fc", font=FONT).grid(row=6, column=0, sticky="w", padx=5)
aircraft_entry = Entry(frame4, width=10, font=FONT, bg='#c084fc')
aircraft_entry.grid(row=6, column=1, padx=5, pady=3, sticky="ew")
Button(frame4, text="Assign Gate to Aircraft",     command=AssignGateUI,             bg='#7c3aed', fg="white", font=FONT_B).grid(row=7, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")


root.mainloop()
