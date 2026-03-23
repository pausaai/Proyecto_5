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
