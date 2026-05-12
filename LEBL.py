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
