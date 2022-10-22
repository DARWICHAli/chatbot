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
                    # self.array[self.array >= i & self.array < (nb_pages*vitesse_imprimmer)+i] = [1 for h in range(i,nb_pages+i)]
                    # self.array.loc[(self.array == -1) & (self.array == -1)]
                    for h in range(i,(nb_pages*self.vitesse_imprimmer)+i) :
                        self.array[h] = 1
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

    # x = ordonnanceur()
    # x.add_creneau(10080)
    # pass





if __name__ == '__main__':
    main()
