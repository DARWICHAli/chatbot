class ordonnanceur(object):
    """docstring for ordonnanceur."""

    lenght_array = 10080 # 7 jour * 24h * 60 mins
    array = [lenght_array] # 0 creneau libre  sinon 1
    vitesse_imprimmer = 1 # 1 page/sec
    array = [0 for i in range(lenght_array)]


    def __init__(self):
        super(ordonnanceur, self).__init__()
        array = [0 for i in range(lenght_array)]

    def add_creneau(nb_pages):
        for i in range(lenght_array):
            if(array[i] == 0):
                if(nb_pages+i < lenght_array):
                    print('reserving time')
                    array = [1 for h in range(i,nb_pages+i)]
                else :
                    print('il y a plus de creneau ')



def main():
    pass





if __name__ == '__main__':
    main()
