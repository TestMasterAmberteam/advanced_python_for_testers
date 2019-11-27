import configparser
import sched
from os import listdir
from os.path import isfile, join
from random import randint, choice
from time import time, sleep

TEST_DATA_PATH = 'test_data'

# region Załaduj ini
config = configparser.ConfigParser(interpolation=None)
config.read_file(open('mt101.ini'))
NUMBER_OF_TRANSFERS = int(config['General']['number_of_transfers'])
LARGER_NUMBER_OF_TRANSFERS = int(config['General']['larger_number_of_transfers'])
LARGER_EVERY = int(config['General']['larger_every'])
INTERVAL = int(config['General']['itnerval'])
# endregion

s = sched.scheduler(time, sleep)
FILES = [join(TEST_DATA_PATH, f) for f in listdir(TEST_DATA_PATH) if f.endswith('.txt') and isfile(join(TEST_DATA_PATH, f))]
def get_mt101():
    while True:
        f = choice(FILES)
        with open(f, 'rt') as fin:
            print(f'Otwieram {f}')
            line = fin.readline()
            while line:
                if line[0] == chr(1): # początek komunikatu
                    mt101 = line
                    line = fin.readline()
                    # czy nie końcówka pliku
                    if line.startswith('DATE'):
                        break  # zaznacz,  że plik się skończył
                    while line[0] != chr(3): # czekaj na koniec komunikatu
                        mt101 += line
                        line = fin.readline()
                    # dokończ komunikat i zwróc
                    mt101 += line
                    yield mt101
                line = fin.readline()


gen_mt101 = get_mt101()
generation = 0 # licznik wygenerowanych plików
flog = open('mt101.csv', 'at')
flog.write('mt101_folder;field_20;field_21;timestamp\n')
state = 0

def generuj_paczke():
    global generation, state
    s.enter(INTERVAL, 1, generuj_paczke)
    generation += 1
    generation_time = time()
    print(f'Generowanie paczki {generation} - {generation_time:.0f} - {NUMBER_OF_TRANSFERS if generation % LARGER_EVERY != 3 else LARGER_NUMBER_OF_TRANSFERS}')
    with open(f'{config["General"]["mt101_folder"]}/{generation_time:.0f}.txt','wt') as fout:
        # co LARGER_EVERY ma być większa paczka
        for i in range(NUMBER_OF_TRANSFERS if generation % LARGER_EVERY != 3 else LARGER_NUMBER_OF_TRANSFERS):
            reference = randint(1,10**14-1)
            mt101 = next(gen_mt101)
            nr_przelewu = 0
            for line in mt101.split('\n'): # podmień pola 20, 21, 59
                if line.startswith(':20:'):
                    line = f':20:{reference:014d}'
                elif line.startswith(':21:'):
                    nr_przelewu += 1
                    line = f':21:{reference:014d}{nr_przelewu:02d}'
                    flog.write(f'{config["General"]["mt101_folder"]};{reference:014d};{reference:014d}{nr_przelewu:02d};{generation_time:.0f}\n')
                elif line.startswith(':59:'):
                    state = 59 # obrabiamy drugą linię pola 59
                elif state == 59:
                    if not line.startswith(':70:'): # zastąp drugą linijkę pola 59
                        line = f'{reference:014d}{nr_przelewu:02d}'
                    else: # dodaj linijkę i pole 70 zapisz normalnie
                        fout.write(f'{reference:014d}{nr_przelewu:02d}\n')
                    state = 0
                fout.write(line)
                fout.write('\n')



# uruchom generowanie, które zascheduluje następne uruchamiania
generuj_paczke()
s.run()
