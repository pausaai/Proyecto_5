import os
import sys
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from aircraft import *
from LEBL import *

try:
    open("Airports.txt", "r").close()
except FileNotFoundError:
    messagebox.showerror("Error", "Airports.txt not found")
    sys.exit(1)

root = Tk()
root.title("Airport Management System")
root.geometry("1450x850")
root.configure(bg="#2a2a3d")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)

FONT_B = ("Segoe UI", 9, "bold")

bcn = None


def ShowPlot(fig, show_filter=False):

    for w in frame3.winfo_children():
        w.destroy()

    frame3.rowconfigure(0, weight=1)

    if show_filter:

        frame3.columnconfigure(0, weight=4)
        frame3.columnconfigure(1, weight=1)

        graph_frame = Frame(frame3, bg="#2a2a3d")
        graph_frame.grid(row=0, column=0, sticky="nsew")

        filter_frame = Frame(frame3, bg="#222233", width=250)
        filter_frame.grid(row=0, column=1, sticky="ns")

        BuildAirlineFilter(filter_frame)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    else:

        frame3.columnconfigure(0, weight=1)

        canvas = FigureCanvasTkAgg(fig, master=frame3)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

selected_airlines = []
all_airlines = []
airline_filter_panel = None
airline_listbox = None
airline_selected_box = None
airline_search_var = None

def OpenAirlineSelector():
    global all_airlines

    data = LoadArrivals()
    all_airlines = sorted(list(set([d.company for d in data])))

    win = Toplevel(root)
    win.title("Airline Filter")
    win.geometry("420x520")
    win.configure(bg="#2a2a3d")

    Label(win, text="Search airline:", bg="#2a2a3d", fg="white").pack(pady=5)

    search_var = StringVar()
    Entry(win, textvariable=search_var, width=35).pack()

    listbox = Listbox(win, height=10, width=40)
    listbox.pack(pady=5)

    Label(win, text="Selected airlines:", bg="#2a2a3d", fg="#c084fc").pack()

    selected_box = Listbox(win, height=6, width=40)
    selected_box.pack(pady=5)

    def refresh_available():
        listbox.delete(0, END)
        q = search_var.get().lower()

        for a in all_airlines:
            if q in a.lower():
                listbox.insert(END, a)

    def refresh_selected():
        selected_box.delete(0, END)
        for s in selected_airlines:
            selected_box.insert(END, s)

    def add():
        try:
            val = listbox.get(listbox.curselection())
            if val not in selected_airlines:
                selected_airlines.append(val)
                refresh_selected()
        except:
            messagebox.showerror("Error", "Select airline")

    def remove():
        try:
            val = selected_box.get(selected_box.curselection())
            selected_airlines.remove(val)
            refresh_selected()
        except:
            messagebox.showerror("Error", "Select selected airline")

    def clear():
        selected_airlines.clear()
        refresh_selected()

    def apply():
        win.destroy()
        PlotAl()

    search_var.trace("w", lambda *args: refresh_available())
    refresh_available()
    refresh_selected()

    Button(win, text="Add →", command=add, width=20).pack(pady=2)
    Button(win, text="← Remove", command=remove, width=20).pack(pady=2)
    Button(win, text="Clear", command=clear, width=20).pack(pady=2)
    Button(win, text="Apply Filter", command=apply, width=25, bg="#7c3aed", fg="white").pack(pady=10)

def PlotAp():
    ShowPlot(PlotAirports(LoadAirports()))

def PlotArrRate():
    ShowPlot(PlotArrivals(LoadArrivals()))

def PlotFlTy():
    ShowPlot(PlotFlightsType(LoadArrivals()))

def PlotAl():

    data = LoadArrivals()

    if len(selected_airlines) == 0:
        filtered = data
    else:
        filtered = [
            d for d in data
            if d.company in selected_airlines
        ]

    ShowPlot(
        PlotAirlines(filtered),
        show_filter=True
    )

def MapAp():
    MapAirports(LoadAirports())
    os.system("start Airports.kml")

def MapFl():
    MapFlights(LoadArrivals())
    os.system("start Flights.kml")

def MapFlLong():
    MapFlights(LongDistanceArrivals(LoadArrivals()))
    os.system("start Flights.kml")

def Save():
    if latitude.get() == "" or longitude.get() == "":
        messagebox.showerror("Error", "Check coordinates")
        return

    a = Airport()
    a.icao = icao.get()
    a.latitude = ConvertCoordinates(latitude.get())
    a.longitude = ConvertCoordinates(longitude.get())

    SetSchengen(a)
    SaveSchengenAirports(a)

def Add():
    a = Airport()
    a.icao = icao.get()
    a.latitude = ConvertCoordinates(latitude.get())
    a.longitude = ConvertCoordinates(longitude.get())

    SetSchengen(a)
    AddAirport(a)

def Remove():
    RemoveAirport(LoadAirports(), icao.get())

def LoadAP():
    global bcn
    bcn = LoadAirportStructure("Terminals.txt")

def ShowOccupancy():
    if bcn:
        ShowPlot(GateOccupancy(bcn))

def SearchAirline():
    if bcn:
        res = SearchTerminal(bcn, airline_entry.get())
        messagebox.showinfo("Result", res)

def CheckIsAirlineInTerminal():
    if not bcn:
        return

    t_name = terminal_entry.get()
    airline = airline_entry.get()

    t_obj = None
    for t in bcn.terminals:
        if t.name == t_name:
            t_obj = t

    if t_obj:
        res = IsAirlineInTerminal(t_obj, airline)
        messagebox.showinfo("Result", str(res))

