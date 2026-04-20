import matplotlib.pyplot as pyplot

class Airport:
    def __init__(self):
        self.icao = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.schengen = False

def IsSchengenAirport(code):
    if code == '' or len(code) != 4:
        return False
    zone = code[0] + code[1]
    codes = ['ET','EI','LO','EB','LK','LC','EK','EE','EF','LF','ED','LG','EH','LH','BI','LI','EV','EY','EL','LM','EN','EP','LP','LZ','LJ','LE','ES','LS','GC','LD','LR','LB']
    found = False
    i = 0
    while not found and i < len(codes):
        if codes[i] == zone:
            found = True
        i = i + 1
    return found

def ConvertCoordinates(coord):
    try:
        direction = coord [0]
        if direction == 'N' or direction == 'S':
            degrees = int(coord[1:3])
            minutes = int(coord[3:5])
            seconds = int(coord[5:7])
        else:
            degrees = int(coord[1:4])
            minutes = int(coord[4:6])
            seconds = int(coord[6:8])
        decimal = degrees + minutes/60 + seconds/3600
        if direction == 'S' or direction == 'W':
            decimal = -decimal
        return decimal
    except Exception:
        print(f'{coord} is not a valid coordinate.')
        return False

def ReturnCoordinates(decimal, islat):
    if islat:
        if decimal >= 0:
            direction = "N"
        else:
            direction = "S"
    else:
        if decimal >= 0:
            direction = "E"
        else:
            direction = "W"
    decimal = abs(decimal)
    deg = int(decimal)
    mins = int((decimal - deg) * 60)
    sec = int((decimal - deg - mins/60)*3600)
    if islat:
        if deg < 10:
            degfin = "0" + str(deg)
        else:
            degfin = str(deg)
    else:
        if deg < 10:
            degfin = "00" + str(deg)
        elif deg < 100:
            degfin = "0" + str(deg)
        else:
            degfin = str(deg)
    if mins < 10:
        minsfin = "0" + str(mins)
    else:
        minsfin = str(mins)
    if sec < 10:
        secfin = "0" + str(sec)
    else:
        secfin = str(sec)
    return direction + degfin + minsfin + secfin

def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.icao)

def PrintAirport(airport):
    try:
        print("ICAO:", airport.icao)
        print("Latitude:", airport.latitude)
        print("Longitude:", airport.longitude)
        print("Schengen:", airport.schengen)
    except AttributeError:
        print("Error, invalid airport.")

def LoadAirports():
        f = open('Airports.txt', 'r')
        f.readline()
        airports = []
        line = f.readline()
        while line != '':
            if line.strip() != '':
                elements = line.split()
                a = Airport()
                a.icao = elements[0]
                a.latitude = ConvertCoordinates(elements[1])
                a.longitude = ConvertCoordinates(elements[2])
                a.schengen = IsSchengenAirport(a.icao)
                airports = airports + [a]
            line = f.readline()
        f.close()
        return airports

def SaveSchengenAirports(airport):
    if airport is None:
        print('Input a valid airport.')
        return False
    if len(airport.icao) != 4:
        print("Invalid ICAO code")
        return False
    if not ('A' <= airport.icao[0] <= 'Z') or not ('A' <= airport.icao[1] <= 'Z') or not ('A' <= airport.icao[2] <= 'Z') or not ('A' <= airport.icao[3] <= 'Z'):
        print("Invalid Airport code")
        return False
    if airport.latitude < -90 or airport.latitude > 90:
        print("Invalid latitude")
        return False
    if airport.longitude < -180 or airport.longitude > 180:
        print("Invalid longitude")
        return False
    if not IsSchengenAirport(airport.icao):
        print("Not in Schengen.")
        return False
    full = []
    f = open(f'Airports.txt', 'r')
    line = f.readline()
    while line != "":
        full = full + [line]
        line = f.readline()
    f.close()
    i = 0
    found = False
    while i < len(full) and not found:
        elements = full[i].split(' ')
        if elements[0] == airport.icao:
            found = True
        if not found:
            i = i + 1
    if found:
        print('Airport is already on the list.')
        return found
    else:
        airportAdd = str(airport.icao) + ' ' + ReturnCoordinates(airport.latitude, True) + ' ' + ReturnCoordinates(
            airport.longitude, False)
        f = open(f'Airports.txt', 'a')
        last = full[-1].split(' ')
        if '\n' in last[-1]:
            f.write(f'{airportAdd}\n')
        else:
            f.write(f'\n{airportAdd}')
        f.close()
        print('Airport added to the list.')

