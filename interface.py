from airport import*
import tkinter as tk
from tkinter import messagebox, filedialog

#Datos
airports=[]

def refresh_list()
  listbox.delete(0,tk.END)
  for a in airpots:
    litsbox.insert(tk.END, a.code)

#Butones de la app
def load_airports():
  global airports 
  filename=filedialog.askopenfilename()
  if filename:
    airports= LoadAirports(filename)
    refresh_list()
def add_airport():
  try:
    code=entry_code.get()
    lat=float(entry_lat.get())
    lon=float(entry_lon.get())
    a= Airport(code, lat, lon)
    SetSchengen(airports,a )
    AddAirports(airports, a)
    refresh_list()
  except:
    messagebox.showerror("Error","Enter ICAO code")
def delete_airport():
  code= entry_code.get()
  if code=="":
    message.box.showerror("Error", "Enter ICAO code")
    return
  RemoveAirport(airports, code)
  refresh_list()
def show_airports():
  listbox.delete(0, tk.END)
  for a in airports:
    text= f"{a.code¨} , {a.lat} , {a.lon} Schengen: {a.schengen}"
    listbox.insert(tk.END, text)
def save_schengen():
  filename=fikedialog.asksaveasfilename(defaultextension=".txt")
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
  
  
