# -*- coding: utf-8 -*-

import random, json, os, pymongo, pprint
from random import randrange

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pokidb"]
print(mydb)

atakikol = mydb["ataki"]
pokikol = mydb["poki"]
typykol = mydb["typy"]

result = atakikol.delete_many({})
result = typykol.delete_many({})

ataki = [
            {'nazwa' : 'Thunder_Shock', 'typ' : 'Elektryczny', 'pkt' : 8.33},
            {'nazwa' : 'Quick_Attack', 'typ' : 'Elektryczny', 'pkt' : 7.52},
            {'nazwa' : 'Discharge', 'typ' : 'Elektryczny', 'pkt' : 14.12},
            {'nazwa' : 'Thunder', 'typ' : 'Elektryczny', 'pkt' : 23.26},
            {'nazwa' : 'Bubble', 'typ' : 'Wodny', 'pkt' : 10.87},
            {'nazwa' : 'Body Slam', 'typ' : 'Wodny', 'pkt' : 25.64},
            {'nazwa' : 'Mud Bomb', 'typ' : 'Wodny', 'pkt' : 11.54},
            {'nazwa' : 'Bubble Beam','typ' : 'Wodny', 'pkt' : 10.34},
        ]

typy = [ {'typ' : 'Wodny'},
         {'typ' : 'Elektryczny'},
         {'typ' : 'Trawiasty'},
         {'typ' : 'Ognisty' } ]

poki = [ {'nazwa' : 'Rajczu', 'typ' : 'Elektryczny', 'hp' : 40, 'pkta' : 10, 'ataki' : ['Thunder_Shock', 'Quick_Attack', 'Discharge']},
         {'nazwa' : 'Blastoise', 'typ' : 'Wodny', 'hp' : 46, 'pkta' : 14, 'ataki' : ['Body Slam', 'Mud Bomb', 'Bubble Beam']},
       ]


x = atakikol.insert_many(ataki)
y = typykol.insert_many(typy)



def wybierz_typ():
    lista = []
    for l in typykol.find():
        lista.append(l['typ'])
    print('\nLista typow: ' + str(lista))
    status = False
    while status == False:
        print('\n')
        wybor = input('Wybierz typ z powyzszej listy, np. Trawiasty: \n')
        if wybor not in lista:
            print('Podales niewlasciwa wartosc!')
            status = False
        else:
            status = True
            return wybor

class Pokemon():
    def __init__(self, nazwa, typ, hp, pkta):	#pkta	
        self.nazwa = nazwa
        self.typ = typ
        self.hp = hp
        self.pkta = pkta
        self.ataki = []

    def __str__(self):
        return self.nazwa
    
    def wybierz_atak(self):
        i=0
        lista_atakow = []
        print('\n')
        for a in atakikol.find():
            print(str(a['typ']) + ' ' + str(a['nazwa']) + ' ' + str(a['pkt']))
            lista_atakow.append(a['nazwa'])
        print('\nWybierz 3 ataki z listy: \n')
        while i<3:
            wybrany_a = str(input())
            zapytanie = { "nazwa": wybrany_a }
            x = atakikol.find_one(zapytanie)
            if x == None:
                print('Sprawdz czy na pewno prawidlowo przepisales nazwe ataku! Uwzglednij wielkosc liter.')
            else:
                if x['typ']!=self.typ:
                    print('Ten atak nie pasuje do Twojego typu pokemona')
                else:
                    self.ataki.append(x)
                    i=i+1
        return self.ataki

    def atakuj(self,  atak, przeciwnik):
        przeciwnik.hp = przeciwnik.hp - atak['pkt']
        print('{0} atakuje przeciwnika i zadaje {1} obrazen ! \n Przeciwnikowi pozostalo {2} pkt zycia.\n'.format(self.nazwa, atak['pkt'], przeciwnik.hp))
        return przeciwnik.hp

