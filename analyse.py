import glob
import os
import csv
from pathlib import Path
from pprint import pprint
from turtle import position
from utils import isCyclique, isFatiguee, isRegulier

DATA_DIR = "./data0"
TYPE = "tiny"

prev = {'position': -1, 'top': -1}


def analyseFile(fileName):
    result = {'vitesses': []}
    with open(fileName, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:

            stats = dict(row,
                         delta=(int(row['top'])-prev['top']))
            # if stats['delta'] > 1 : print(stats)

            if prev['position'] != -1:
                stats['vitesse'] = int(row['vitesse'])

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
        cyclique = isCyclique(result['vitesses'][1:])
        regulier = isRegulier(result['vitesses'][1:])
        fatigue = isFatiguee(result['vitesses'][1:])
        trueList = [cyclique['cyclique'],
                    regulier['regulier'], fatigue['fatigue']]
        if trueList.count(True) != 1:
            # print(result)
            # print("Cyclique", cyclique)
            # print("Regulier", regulier)
            # print("Fatigué", fatigue)
            return {
                'isGood': False
            }
        result = [cyclique, regulier, fatigue][trueList.index(True)]
        return {
            'isGood': True,
            'result': result,
        }


os.chdir(f"{DATA_DIR}/{TYPE}")

prev = {'position': -1, 'top': -1}

for dirCounter, dir in enumerate(sorted(glob.glob("*"), key=lambda a: int(a.split("-")[0]))):
    for fileCounter, file in enumerate(sorted(glob.glob(f"{dir}/*"), key=lambda a: int(a.split("/")[1].split("-")[0]))):
        # if dirCounter < 10:
        print('________________', file)
        fileAnalyse = analyseFile(file)
        if fileAnalyse['isGood'] : print(fileAnalyse)
        # break
