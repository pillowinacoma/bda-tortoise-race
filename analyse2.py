import json
import operator
from os import listdir
from os import path, makedirs
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import struct, collect_list, udf
import sys

compte = "p1807434"
data_dir = "data3"
# type_dir = "small"
result_file_name = "result.json"


def isCyclique(speeds=[]):
    if(len(speeds) > 1):
        first = speeds[0]
        try:
            index_cycle = speeds[1:].index(first) + 1
        except:
            index_cycle = -1
        if index_cycle > 1:
            cycle = speeds[0:index_cycle]
            if 0 in cycle:
                return ('non cyclique')
            return ('cyclique', cycle, len(cycle))
    return ('non cyclique')


def isRegulier(speeds=[]):
    if(len(speeds) > 1):
        first = speeds[0]
        for speed in speeds[1:2]:
            if speed == 0 or speed != first:
                return ('non regulier')
        return ('regulier', first)
    return ('non regulier')


def isFatiguee(speeds=[]):
    if(len(speeds) > 1):
        try:
            first_zero_index = speeds.index(0)
        except:
            return ('non fatigue')
        try:
            second_zero_index = first_zero_index + \
                speeds[first_zero_index + 1:].index(0) + 1
        except:
            return ('non fatigue')
        cycle = speeds[first_zero_index:second_zero_index + 1]
        max_speed = max(cycle)
        rythme = max_speed - cycle[cycle.index(max_speed) + 1]
        if rythme == 0:
            ('non fatigue')
        return ('fatigue', max_speed, rythme)

    return ('non fatigue')


def isSameCycle(cycle1, cycle2):
    fc1 = cycle1[0]
    try:
        lc2 = cycle2.index(fc1)
    except:
        return False
    tc2 = cycle2[lc2:] + cycle2[:lc2]
    return cycle1 == tc2


def sorter(l):
    res = sorted(l, key=operator.itemgetter(0))
    return [item[1] for item in res]


def analyseVitesse(entry):
    id = entry[0]
    temp = entry[1]
    quali = entry[2]
    speeds = entry[3]
    regulier = isRegulier(speeds)
    cyclique = isCyclique(speeds)
    fatigue = isFatiguee(speeds)

    if regulier[0] == 'regulier':
        return (id, temp, quali, regulier)
    if cyclique[0] == 'cyclique':
        return (id, temp, quali, cyclique)
    if fatigue[0] == 'fatigue':
        return (id, temp, quali, fatigue)
    return (id, temp, quali, ('non definie', ''))


def mapTortue(tortuePath, ss, source, target, type):
    df = ss.read.options(header=True, inferSchema=True, delimiter=',').csv(
        tortuePath).select("*").distinct().sort("top")
    grouped_df = df.groupBy("id", "temperature", "qualite")\
        .agg(
        collect_list("vitesse").alias("vitesses")
    )

    def tempQualiSpeedsReducer(acc, curr):
        if(list(curr.keys())[0] == 'cyclique'):
            current = curr['cyclique'][0]
            cycle = current['params'][1]
            fenetre = current['params'][2]
            env = current['env'][0]
            if 'cyclique' in acc:
                for accumulated in acc['cyclique']:
                    if fenetre == accumulated['params'][2] and isSameCycle(accumulated['params'][1], cycle):
                        accumulated['env'].append(env)
                    else:
                        if next((elem for elem in acc['cyclique'] if elem['params'] == current['params']), None) == None:
                            acc['cyclique'].append(current)
            else:
                acc['cyclique'] = curr['cyclique']

        if(list(curr.keys())[0] == 'fatigue'):
            current = curr['fatigue'][0]
            env = current['env'][0]
            if 'fatigue' in acc:
                for accumulated in acc['fatigue']:
                    if current['params'] == accumulated['params']:
                        accumulated['env'].append(env)
                    else:
                        if next((elem for elem in acc['fatigue'] if elem['params'] == current['params']), None) == None:
                            acc['fatigue'].append(current)
            else:
                acc['fatigue'] = curr['fatigue']

        elif(list(curr.keys())[0] == 'regulier'):
            current = curr['regulier'][0]
            env = current['env'][0]
            if 'regulier' in acc:
                for accumulated in acc['regulier']:
                    if current['params'] == accumulated['params']:
                        accumulated['env'].append(env)
                    else:
                        if next((elem for elem in acc['regulier'] if elem['params'] == current['params']), None) == None:
                            acc['regulier'].append(current)
            else:
                acc['regulier'] = curr['regulier']

        return acc

    envByTypeDict = grouped_df\
        .rdd\
        .map(analyseVitesse)\
        .map(lambda x: {x[3][0]: [
            {'params': x[3], 'env': [{'temp': x[1], 'quali': x[2]}]}]})\
        .reduce(tempQualiSpeedsReducer)

    tortueId = tortuePath.split("/")[-1]

    with open("./"+target+"/"+type+"/"+tortueId+".json", "w") as outfile:
        json.dump(envByTypeDict, outfile, indent=4)


def main(source, target, type):
    # sc = pyspark.SparkContext(appName="Tp-tortues-" + compte)
    # target_dir = "hdfs:///user/"+compte+"/"+target+"/"+type+""
    target_dir = "./"+target+"/"+type+""
    if not path.exists(target_dir):
        makedirs(target_dir)
    ss = SparkSession.builder.appName("Tp-tortues-" + compte).getOrCreate()
    # input_file = "hdfs:///user/"+compte+"/"+source+"/"+type
    input_file = "./"+source+"/"+type
    # df = ss.read.options(header=True, inferSchema=True, delimiter=',').csv(input_file)

    print("##-1-##############################################################################################################")
    turtles = list(map(lambda x: path.join(
        input_file, x), listdir(input_file)))
    for tPath in turtles:
        mapTortue(tPath, ss, source, target, type)
    # df.printSchema()
    # df.show()
    # df['vitesse'].tolist()

    print("##-2-##############################################################################################################")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
