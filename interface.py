import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from airport import (IsSchengenAirport, LoadAirports, SaveSchengenAirports,
                     AddAirport, RemoveAirport, PlotAirports, MapAirports)

# ── Root window ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Airport Manager")
root.geometry("800x600")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

# ═══════════════════════════════════════════════════════════════════════════════
# FRAME 1 — File operations (Load, Map, Plot)
# ═══════════════════════════════════════════════════════════════════════════════
frame_file = tk.LabelFrame(root, text="File Operations")
frame_file.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
frame_file.columnconfigure(0, weight=1)

tk.Label(frame_file, text="Filename (no .txt):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_filename = tk.Entry(frame_file, width=25)
entry_filename.grid(row=1, column=0, padx=5, pady=2)

def do_load():
    fn = entry_filename.get().strip()
    if fn == '':
        messagebox.showinfo("Error", "Please enter a filename.")
    else:
        LoadAirports(fn)
        messagebox.showinfo("Load", f"'{fn}.txt' loaded. Check the console for output.")

def do_map():
    fn = entry_filename.get().strip()
    if fn == '':
        messagebox.showinfo("Error", "Please enter a filename.")
    else:
        MapAirports(fn)
        messagebox.showinfo("Map", f"KML file '{fn}.kml' generated.")

def do_plot():
    fn = entry_filename.get().strip()
    if fn == '':
        messagebox.showinfo("Error", "Please enter a filename.")
    else:
        show_plot(fn)

tk.Button(frame_file, text="Load Airports",    command=do_load, bg="lightblue").grid(row=2, column=0, padx=5, pady=3, sticky="ew")
tk.Button(frame_file, text="Generate KML Map", command=do_map,  bg="lightblue").grid(row=3, column=0, padx=5, pady=3, sticky="ew")
tk.Button(frame_file, text="Plot Airports",    command=do_plot, bg="lightblue").grid(row=4, column=0, padx=5, pady=3, sticky="ew")

# ═══════════════════════════════════════════════════════════════════════════════
# FRAME 2 — Add / Remove airport
# ═══════════════════════════════════════════════════════════════════════════════
frame_edit = tk.LabelFrame(root, text="Add / Remove Airport")
frame_edit.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
frame_edit.columnconfigure(0, weight=1)

tk.Label(frame_edit, text="Filename (no .txt):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_edit_file = tk.Entry(frame_edit, width=25)
entry_edit_file.grid(row=1, column=0, padx=5, pady=2)

tk.Label(frame_edit, text="Airport entry (e.g. LEBL N411749 E0020442):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
entry_add_data = tk.Entry(frame_edit, width=25)
entry_add_data.grid(row=3, column=0, padx=5, pady=2)

tk.Label(frame_edit, text="ICAO code to remove:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
entry_remove_code = tk.Entry(frame_edit, width=25)
entry_remove_code.grid(row=5, column=0, padx=5, pady=2)

def do_add():
    fn   = entry_edit_file.get().strip()
    data = entry_add_data.get().strip()
    if fn == '' or data == '':
        messagebox.showinfo("Error", "Please fill in both fields.")
    else:
        AddAirport(fn, data)
        messagebox.showinfo("Add", f"Airport added to '{fn}.txt'.")

def do_remove():
    fn   = entry_edit_file.get().strip()
    code = entry_remove_code.get().strip().upper()
    if fn == '' or code == '':
        messagebox.showinfo("Error", "Please fill in both fields.")
    else:
        RemoveAirport(fn, code)

tk.Button(frame_edit, text="Add Airport",    command=do_add,    bg="lightgreen").grid(row=6, column=0, padx=5, pady=3, sticky="ew")
tk.Button(frame_edit, text="Remove Airport", command=do_remove, bg="salmon").grid(    row=7, column=0, padx=5, pady=3, sticky="ew")

# ═══════════════════════════════════════════════════════════════════════════════
# FRAME 3 — Schengen operations
# ═══════════════════════════════════════════════════════════════════════════════
frame_sch = tk.LabelFrame(root, text="Schengen Operations")
frame_sch.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
frame_sch.columnconfigure(0, weight=1)

tk.Label(frame_sch, text="ICAO code to check:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_check_code = tk.Entry(frame_sch, width=25)
entry_check_code.grid(row=1, column=0, padx=5, pady=2)

tk.Label(frame_sch, text="Airports string (LEBL N411749 E0020442,...):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
entry_sch_airports = tk.Entry(frame_sch, width=25)
entry_sch_airports.grid(row=3, column=0, padx=5, pady=2)

tk.Label(frame_sch, text="Output filename (no .txt):").grid(row=4, column=0, padx=5, pady=2, sticky="w")
entry_sch_file = tk.Entry(frame_sch, width=25)
entry_sch_file.grid(row=5, column=0, padx=5, pady=2)

def do_check():
    code = entry_check_code.get().strip().upper()
    if code == '':
        messagebox.showinfo("Error", "Please enter an ICAO code.")
    else:
        result = IsSchengenAirport(code)
        if result:
            messagebox.showinfo("Schengen Check", f"'{code}' is a Schengen airport.")
        else:
            messagebox.showinfo("Schengen Check", f"'{code}' is NOT a Schengen airport.")

def do_save_schengen():
    airports = entry_sch_airports.get().strip()
    fn       = entry_sch_file.get().strip()
    if airports == '' or fn == '':
        messagebox.showinfo("Error", "Please fill in both fields.")
    else:
        SaveSchengenAirports(airports, fn)
        messagebox.showinfo("Save Schengen", f"Schengen airports saved to '{fn}.txt'.")

tk.Button(frame_sch, text="Check Schengen",         command=do_check,          bg="lightyellow").grid(row=6, column=0, padx=5, pady=3, sticky="ew")
tk.Button(frame_sch, text="Save Schengen Airports", command=do_save_schengen,  bg="lightyellow").grid(row=7, column=0, padx=5, pady=3, sticky="ew")

# ═══════════════════════════════════════════════════════════════════════════════
# FRAME 4 — Plot display (right column, spans all rows)
# ═══════════════════════════════════════════════════════════════════════════════
frame_plot = tk.LabelFrame(root, text="Plot")
frame_plot.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky="nsew")
frame_plot.columnconfigure(0, weight=1)
frame_plot.rowconfigure(0, weight=1)

canvas_widget = None

def show_plot(fn):
    global canvas_widget
    fig, ax = plt.subplots()
    f = open(f'{fn}.txt', 'r')
    f.readline()  # skip header
    lines = f.readlines()
    f.close()
    schengen = 0
    notschengen = 0
    i = 0
    while i < len(lines):
        code = lines[i].split()[0]
        if IsSchengenAirport(code):
            schengen += 1
        else:
            notschengen += 1
        i += 1
    ax.bar('Airports', schengen,    color='blue', label='Schengen')
    ax.bar('Airports', notschengen, color='red',  label='Not Schengen', bottom=schengen)
    ax.set_title('Schengen Airports')
    ax.set_ylabel('Count')
    ax.legend()
    if canvas_widget is not None:
        canvas_widget.get_tk_widget().destroy()
    canvas_widget = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# ═══════════════════════════════════════════════════════════════════════════════
root.mainloop()
