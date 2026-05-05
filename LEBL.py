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