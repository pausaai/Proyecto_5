class Gate:
    def __init__(self):
        self.name = ""
        self.free = False
        self.ID   = ""

class BoardingArea:
    def __init__(self):
        self.name  = ""
        self.type  = False
        self.gates = []

class Terminal:
    def __init__(self):
        self.name  = ""
        self.areas = []
        self.codes = []

class BarcelonaAP:
    def __init__(self):
        self.code      = ""
        self.terminals = []


def SetGates(area, init_gate, end_gate, prefix):
    if init_gate > end_gate:
        return -1
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
    try:
        f = open(filename, "r")
    except:
        return -1

    terminal.codes = []
    lines = f.readlines()
    f.close()

    for line in lines:
        line = line.strip()
        if line != "":
            parts = line.split("\t")
            if len(parts) >= 2:
                terminal.codes.append(parts[1].strip())
    return terminal


def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")
    except:
        return -1

    lines = f.readlines()
    f.close()
    lines = [l.strip() for l in lines]

    first      = lines[0].split()
    airport    = BarcelonaAP()
    airport.code = first[0]
    num_terminals = int(first[1])
    idx = 1

    for _ in range(num_terminals):
        term_parts = lines[idx].split()
        idx += 1
        terminal      = Terminal()
        terminal.name = term_parts[1]
        num_areas     = int(term_parts[2])

        for _ in range(num_areas):
            area_parts = lines[idx].split()
            idx += 1
            area      = BoardingArea()
            area.name = area_parts[1].lower()
            area.type = (area_parts[2] == "Schengen")
            init_gate = int(area_parts[4])
            end_gate  = int(area_parts[6])
            result    = SetGates(area, init_gate, end_gate, terminal.name)
            if result == -1:
                return -1
            terminal.areas.append(area)

        LoadAirlines(terminal, terminal.name)
        airport.terminals.append(terminal)

    return airport


def GateOccupancy(bcn):
    occupancy = []
    for terminal in bcn.terminals:
        for area in terminal.areas:
            for gate in area.gates:
                entry = [gate.name]
                if gate.free:
                    entry.append("free")
                    entry.append("")
                else:
                    entry.append("occupied")
                    entry.append(gate.ID)
                occupancy.append(entry)
    return occupancy


def IsAirlineInTerminal(terminal, name):
    if not terminal or not name:
        return False
    for code in terminal.codes:
        if code == name:
            return True
    return False


def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name
    return ""


def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.company)
    if terminal_name == "":
        print("Airline not found in any terminal")
        return -1

    terminal = next((t for t in bcn.terminals if t.name == terminal_name), None)
    if terminal is None:
        return -1

    for area in terminal.areas:
        for gate in area.gates:
            if gate.free:
                gate.free = False
                gate.ID   = aircraft.id
                return 0
    return -1

def AssignNightGates(bcn, aircrafts):
    #VERIFICAMOS con la condicion aircrafts[i].time == "00:00" and aircrafts[i].origin == "" que no tiene llegadas, aka es nocturno
    #Luego con funcion AssigGate le asignamos un puerta y pasa al siguiente
    if len(aircrafts) == 0:
        return -1
    i = 0
    while i < len(aircrafts):
        # Only process aircraft with no arrival data (night aircraft)
        if aircrafts[i].time == "00:00" and aircrafts[i].origin == "":
            AssignGate(bcn, aircrafts[i])
        i = i + 1
