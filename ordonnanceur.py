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
        if(nb_pages <= 0):
            return [-1, "Error on number of pages"]
        for i in range(self.length_array):
            #print(i,self.array[i])
            if(self.array[i] == 0):
                if(nb_pages+i <= self.length_array):
                    print('reserving time')
                    date1 = hour_calc(i)
                    for h in range(i,int((nb_pages*self.vitesse_imprimmer)/60)+i) :
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
