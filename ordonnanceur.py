def hour_calc(i):
    date = 0
    hour= 0
    min= 0
    min_of_day = 60 *24
    if(i < min_of_day):
        date = "Mon"
    elif(i < min_of_day*2):
        date = "Tue"
    elif(i < min_of_day*3):
        date = "Wed"
    elif(i < min_of_day*4):
        date = "Thu"
    elif(i < min_of_day*5):
        date = "Fri"
    elif(i < min_of_day*6):
        date = "Sat"
    else:
        date = "Sun"

    tmp = i%min_of_day
    min = tmp%60
    hour = tmp -min
    hour = hour/60
    res = "{}:{}".format(int(hour), int(min))
    return [date,res]


def get_day(date1):
    if(date1[0] == "Mon"):
        return 0
    elif(date1[0] == "Tue"):
        return 1
    elif(date1[0] == "Wed"):
        return 2
    elif(date1[0] == "Thu"):
        return 3
    elif(date1[0] == "Fri"):
        return 4
    elif(date1[0] == "Sat"):
        return 5
    else: #Sun
        return 6


class Ordonnanceur(object):
    """docstring for Ordonnanceur."""

    length_array = 10080 # 7 jour * 24h * 60 mins
    array = [length_array] # 0 creneau libre  sinon 1  -1 si date block
    vitesse_imprimmer = 1 # 1 page/sec
    array = [0 for i in range(length_array)]


    def __init__(self):
        super(Ordonnanceur, self).__init__()
        self.array = [0 for i in range(self.length_array)]

    def add_creneau(self, nb_pages):
        b1 = 0
        if(nb_pages <= 0):
            return [-1, "Error on number of pages"]
        mins_took = int((nb_pages*self.vitesse_imprimmer)/60)
        for i in range(self.length_array):
            if(self.array[i] == 0):
                if(mins_took+i <= self.length_array ):
                    for h in range(i,mins_took+i): # on imprimme un fichier en entier
                        if(self.array[h] != 0 ):
                            b1=1
                            break
                    if(b1==1):
                        b1=0
                        continue
                    print('reserving time')
                    date1 = hour_calc(i)
                    for h in range(i,mins_took+i) :
                        self.array[h] = 1

                    date2 = hour_calc(h)
                    return date1 ,date2
                else :
                    print()
                    return [-1, "No timeslot left for this week."]
        return [-1, "No timeslot left for this week."]
    # block a specific date

    def bloque(self,jour):
        len_day = int(self.length_array /7)
        #self.array = [-1 for i in range(len_day*jour,len_day*jour+1)]

        for h in range(len_day*jour,len_day*(jour+1)) :
            self.array[h] = -1

    def bloque_hour(self,date1,date2):

        jour1 = 0
        jour2 = 0

        hour_min1 = date1[1].split(":")
        hour_min2 = date2[1].split(":")

        hour1 = int(hour_min1[0])
        min1 =  int(hour_min1[1])
        hour2 = int(hour_min2[0])
        min2 =  int(hour_min2[1])

        jour1 = get_day(date1)
        jour2 = get_day(date2)

        len_day = int(self.length_array /7)

        for h in range((len_day*jour1)+(hour1*60)+min1 ,(len_day*jour2)+(hour2*60)+min2 ) :
            self.array[h] = -1
