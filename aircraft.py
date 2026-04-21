from airport import *
import math as math

class Aircraft:
    def __init__(self):
        self.id = ""
        self.company = ""
        self.origin = ""
        self.time = "00:00"

def GoodTimeFormat(time):
    try:
        if time == '':
            return False
        time = time.split(':')
        if len(time) != 2:
            return False
        if len(time[0]) != 2:
            return False
        if len(time[1]) != 2:
            return False

        hour = int(time[0])
        minute = int(time[1])
        if hour < 0 or hour > 23:
            return False
        if minute < 0 or minute > 59:
            return False
        else:
            return True
    except ValueError:
        return False

def LoadArrivals():
    arrivals = []
    try:
        f = open('Arrivals.txt', 'r')
        f.readline()
        line = f.readline()
        while line != '':
            data = line.split()
            if len(data) == 4 and GoodTimeFormat(data[2]):
                a = Aircraft()
                a.id = data[0]
                a.time = data[2]
                a.origin = data[1]
                a.company = data[3]
                arrivals = arrivals + [a]
            line = f.readline()
        f.close()
        return arrivals
    except FileNotFoundError:
        return []

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print('List is empty')
        return
    fig, ax = pyplot.subplots()
    count = [0]*24
    i = 0
    while i < len(aircrafts):
        hour = int(aircrafts[i].time.split(':')[0])
        count[hour] = count[hour] + 1
        i = i + 1
    ax.bar(range(24), count, color = "#d4664b")
    ax.set_title('Landing Frequency')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of landings')
    return fig

def SaveFlights(aircrafts):
    if len(aircrafts) == 0:
        print('List or File is empty')
    f = open(f'Arrivals.txt', 'w')
    i = 0
    f.write('AIRCRAFT ORIGIN ARRIVAL AIRLINE\n')
    while i < len(aircrafts):
        if aircrafts[i].id != '':
            aid = aircrafts[i].id
        else:
            aid = '-'
        if aircrafts[i].time != '':
            time = aircrafts[i].time
        else:
            time = '-'
        if aircrafts[i].origin != '':
            origin = aircrafts[i].origin
        else:
            origin = '-'
        if aircrafts[i].company != '':
            company = aircrafts[i].company
        else:
            company = '-'
        f.write(aid + ' ' + origin + ' ' + time + ' ' + company + '\n')
        i = i+1
    f.close()

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print('List is empty')
        return
    fig, ax = pyplot.subplots()
    different = []
    count = []
    d = 0
    while d < len(aircrafts):
        current = aircrafts[d].company
        i = 0
        found = False
        while not found and i < len(different):
            if different[i] == current:
                found = True
                count[i] = count[i]+1
            i = i+1
        if not found:
            different = different + [current]
            count = count + [1]
        d = d + 1
    ax.bar(different, count, color = "#d4664b")
    ax.set_title('Airline Flights')
    ax.set_xlabel('Airlines')
    ax.set_ylabel('Number of arriving aircraft')
    return fig

def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print('List is empty')
        return
    fig, ax = pyplot.subplots()
    schengen = 0
    notschengen = 0
    i = 0
    while i < len(aircrafts):
        code = aircrafts[i].origin
        if IsSchengenAirport(code):
            schengen = schengen + 1
        else:
            notschengen = notschengen + 1
        i = i + 1
    ax.bar('Schengen', schengen, color='#d4664b', label='Schengen')
    ax.bar('Not Schengen', notschengen, color='#ff5c3b', label='Not Schengen')
    ax.set_title('Arrival Origin')
    ax.set_ylabel('Count')
    ax.legend()
    return fig

def DegreesToRadians(degrees):  #Había otra funcion que ya donde ya se tenia los vuelos en grados?
    return degrees * (math.pi / 180)

def HaversineDistance(lat1, lon1, lat2 , lon2):
    RadioTierra=6371.0 #KM

    rlat1= DegreesToRadians(lat1)
    rlon1= DegreesToRadians(lon1)
    rlat2= DegreesToRadians(lat2)
    rlon2= DegreesToRadians(lon2)

    diferencia_lat= rlat2 - rlat1
    diferencia_lon= rlon2 - rlon1
    #Usamos la formula del HAversine este

    a=(math.sin(diferencia_lat/2)**2+math.cos(rlat1)*math.cos(rlat2)*math.sin(diferencia_lon/2)**2)

    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    distance = RadioTierra * c
    return distance

def FindAirports(airports, code):
    i=0
    while i < len(airports):
        if airports[i].icao == code:
            return airports[i]
        i += 1
    return None

def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print('List is empty')
        return
     # Escribimos las coordenadas de LEBL
    LEBLlon = 2.07833
    LEBLlat = 41.29694
    airports=LoadAirports()
    kml=open('Flights.kml','w')
    kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml.write('<Document>\n')

    i=0
    while i < len(aircrafts):
        codigoorigen = aircrafts[i].origin
        AeropuertoOrigen = FindAirports(airports, codigoorigen)
        if AeropuertoOrigen != None:
            origenlat = AeropuertoOrigen.latitude
            origenlon = AeropuertoOrigen.longitude
        #Pillamos codigo para determinar si Schengen o no, discutir colores luego
            if IsSchengenAirport(codigoorigen):
                color='ffff0000'#Azul
            else:
                color='#ff0000ff'#Rojo
            #Trayectoria/linea de origen a destino
            kml.write('<Placemark>\n')
            kml.write('<name>' + aircrafts[i].id + '</name>\n')
            kml.write('<Style>\n')
            kml.write('  <LineStyle>\n')
            kml.write('    <color>' + color + '</color>\n')
            kml.write('    <width>2</width>\n')
            kml.write('  </LineStyle>\n')
            kml.write('</Style>\n')
            kml.write('<LineString>\n')
            kml.write('  <altitudeMode>clampToGround</altitudeMode>\n')
            kml.write('  <tessellate>1</tessellate>\n')
            kml.write('  <coordinates>\n')

            kml.write('  ' + str(origenlon) + ',' + str(origenlat) + '\n')
            kml.write('  ' + str(LEBLlon) + ',' + str(LEBLlat) + '\n')
            kml.write('  </coordinates>\n')
            kml.write('</LineString>\n')
            kml.write('</Placemark>\n')
        i+=1
    kml.write('</Document>\n')
    kml.write('</kml>\n')
    kml.close()
    print('Flights.kml generated with ' + str(len(aircrafts)) + ' trajectories.')

def LongDistanceArrivals(aircrafts):
    if len(aircrafts) == 0:
        print('List is empty')
        return
    i = 0
    #Escribimos las coordenadas de LEBL
    LEBLlon=2.07833
    LEBLlat=41.29694

    #Utilizamos la condicion de 2000KM
    limite= 2000.0
    airports=LoadAirports()
    mayorlimite=[]
    while i < len(aircrafts):
        origincode = aircrafts[i].origin
        originairport= FindAirports(airports, origincode)
        if originairport != None:
            dist = HaversineDistance(originairport.latitude, originairport.longitude, LEBLlat, LEBLlon)
            if dist > limite:
                mayorlimite.append(aircrafts[i])
        i+= 1
    return mayorlimite
