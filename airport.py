import matplotlib.pyplot as pyplot

class Airport:
    def __init__(self):
        self.icao = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.schengen = False


def IsSchengenAirport(code):
    if code == '' or len(code)!= 4:
        return False
    zone = code[0] + code[1]
    f = open('SchengenCodes.txt')
    codes = (f.readline())
    codes = codes.split(' ')
    f.close()
    if zone in codes:
        return True
    else:
        return False


def SetSchengen(airport):
    Airport.schengen = IsSchengenAirport(airport.icao)


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
        else:
            f = open(f'{filename}.txt', 'r')
            f.readline()
            print("CODE LAT LON")
            for line in f:
                print(line)
            f.close()
    except FileNotFoundError:
        print(f'{filename}.txt not found.')


def CheckFormat(airport):
    if airport == '':
        return False
    tot = airport.split(',')
    i = 0
    while i < len(tot):
        inputairport = tot[i].split()
        lat = inputairport[1]
        lon = inputairport[2]
        if len(inputairport) != 3 or len(inputairport[0]) != 4 or len(lat) != 7 or lat[0] != 'N' and lat[0] != 'S' or len(lon) != 8 or lon[0] != 'E' and lon[0] != 'W':
            return False
        i = i+1
    return True


def SaveSchengenAirports(airports, filename):
    if filename == '' or airports == []:
        print("Input a list of airports and a filename. The airport information must have the following format: ICAO N123456 W123456,ICAO...")
    elif not CheckFormat(airports):
        print("Check the Airport format.")
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


def AddAirport(file, airport):
    try:
        f = open(f'{file}.txt', 'r')
        full = f.readlines()
        f.close()
    except FileNotFoundError:
        print('File not found')
        return
    i = 0
    found = False
    try:
        if file == '' or airport == '':
            print('Please enter a filename and airport data in the right format.')
            return
        if not CheckFormat(airport):
            print('Please review the airport format. Keep in mind that longitude has 3 integrers of degrees and latitude only has 2.')
            return
        else:
            while i < len(full) and not found:
                elements = full[i].split(' ')
                if elements[0] == airport[0:4]:
                    found = True
                if not found:
                    i = i + 1
            if found:
                print('Airport is already on the list.')
            else:
                f = open(f'{file}.txt', 'a')
                last = full[-1].split(' ')
                if '\n' in last[-1]:
                    f.write(f'{airport}\n')
                else:
                    f.write(f'\n{airport}')
                f.close()
                print('Airport added to the list.')
    except ValueError:
        print('Revise el formato del aeropuerto.')


def RemoveAirport(airports, code):
    try:
        f = open(f'{airports}.txt', 'r')
        f.readline()
        lines = f.readlines()
        f.close()
    except FileNotFoundError:
        print(f'{airports}.txt does not exist.')
        return
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
    try:
        f = open(f'{airports}.txt', 'r')
        f.readline()
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
    except FileNotFoundError:
        print(f'{airports}.txt does not exist.')


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


def MapAirports(airports):
    try:
        f = open(f'{airports}.txt', 'r')
        f.readline()
        lines = f.readlines()
        f.close()
    except FileNotFoundError:
        print(f'{airports}.txt does not exist.')
        return
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
