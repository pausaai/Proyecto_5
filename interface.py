import os
import sys
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from airport import *
from aircraft import *

try:
    f = open("Airports.txt", "r")
    f.close()
except FileNotFoundError:
    messagebox.showerror("Error", "No Airports file found.\nPlease download Airports.txt")
    sys.exit(1)

root = Tk()
root.title("Airport Management")
root.configure(bg='#f5e8c3', padx=15, pady=15)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=2)
root.rowconfigure(3, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

FONT = ("Helvetica", 10)
FONT_B = ("Helvetica", 10, "bold")
FONT_TITLE = ("Helvetica", 11, "bold")

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
        a = Airport()
        a.icao = icao.get()
        a.latitude = ConvertCoordinates(latitude.get())
        a.longitude = ConvertCoordinates(longitude.get())
        SetSchengen(a)
        result = SaveSchengenAirports(a)
        if result == True:
            messagebox.showinfo("Error", "Airport Already on the List")
            return
        elif result == False:
            messagebox.showinfo("Error", "Check Airport Format")
        else:
            messagebox.showinfo("Success", "Airport Added Successfully")
    except ValueError:
        messagebox.showerror("Error", "No Airports found.\n Please input a valid Airport")
        return
def Add():
    try:
        a = Airport()
        a.icao = icao.get()
        a.latitude = ConvertCoordinates(latitude.get())
        a.longitude = ConvertCoordinates(longitude.get())
        if (a.latitude == None) or (a.longitude == None):
            messagebox.showerror("Error", "Check coordinates")
            return
        SetSchengen(a)
        result = AddAirport(a)
        if result == True:
            messagebox.showinfo("Error", "Airport Already on the List")
            return
        elif result == False:
            messagebox.showinfo("Error", "Check Airport Format")
            return
        else:
            messagebox.showinfo("Success", "Airport Added Successfully")
    except ValueError:
        messagebox.showerror("Error", "No Airports found.\n Please input a valid Airport")
        return

def Remove():
    airport = icao.get()
    RemoveAirport(LoadAirports(), airport)

Label(root, text="Airport Management", bg='#f5e8c3', fg='#ff5c3b', font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

frame1 = LabelFrame(root, text="Existing File Operations", font=FONT_TITLE)
frame1.configure(bg='#f5e8c3', fg="#ff5c3b")
frame1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
frame1.columnconfigure(0, weight=1)
Button(frame1, text="Plot Airports", command=PlotAp, bg='#d4664b', fg="white", font=FONT_B).grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot Arrivals by type", command=PlotFlTy, bg='#d4664b', fg="white", font=FONT_B).grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot Airlines", command=PlotAl, bg='#d4664b', fg="white", font=FONT_B).grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Plot Arrivals", command=PlotArrRate, bg='#d4664b', fg="white", font=FONT_B).grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map Airports", command=MapAp,  bg='#d4664b', fg="white", font=FONT_B).grid(row=7, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map Arrivals", command=MapFl, bg='#d4664b', fg="white", font=FONT_B).grid(row=8, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame1, text="Map Long Distance Arrivals", command=MapFlLong, bg='#d4664b', fg="white", font=FONT_B).grid(row=9, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

frame2 = LabelFrame(root, text="Add / Save / Remove:", font=FONT_TITLE)
frame2.configure(bg='#f5e8c3', fg="#ff5c3b")
frame2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
frame2.columnconfigure(0, weight=1)
Label(frame2, text="Enter Airport:", bg="#f5e8c3", fg="#ff5c3b", font=FONT_B).grid(row=0, column=0, columnspan= 2)
Label(frame2, text="ICAO code: (e.g. 'LEBL')", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=1, column=0)
icao = Entry(frame2, width=40, font=FONT, bg='#e7ceb1')
icao.grid(row=1, column=1, padx=5, pady=5)
Label(frame2, text="Latitude: (e.g. 'N411749')", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=2, column=0)
latitude = Entry(frame2, width = 40, font=FONT, bg='#e7ceb1')
latitude.grid(row=2, column=1, padx=5, pady=5)
Label(frame2, text="Longitude: (e.g. 'E0020442')", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=3, column=0)
longitude = Entry(frame2, width=40, font=FONT, bg='#e7ceb1')
longitude.grid(row=3, column=1, padx=5, pady=5)
Button(frame2, text="Save Schengen Airports Only", command=Save, bg="#d4664b", fg="white", font=FONT_B).grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame2, text="Add Airport list to File", command=Add,  bg="#d4664b", fg="white", font=FONT_B).grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")
Button(frame2, text="Remove Airport", command=Remove, bg="#d4664b", fg="white", font=FONT_B).grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=3, sticky="nsew")

frame3 = LabelFrame(root, text="Figure Visualizer", font=FONT_TITLE)
frame3.configure(bg='#f5e8c3', fg="#ff5c3b")
frame3.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
frame3.rowconfigure(1, weight=1)
frame3.columnconfigure(0, weight=1)
    #Añadimos la función para ajustar las grafica a la interfaz
def PlotAp():
    for widget in frame3.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(PlotAirports(LoadAirports()), master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

Label(frame3, text="Press any 'Plot' button to display", bg="#f5e8c3", fg="#ff5c3b", font=FONT).grid(row=0, column=0)
root.mainloop()
