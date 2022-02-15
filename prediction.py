import json
from os import listdir, path
from pprint import pprint
from statistics import mode
from sys import argv
from math import dist


source = 'results'


def predictRegulier(deltatop, pos1, pos2):
    return pos1 + deltatop * (pos2 - pos1)


def predictFatigue(deltatop, pos1, pos2, pos3, max_value, rythme):
    cycle = [i for i in range(max_value, 0, -rythme)] + \
        [i for i in range(0, max_value, rythme)]
    cycle_size = len(cycle)
    two_speeds = [pos2 - pos1, pos3 - pos2]
    arr_speed_at_pos2 = [i for i, elem in enumerate(cycle) if(
        elem == two_speeds[0] and cycle[(i + 1) % cycle_size] == two_speeds[1])]
    idx_speed_at_pos2 = arr_speed_at_pos2[0] if len(arr_speed_at_pos2) == 1 else -1
    if idx_speed_at_pos2 == -1: return "positions ne sont pas coherents avec le cycle"

    result = pos1
    for i in range(deltatop):
        result += cycle[(idx_speed_at_pos2 + i) % cycle_size]

    return result


def predictCyclique(deltatop, pos1, pos2, pos3, cycle, fenetre):
    two_speeds = [pos2 - pos1, pos3 - pos2]
    idx_speed_at_pos2 = [i for i, elem in enumerate(cycle) if(
        elem == two_speeds[0] and cycle[(i + 1) % fenetre] == two_speeds[1])][0]

    result = pos1
    for i in range(deltatop):
        result += cycle[(idx_speed_at_pos2 + i) % fenetre]

    return result


def main(course, id, top, pos1, pos2, pos3, temp, quali, deltatop):

    input_file = f"{source}/{course}"
    # files = list(map(lambda x: path.join(
    #     input_file, x), listdir(input_file)))
    with open(f"results/{course}/{id}.json") as f:
        modele = json.loads(f.read())
        if len(modele) == 1 and len(modele[list(modele.keys())[0]]) == 1:
            turtle_type = list(modele.keys())[0]
            params = modele[turtle_type][0]['params']
            if turtle_type == 'regulier':
                return predictRegulier(deltatop, pos1, pos2)
            elif turtle_type == 'fatigue':
                return predictFatigue(deltatop, pos1,
                      pos2, pos3, params[1], params[2])
            elif turtle_type == 'cyclique':
                return predictCyclique(deltatop, pos1,
                      pos2, pos3, params[1], params[2])
        else: 
            qualiTempParamsList = []
            for type in modele:
                for typeConf in modele[type]:
                    env = typeConf['env']
                    params = typeConf['params']
                    # pprint(env)
                    # pprint(params)
                    def mapEnv(singleEnv):
                        c = singleEnv
                        c ['params'] = params
                        return c
                    qualiTempParamsList += [elem for elem in list(map(mapEnv, env)) if elem['params'][0] == "fatigue" or "cyclique" or "regulier"]
            targetConfig = min(qualiTempParamsList, key=lambda x: dist([temp, quali], [x['temp'], x['quali']]))

            params = targetConfig['params']
            print(params)
            if params[0] == 'regulier':
                return predictRegulier(deltatop, pos1, pos2)
            elif params[0] == 'fatigue':
                return predictFatigue(deltatop, pos1,
                      pos2, pos3, params[1], params[2])
            elif params[0] == 'cyclique':
                return predictCyclique(deltatop, pos1,
                      pos2, pos3, params[1], params[2])



if __name__ == "__main__":
    course = argv[1]
    id = int(argv[2])
    top = int(argv[3])
    pos1 = int(argv[4])
    pos2 = int(argv[5])
    pos3 = int(argv[6])
    temp = float(argv[7])
    quali = float(argv[8])
    deltatop = int(argv[9])
    print(main(course, id, top, pos1, pos2, pos3, temp, quali, deltatop))
