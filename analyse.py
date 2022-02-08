import glob
import os
import csv
from pathlib import Path
from pprint import pprint
from turtle import position
from utils import isCyclique, isFatiguee, isRegulier

DATA_DIR = "./data0"
TYPE = "tiny"
TORTOISE_ID = '6'

prev = {'position': -1, 'top': -1}
result = {'vitesses': []}


def analyseFile(fileName):
    with open(fileName, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:

            stats = dict(row,
                         delta=(int(row['top'])-prev['top']))
            # if stats['delta'] > 1 : print(stats)

            if prev['position'] != -1:
                stats['vitesse'] = int(row['position']) - prev['position']

            if('temperature' not in result):
                result['temperature'] = stats['temperature']
            # elif(result['temperature'] != stats['temperature']):
            #     print('')

            if('qualite' not in result):
                result['qualite'] = stats['qualite']
            # elif(result['qualite'] != stats['qualite']):
            #     print('')

            if(prev['position'] != -1 and prev['top'] != stats['top']):
                result['vitesses'].append(stats['vitesse'])

            prev['position'] = int(row['position'])
            prev['top'] = int(row['top'])
        # print(result)
        print("Cyclique", isCyclique(result['vitesses'][1:]))
        print("Regulier",isRegulier(result['vitesses'][1:]))
        print("Fatigué",isFatiguee(result['vitesses'][1:]))


os.chdir(f"{DATA_DIR}/{TYPE}/{TORTOISE_ID}")

prev = {'position': -1, 'top': -1}

for counter, file in enumerate(sorted(glob.glob("*"))):
    if counter < 10:
        analyseFile(file)
    else:
        break
