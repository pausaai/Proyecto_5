class Airport:
    def __init__(self):
        self.icao = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.schengen = False


def IsSchengenAirport(code):
    if code == '':
        return False
    zone = code[0] + code[1]
    if zone == 'LO' or zone == 'EB' or zone == 'LK' or zone == 'LC' or zone == 'EK' or zone == 'EE' or zone == 'EF' or zone == 'LF' or zone == 'ED' or zone == 'LG' or zone == 'EH' or zone == 'LH' or zone == 'BI' or zone == 'LI' or zone == 'EV' or zone == 'EY' or zone == 'EL' or zone == 'LM' or zone == 'EN' or zone == 'EP' or zone == 'LP' or zone == 'LZ' or zone == 'LJ' or zone == 'LE' or zone == 'ES' or zone == 'LS':
        return True
    else:
        return False
def SetSchengen(Airport):
    Airport.schengen = IsSchengenAirport(Airport.icao)
def PrintAirport(Airport):
    print("ICAO:", Airport.icao)
    print("Latitude:", Airport.latitude)
    print("Longitude:", Airport.longitude)
    print("Schengen:", Airport.schengen)