class Atak():
    def __init__(self, nazwa, sila_ataku, typ):
        self.nazwa = nazwa
        self.typ = typ
        self.silaa = sila_ataku
    
    def info(self):
        print('Atak ' + nazwa + ' zabral przeciwnikowi' + str(sila_ataku) + ' pkt zycia')
        
    def __str__(self):
        return(self.nazwa)
        

print('Opcje:')
opcje ={
            1: 'Dodaj pokemona',
            2: 'Dodaj atak',
            3: 'Walcz',
            4: 'Wyjdz',
            }


for n in range(len(opcje)):
    print(str(n+1) + '.' + ' ' + opcje[n+1])
    

wybor = int(input('>'))


if wybor == 1:
    os.system('clear')
    nazwa = input('Wybierz nazwe dla nowego pokemona:\n')
    print('\n')
    typ = wybierz_typ()
    hp = int(input("\nPodaj ilosc puntkow hp (z zakresu od 1 do 50): "))
    while hp not in range(1, 51):
        hp = int(input('Blad! Licza powinna byc z zakresu od 1 do 50, sprobuj ponownie:'))
    pkta = int(input("\nPodaj ilosc puntkow ataku (z zakresu od 1 do 15): "))
    while pkta not in range(1, 16):
        pkta = int(input('Blad! Licza powinna byc z zakresu od 1 do 15, sprobuj ponownie:'))
    new = Pokemon(nazwa, typ, hp, pkta)
    new.wybierz_atak()
    result = pokikol.insert_one({'nazwa' : new.nazwa,
                                 'typ' : new.typ,
                                 'hp' : new.hp,
                                 'pkta' : new.pkta,
                                 'ataki' : new.ataki})

    for pokemon in pokikol.find():
        print(pokemon)


elif wybor == 2:
    os.system('clear')
    nazwaa = input('Wybierz nazwe dla nowego ataku:\n')
    typaa = wybierz_typ()
    silaa = int(input("\nPodaj sile obrazen ataku ( liczba z zakresu od 1 do 30): "))
    while silaa not in range(1, 31):
        silaa = int(input('Blad! Licza powinna byc z zakresu od 1 do 30, sprobuj ponownie:'))
    nowy_atak = Atak(nazwaa, typaa, silaa)
    print(nowy_atak)
    result = atakikol.insert_one({'nazwa' : nowy_atak.nazwa,
                                 'typ' : nowy_atak.typ,
                                 'pkt' : nowy_atak.silaa,
                                })

    
elif wybor == 3:
    os.system('clear')
    print('-->Pojedynek<--\n \n Wybierz dwa pokemony do walki z ponizszej listy:\n')
    for element in pokikol.find():
        pprint.pprint('{0} ({1})'.format(element['nazwa'], element['typ']))
    i = 0
    pokemony = []
    while i < 2:
        wybor = input('\n Twoj {0} wybor: '.format(i+1))
        myquery = { "nazwa": wybor }
        wynik_zapytania = pokikol.find_one(myquery) 
        if wynik_zapytania == None:
            print('\nPrawdopodobnie zle przepisales nazwe. Zwroc uwage na wielkosc liter.')
        else:
            pokemon = Pokemon(wynik_zapytania['nazwa'],
                              wynik_zapytania['typ'],
                              wynik_zapytania['hp'],
                              wynik_zapytania['pkta'],
                              )
            for element in wynik_zapytania['ataki']:
                pokemon.ataki.append(element)
            pokemony.append(pokemon)
            i=i+1
    while pokemony[0].hp > 0 and pokemony[1].hp > 0 :
        print('\nWybierz atak:\n')
        i=0
        for atak in pokemony[0].ataki:
            print(i, atak['nazwa'])
            i += 1
        print('\n')

        x = int(input('Wybierz atak z powyzszej listy:'))
        pokemony[1].hp = pokemony[0].atakuj(pokemony[0].ataki[x], pokemony[1])
        pokemony[0].hp = pokemony[1].atakuj(pokemony[1].ataki[randrange(3)], pokemony[0])
    

elif wybor == 4 :
    print('-->Zakonczono dzialanie programu<--')
    quit()


