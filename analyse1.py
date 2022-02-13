import json
import operator
from os import listdir, curdir, truncate
from os import path
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import struct, collect_list, udf
from utils import isCyclique, isFatiguee, isRegulier, isSameCycle

compte = "p1807434"
# input_file = "hdfs:///user/" + compte + "/data3/tiny/0"
data_dir = "data3"
type_dir = "small"
result_file_name = "result.json"


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


def mapTortue(tortuePath, ss):
    df = ss.read.options(header=True, inferSchema=True, delimiter=',').csv(
        tortuePath).select("*").distinct().sort("top")
    grouped_df = df.groupBy("id", "temperature", "qualite")\
        .agg(
        collect_list("vitesse").alias("vitesses")
    )

    print("##-"+tortuePath+"-##############################################################################################################")

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

    # grouped_df.rdd.map(analyseVitesse).map(lambda x: {'type': x[3][0], 'params': x[3], 'temp': x[1], 'quali': x[2]}).foreach(print)
    envByTypeDict = grouped_df\
        .rdd\
        .map(analyseVitesse)\
        .map(lambda x: {x[3][0]: [
            {'params': x[3], 'env': [{'temp': x[1], 'quali': x[2]}]}]})\
        .reduce(tempQualiSpeedsReducer)

    tortueId = tortuePath.split("/")[-1]
    # Path(f"./results/{tortueId}.json").touch(exist_ok=True)
    with open("results/"+type_dir+"/"+tortueId+".json", "w") as outfile:
        json.dump(envByTypeDict, outfile, indent=4)

    # grouped_df.rdd\
    #        .map(analyseVitesse)\
    #        .map(lambda x: {x[3][0]: [{'params': x[3], 'env': [{'temp': x[1], 'quali': x[2]}]}]})\
    #        .foreach(pprint)


# Main process


def main():
    # sc = pyspark.SparkContext(appName="Tp-tortues-" + compte)
    Path("./results/"+type_dir+"").mkdir(parents=True, exist_ok=True)
    ss = SparkSession.builder.appName("Tp-tortues-" + compte).getOrCreate()
    input_file = data_dir+"/"+{type_dir}+"/"
    # df = ss.read.options(header=True, inferSchema=True, delimiter=',').csv(input_file)

    print("##-1-##############################################################################################################")
    turtles = list(map(lambda x: path.join(
        input_file, x), listdir(input_file)))
    print(turtles)
    for tPath in turtles:
        mapTortue(tPath, ss)
    # df.printSchema()
    # df.show()
    # df['vitesse'].tolist()

    print("##-2-##############################################################################################################")


if __name__ == "__main__":
    main()
