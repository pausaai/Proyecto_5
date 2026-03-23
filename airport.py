import matplotlib.pyplot as pyplot

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
    if zone == 'GC' or zone == 'LO' or zone == 'EB' or zone == 'LK' or zone == 'LC' or zone == 'EK' or zone == 'EE' or zone == 'EF' or zone == 'LF' or zone == 'ED' or zone == 'LG' or zone == 'EH' or zone == 'LH' or zone == 'BI' or zone == 'LI' or zone == 'EV' or zone == 'EY' or zone == 'EL' or zone == 'LM' or zone == 'EN' or zone == 'EP' or zone == 'LP' or zone == 'LZ' or zone == 'LJ' or zone == 'LE' or zone == 'ES' or zone == 'LS':
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


def LoadAirports(filename):
    def LoadAirports(filename):
    if filename == '':
        print('File cant be empty')
        return
    try:
        with open(f'{filename}.txt', 'r') as f:
            f.readline()  # Leer la primera línea (encabezados)
            print("CODE LAT     LON")
            for line in f:
                print(line.strip())  # .strip() para eliminar espacios en blanco
    except FileNotFoundError:
        print(f'Error: El archivo {filename}.txt no se encontró.')
    except ValueError as e:
        print(f'Error de valor: {e}')  # Captura errores de formato
    except Exception as e:
        print(f'Error inesperado: {e}')  # Captura otros errores
            


def SaveSchengenAirports(airports, filename):
    if filename == '' or airports == []:
        print("Input a list of airports and a filename. The airport information must have the following format: ICAO N123456 W123456,ICAO...")
    else:
        f = open(f'{filename}.txt', 'w')
        f.write("CODE LAT     LON\n")
        tot = airports.split(',')
        i = 0
        while i < len(tot):
            code = tot[i].split(' ')[0]
            if IsSchengenAirport(code):
                f.write(f'{tot[i]}\n')
                i = i + 1
            else:
                i = i + 1
        f.close()


def AddAirport(airports, airport):
    f = open(f'{airports}.txt', 'a')
    f.write(f'{airport}\n')
    f.close()


def RemoveAirport(airports, code):
    f = open(f'{airports}.txt', 'r')
    lines = f.readlines()
    f.close()
    found = False
    i = 0
    while i < len(lines) and not found:
        elements = lines[i].split()
        if elements[0] == code:
            found = True
        if not found:
            i = i + 1
    if not found:
        print('The code is not indexed.')
    else:
        f = open(f'{airports}.txt', 'w')
        i = 0
        while i < len(lines):
            elements = lines[i].split()
            if elements[0] != code:
                f.write(lines[i])
            i = i + 1
        f.close()


def PlotAirports(airports):
    f = open(f'{airports}.txt', 'r')
    lines = f.readlines()
    f.close()
    schengen = 0
    notschengen = 0
    i = 0
    while i < len(lines):
        code = lines[i].split()[0]
        if IsSchengenAirport(code):
            schengen = schengen + 1
        else:
            notschengen = notschengen + 1
        i = i + 1
    pyplot.bar('Airports', schengen, color='blue', label='Schengen')
    pyplot.bar('Airports', notschengen, color='red', label='Not Schengen')
    pyplot.title('Schengen Airports')
    pyplot.ylabel('Count')
    pyplot.legend()
    pyplot.show()


def ConvertCoordinates(coord):
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


def MapAirports(airports):
    f = open(f'{airports}.txt', 'r')
    f.readline()
    lines = f.readlines()
    f.close()
    kml = open(f'{airports}.kml', 'w')
    kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml.write('<Document>\n')
    i = 0
    while i < len(lines):
        elements = lines[i].split()
        code = elements[0]
        lat = ConvertCoordinates(elements[1])
        lon = ConvertCoordinates(elements[2])
        kml.write(f'<Placemark> <name>{code}</name>\n')
        if IsSchengenAirport(code):
            kml.write('<Style><IconStyle><color>ff0000ff</color></IconStyle></Style>\n')
        else:
            kml.write('<Style><IconStyle><color>ffff0000</color></IconStyle></Style>\n')
        kml.write('<Point>\n')
        kml.write(f'<coordinates>{lon},{lat}</coordinates>\n')
        kml.write('</Point>\n')
        kml.write('</Placemark>\n')
        i = i+1
    kml.write('</Document>\n')
    kml.write('</kml>\n')
    kml.close()
