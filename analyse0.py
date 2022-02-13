import glob
import os
import csv
from pathlib import Path
from pprint import pprint
from turtle import position
from utils import isCyclique, isFatiguee, isRegulier

DATA_DIR = "./data3"
TYPE = "small"

prev = {'position': -1, 'top': -1}


def analyseFile(fileName):
    results = []
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
        cyclique = isCyclique(result['vitesses'])
        regulier = isRegulier(result['vitesses'])
        fatigue = isFatiguee(result['vitesses'])
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
        res = [cyclique, regulier, fatigue][trueList.index(True)]

        return {
            'isGood': True,
            'result': res,
            'temperature': result['temperature'],
            'qualite': result['qualite'],
        }


def mapFile(fileName):
    speeds = {}
    prevTop = -1
    with open(fileName, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for counter, row in enumerate(reader):
            if counter != 0:
                if prevTop == -1:
                    prevTop = int(row['top'])

                qualite = row['qualite']
                temperature = row['temperature']
                emptySpeeds = [-1 for i in range(int(row['top']) - prevTop - 1)] if int(
                    row['top']) - prevTop > 1 else []
                emptySpeeds.append(row['vitesse'])

                if f"{qualite},{temperature}" in speeds:
                    speeds[f"{qualite},{temperature}"].extend(emptySpeeds)
                else:
                    speeds[f"{qualite},{temperature}"] = emptySpeeds

                prevTop = int(row['top'])

    return speeds


os.chdir(f"{DATA_DIR}/{TYPE}")

prev = {'position': -1, 'top': -1}

for dirCounter, dir in enumerate(sorted(glob.glob("*"), key=lambda a: int(a.split("-")[0]))):
    for fileCounter, file in enumerate(sorted(glob.glob(f"{dir}/*"), key=lambda a: int(a.split("/")[1].split("-")[0]))):
        # if dirCounter < 10:
        speedsByTempQuali = {}
        # print('________________ FILE', file)
        # print('________________ TORTOISE', file.split('/')[0])
        fileAnalyse = mapFile(file)
        for key in fileAnalyse.keys():
            if key in speedsByTempQuali:
                speedsByTempQuali[key].extend(fileAnalyse[key])
            else: 
                speedsByTempQuali[key] = fileAnalyse[key]
        k = next(iter(fileAnalyse))
        cyclique = isCyclique(speedsByTempQuali[k])
        regulier = isRegulier(speedsByTempQuali[k])
        fatigue = isFatiguee(speedsByTempQuali[k])
        trueList = [cyclique['cyclique'],
                    regulier['regulier'], fatigue['fatigue']]
        if trueList[2]: print(trueList)
        if trueList.count(True) == 1:
            res = [cyclique, regulier, fatigue][trueList.index(True)]
            # print(res)
            break
        
        

        # if fileAnalyse['isGood'] : print(fileAnalyse)
