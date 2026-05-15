class Gate:
    def __init__(self):
        self.name = ""
        self.free = False
        self.ID = ""
class BoardingArea:
    def __init__(self):
        self.name = ""
        self.type = False
        self.gates = []
class Terminal:
    def __init__(self):
        self.name = ""
        self.areas = []
        self.codes = []
class BarcelonaAP:
    def __init__(self):
        self.code = ""
        self.terminals = []
def SetGates(area, init_gate, end_gate, prefix):
    if init_gate > end_gate:
        return(-1)
    schengenAreas = ["a", "b", "c", "m", "r", "s", "u"]
    d = 0
    while d != len(schengenAreas):
        if area.name == schengenAreas[d]:
            area.type = True
            d = d + 1
        else:
            d = d + 1
    i = init_gate
    while i <= end_gate:
        g = Gate()
        g.name = prefix + area.name + str(i)
        g.free = True
        area.gates.append(g)
        i += 1
    return area
def LoadAirlines(terminal, t_name):
    filename = t_name + "_Airlines.txt"
    found = False
    try:
        f = open(filename, "r")
        found = True
        f.close()
    except:
        found = False

    if found == False:
        return -1
    terminal.codes = []
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    i = 0
    while i != len(lines):
        line = lines[i]
        line = line.strip()
        if line != "":
            parts = line.split("\t")
            if len(parts) >= 2:
                terminal.codes.append(parts[1].strip())
        i = i + 1
    return terminal
def LoadAirportStructure(filename):
    found = False
    try:
        f = open(filename, "r")
        found = True
        f.close()
    except:
        found = False
    if found == False:
        return -1
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    i = 0
    while i != len(lines):
        lines[i] = lines[i].strip()
        i = i + 1
    first = lines[0].split()
    airport = BarcelonaAP()
    airport.code = first[0]
    num_terminals = int(first[1])
    idx = 1
    t = 0
    while t != num_terminals:
        term_parts = lines[idx].split()
        idx = idx + 1
        terminal = Terminal()
        terminal.name = term_parts[1]
        num_areas = int(term_parts[2])
        a = 0
        while a != num_areas:
            area_parts = lines[idx].split()
            idx = idx + 1
            area = BoardingArea()
            area.name = area_parts[1].lower()
            if area_parts[2] == "Schengen":
                area.type = True
            else:
                area.type = False
            init_gate = int(area_parts[4])
            end_gate = int(area_parts[6])
            prefix = terminal.name
            result = SetGates(area, init_gate, end_gate, prefix)
            if result == -1:
                return -1
            terminal.areas.append(area)
            a = a + 1
        LoadAirlines(terminal, terminal.name)
        airport.terminals.append(terminal)
        t = t + 1
    return airport
def GateOccupancy(bcn):
    occupancy = []
    t = 0
    while t != len(bcn.terminals):
        terminal = bcn.terminals[t]
        a = 0
        while a != len(terminal.areas):
            area = terminal.areas[a]
            g = 0
            while g != len(area.gates):
                gate = area.gates[g]
                entry = []
                entry.append(gate.name)
                if gate.free == True:
                    entry.append("free")
                    entry.append("")
                else:
                    entry.append("occupied")
                    entry.append(gate.ID)
                occupancy.append(entry)
                g = g + 1
            a = a + 1
        t = t + 1
    i = 0
    while i != len(occupancy):
        print(occupancy[i])
        i = i + 1
    return occupancy