def AddAirport(airport):
    if airport is None:
        print('Input a valid airport.')
        return False
    if len(airport.icao) != 4:
        print("Invalid ICAO code")
        return False
    if not ('A' <= airport.icao[0] <= 'Z') or not ('A' <= airport.icao[1] <= 'Z') or not ('A' <= airport.icao[2] <= 'Z') or not ('A' <= airport.icao[3] <= 'Z'):
        print("Invalid Airport code")
        return False
    if airport.latitude < -90 or airport.latitude > 90:
        print("Invalid latitude")
        return False
    if airport.longitude < -180 or airport.longitude > 180:
        print("Invalid longitude")
        return False
    full = []
    f = open(f'Airports.txt', 'r')
    line = f.readline()
    while line != "":
        full = full + [line]
        line = f.readline()
    f.close()
    i = 0
    found = False
    while i < len(full) and not found:
        elements = full[i].split(' ')
        if elements[0] == airport.icao:
            found = True
        if not found:
            i = i + 1
    if found:
        print('Airport is already on the list.')
        return True
    else:
        airportAdd = str(airport.icao) + ' ' + ReturnCoordinates(airport.latitude, True) + ' ' + ReturnCoordinates(airport.longitude, False)
        f = open(f'Airports.txt', 'a')
        last = full[-1].split(' ')
        if '\n' in last[-1]:
            f.write(f'{airportAdd}\n')
        else:
            f.write(f'\n{airportAdd}')
        f.close()
        print('Airport added to the list.')

def RemoveAirport(airports, code):
    if len(airports) == 0:
        print('List is empty')
        return []

    found = False
    new_airports = []
    i = 0

    while i < len(airports):
        if airports[i].icao == code:
            found = True
        else:
            new_airports = new_airports + [airports[i]]
        i = i + 1

    if not found:
        print('The code is not indexed.')
        return

    else:
        f = open(f'Airports.txt', 'r')
        f.write("CODE LAT     LON\n")
        i = 0
        while i < len(new_airports):
            f.write(new_airports[i].icao + ' ' + ReturnCoordinates(new_airports[i].latitude, True) + ' ' + ReturnCoordinates(new_airports[i].longitude, False) + '\n')
            i = i+1
        f.close()

def PlotAirports(airports):
    if len(airports) == 0:
        print('No airports found.')
        return
    fig, ax = pyplot.subplots()
    schengen = 0
    notschengen = 0
    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen = schengen + 1
        else:
            notschengen = notschengen + 1
        i = i + 1
    ax.bar('Schengen', schengen, color='#d4664b', label='Schengen')
    ax.bar('Not Schengen', notschengen, color='#ff5c3b', label='Not Schengen')
    ax.set_title('Schengen Airports')
    ax.set_ylabel('Count')
    return fig

def MapAirports(airports):
    if len(airports) == 0:
        print('No airports found.')
        return
    kml = open(f'Airports.kml', 'w')
    kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml.write('<Document>\n')
    i = 0
    while i < len(airports):
        kml.write(f'<Placemark> <name>{airports[i].icao}</name>\n')
        if airports[i].schengen:
            kml.write('<Style><IconStyle><color>ff0000ff</color></IconStyle></Style>\n')
        else:
            kml.write('<Style><IconStyle><color>ffff0000</color></IconStyle></Style>\n')
        kml.write('<Point>\n')
        kml.write(f'<coordinates>{airports[i].longitude},{airports[i].latitude}</coordinates>\n')
        kml.write('</Point>\n')
        kml.write('</Placemark>\n')
        i = i+1
    kml.write('</Document>\n')
    kml.write('</kml>\n')
    kml.close()
