from airport import *
import tkinter as tk
from tkinter import messagebox, filedialog
airports = []
def refresh_list():
    listbox.delete(0, tk.END)
    for a in airports:
        listbox.insert(tk.END, a.code)
# BUTTON 

def load_airports():
    global airports
    filename = filedialog.askopenfilename()
    if filename:
        airports = LoadAirports(filename)
        refresh_list()
def add_airport():
    try:
        code = entry_code.get()
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        a = Airport(code, lat, lon)
        SetSchengen(a)
        AddAirport(airports, a)
        refresh_list()
    except:
        messagebox.showerror("Error", "Invalid input")

def delete_airport():
    code = entry_code.get()
    if code == "":
        messagebox.showerror("Error", "Enter ICAO code")
        return

    RemoveAirport(airports, code)
    refresh_list()

def show_airports():
    listbox.delete(0, tk.END)
    for a in airports:
        text = f"{a.code} | {a.lat} | {a.lon} | Schengen: {a.schengen}"
        listbox.insert(tk.END, text)

def save_schengen():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        SaveSchengenAirports(airports, filename)

def plot_airports():
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports loaded")
        return
    PlotAirports(airports)

def map_airports():
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports loaded")
        return
    MapAirports(airports)

--
# GUI SETUP

root = tk.Tk()
root.title("Airport Manager")
root.geometry("600x500")

# TITLE
tk.Label(root, text="Airport Manager", font=("Arial", 16)).pack(pady=10)

# INPUT FRAME
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="ICAO").grid(row=0, column=0)
entry_code = tk.Entry(frame_inputs)
entry_code.grid(row=0, column=1)

tk.Label(frame_inputs, text="Latitude").grid(row=1, column=0)
entry_lat = tk.Entry(frame_inputs)
entry_lat.grid(row=1, column=1)

tk.Label(frame_inputs, text="Longitude").grid(row=2, column=0)
entry_lon = tk.Entry(frame_inputs)
entry_lon.grid(row=2, column=1)

# BUTTON FRAME
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Load", width=15, command=load_airports).grid(row=0, column=0)
tk.Button(frame_buttons, text="Add", width=15, command=add_airport).grid(row=0, column=1)
tk.Button(frame_buttons, text="Delete", width=15, command=delete_airport).grid(row=1, column=0)
tk.Button(frame_buttons, text="Show", width=15, command=show_airports).grid(row=1, column=1)
tk.Button(frame_buttons, text="Save Schengen", width=15, command=save_schengen).grid(row=2, column=0)
tk.Button(frame_buttons, text="Plot", width=15, command=plot_airports).grid(row=2, column=1)
tk.Button(frame_buttons, text="Map", width=15, command=map_airports).grid(row=3, column=0)

# LISTBOX
listbox = tk.Listbox(root, width=70)
listbox.pack(pady=20)

# RUN APP
root.mainloop()


