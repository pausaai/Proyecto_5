import matplotlib.pyplot as pyplot


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

def LoadArrivals(filename):
    arrivals = []
    try:
        if filename == '':
            return []
        else:
            f = open(f'{filename}.txt', 'r')
            lines = f.readlines()
            f.close()
            i = 1
            while i < len(lines):
                data = lines[i].split()
                if len(data) == 4 and GoodTimeFormat(data[2]):
                    a = Aircraft()
                    a.id = data[0]
                    a.time = data[2]
                    a.origin = data[1]
                    a.company = data[3]
                    arrivals.append(a)
                i = i+1
            return arrivals
    except FileNotFoundError:
        return []

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print('List is empty')
        return
    count = [0]*24
    i = 0
    while i < len(aircrafts):
        hour = int(aircrafts[i].time.split(':')[0])
        count[hour] = count[hour] + 1
        i = i + 1
    pyplot.bar(range(24), count)
    pyplot.title('Landing Frequency')
    pyplot.xlabel('Hour')
    pyplot.ylabel('NUmber of landings')
    pyplot.show()

def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0 or filename == '':
        print('List or File is empty')
        return -1
    f = open(f'{filename}.txt', 'w')
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
    return 0