def AssignGateUI():
    if not bcn:
        return

    aircraft_id = aircraft_entry.get()
    arrivals = LoadArrivals()

    target = None
    for a in arrivals:
        if a.id == aircraft_id:
            target = a

    if target:
        AssignGate(bcn, target)

def BuildAirlineFilter(parent):

    global airline_search_var

    Label(
        parent,
        text="Airline Filter",
        bg="#222233",
        fg="#c084fc",
        font=("Segoe UI", 11, "bold")
    ).pack(pady=10)

    airline_search_var = StringVar()

    Entry(
        parent,
        textvariable=airline_search_var,
        width=25
    ).pack(pady=5)

    available_box = Listbox(parent, height=12)
    available_box.pack(padx=10, pady=5, fill="x")

    Label(
        parent,
        text="Selected",
        bg="#222233",
        fg="white"
    ).pack()

    selected_box = Listbox(parent, height=8)
    selected_box.pack(padx=10, pady=5, fill="x")

    data = LoadArrivals()
    airlines = sorted(set(d.company for d in data))

    def refresh_available():

        available_box.delete(0, END)

        q = airline_search_var.get().lower()

        for a in airlines:
            if q in a.lower():
                available_box.insert(END, a)

    def refresh_selected():

        selected_box.delete(0, END)

        for a in selected_airlines:
            selected_box.insert(END, a)

    def add():

        try:
            val = available_box.get(available_box.curselection())

            if val not in selected_airlines:
                selected_airlines.append(val)

            refresh_selected()

        except:
            pass

    def remove():

        try:
            val = selected_box.get(selected_box.curselection())

            selected_airlines.remove(val)

            refresh_selected()

        except:
            pass

    def clear():

        selected_airlines.clear()
        refresh_selected()

    airline_search_var.trace_add(
        "write",
        lambda *args: refresh_available()
    )

    Button(
        parent,
        text="Add →",
        command=add
    ).pack(pady=2)

    Button(
        parent,
        text="← Remove",
        command=remove
    ).pack(pady=2)

    Button(
        parent,
        text="Clear",
        command=clear
    ).pack(pady=2)

    Button(
        parent,
        text="Apply",
        bg="#7c3aed",
        fg="white",
        command=PlotAl
    ).pack(pady=10)

    refresh_available()
    refresh_selected()

left = Frame(root, bg="#2a2a3d")
left.grid(row=0, column=0, sticky="nsew")

Label(left,
      text="AIRPORT CONTROL",
      bg="#2a2a3d",
      fg="#c084fc",
      font=("Segoe UI", 16, "bold")).grid(row=0, column=0, pady=10)

BTN = {
    "bg": "#7c3aed",
    "fg": "white",
    "font": FONT_B,
    "width": 24,
    "height": 1,
    "relief": "flat"
}


Label(left, text="Graphs", bg="#2a2a3d", fg="#c084fc").grid()

Button(left, text="Airports", command=PlotAp, **BTN).grid(pady=2)
Button(left, text="Show Airlines", command=PlotAl, **BTN).grid(pady=2)

Button(left, text="Arrivals", command=PlotArrRate, **BTN).grid(pady=2)
Button(left, text="Flight Types", command=PlotFlTy, **BTN).grid(pady=2)

Button(left, text="Map Airports", command=MapAp, **BTN).grid(pady=2)
Button(left, text="Map Flights", command=MapFl, **BTN).grid(pady=2)
Button(left, text="Long Flights", command=MapFlLong, **BTN).grid(pady=2)

Label(left, text="Airports", bg="#2a2a3d", fg="#c084fc").grid(pady=5)

icao = Entry(left, width=30); icao.grid(pady=1)
latitude = Entry(left, width=30); latitude.grid(pady=1)
longitude = Entry(left, width=30); longitude.grid(pady=1)

Button(left, text="Save", command=Save, **BTN).grid(pady=2)
Button(left, text="Add", command=Add, **BTN).grid(pady=2)
Button(left, text="Remove", command=Remove, **BTN).grid(pady=2)

Label(left, text="Operations", bg="#2a2a3d", fg="#c084fc").grid(pady=5)

Button(left, text="Load Structure", command=LoadAP, **BTN).grid(pady=2)
Button(left, text="Occupancy", command=ShowOccupancy, **BTN).grid(pady=2)

terminal_entry = Entry(left, width=30); terminal_entry.grid(pady=1)
airline_entry = Entry(left, width=30); airline_entry.grid(pady=1)

Button(left, text="Check Airline", command=CheckIsAirlineInTerminal, **BTN).grid(pady=2)
Button(left, text="Search Airline", command=SearchAirline, **BTN).grid(pady=2)

aircraft_entry = Entry(left, width=30); aircraft_entry.grid(pady=1)

Button(left, text="Assign Gate", command=AssignGateUI, **BTN).grid(pady=2)

frame3 = Frame(root, bg="#2a2a3d")
frame3.grid(row=0, column=1, sticky="nsew")

frame3.rowconfigure(0, weight=1)
frame3.columnconfigure(0, weight=1)

Label(frame3,
      text="Select a function",
      bg="#2a2a3d",
      fg="#c084fc",
      font=("Segoe UI", 14)).grid()

root.mainloop(
