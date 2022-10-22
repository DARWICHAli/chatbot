
def hour_calc(i):
    date = 0
    hour= 0
    min= 0
    min_of_day = 60 *24
    if(i < min_of_day):
        date = "Monday"
    elif(i < min_of_day*2):
        date = "Tuesday"
    elif(i < min_of_day*3):
        date = "Wednesday"
    elif(i < min_of_day*4):
        date = "Thursday"
    elif(i < min_of_day*5):
        date = "Friday"
    elif(i < min_of_day*6):
        date = "Saturday"
    else:
        date = "Sunday"

    tmp = i%min_of_day
    min = tmp%60
    hour = tmp -min
    hour = hour/60
    res = "{}:{}".format(int(hour), int(min))
    return [date,res]


class ordonnanceur(object):
    """docstring for ordonnanceur."""

    length_array = 10080 # 7 jour * 24h * 60 mins
    array = [length_array] # 0 creneau libre  sinon 1  -1 si date block
    vitesse_imprimmer = 1 # 1 page/sec
    array = [0 for i in range(length_array)]


    def __init__(self):
        super(ordonnanceur, self).__init__()
        self.array = [0 for i in range(self.length_array)]

    def add_creneau(self, nb_pages):
        if(nb_pages <= 0):
            print("error on number of pages")
            return
        for i in range(self.length_array):
            if(self.array[i] == 0):
                if(nb_pages+i <= self.length_array):
                    print('reserving time')
                    date1 = hour_calc(i)

                    for h in range(i,(nb_pages*self.vitesse_imprimmer)+i) :
                        self.array[h] = 1

                    date2 = hour_calc(h)
                    # print(date1)
                    # print(date2)
                    return date1 ,date2
                    break
                else :
                    print('il y a plus de creneau ')
                    break
            else :
                print('il y a plus de creneau ')
                break

    # block a specific date
    def bloque(self,jour):
        len_day = self.length_array /7
        self.array = [-1 for i in range(len_day*jour,len_day*jour+1)]



def main():

    x = ordonnanceur()
    date1 ,date2 =x.add_creneau(456)
    print(date1,date2)
    pass





if __name__ == '__main__':
    main()