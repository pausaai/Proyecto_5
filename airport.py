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
    codes = ['LO','EB','LK','LC','EK','EE','EF','LF','ED','LG','EH','LH','BI','LI','EV','EY','EL','LM','EN','EP','LP','LZ','LJ','LE','ES','LS','GC','LD','LR','LB']
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
        return 0.0


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


def LoadAirports(filename):
    try:
        if filename == '':
            print('')
            return []
        else:
            f = open(f'{filename}.txt', 'r')
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
    except FileNotFoundError:
        print(f'{filename}.txt not found.')
        return []


def SaveSchengenAirports(airports, filename):
    if filename == '' or airports == []:
        print("Input a list of airports and a filename. The airport information must have the following format: ICAO N123456 W123456,ICAO...")
    else:
        f = open(f'{filename}.txt', 'w')
        f.write("CODE LAT     LON\n")
        i = 0
        while i < len(airports):
            if IsSchengenAirport(airports[i].icao):
                f.write(f'{airports[i].icao} {airports[i].latitude} {airports[i].longitude}\n')
            i = i + 1
        f.close()


def AddAirport(airport):
    if airport is None:
        print('Input a valid airport.')
        return
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
        return
    else:
        airportAdd = str(airport.icao) + ' ' + str(airport.latitude) + ' ' + str(airport.longitude)
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

    return new_airports


def PlotAirports(airports):
    if len(airports) == 0:
        print('No airports found.')
        return
    schengen = 0
    notschengen = 0
    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen = schengen + 1
        else:
            notschengen = notschengen + 1
        i = i + 1
    pyplot.bar('Schengen', schengen, color='blue', label='Schengen')
    pyplot.bar('Not Schengen', notschengen, color='red', label='Not Schengen')
    pyplot.title('Schengen Airports')
    pyplot.ylabel('Count')
    pyplot.show()



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
