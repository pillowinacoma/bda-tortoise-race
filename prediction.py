import json
from os import listdir, path
from pprint import pprint


source = 'results'

def predictRegulier(pos, deltatop, speed):
    return pos + deltatop * speed
def predictFatigue(pos, deltatop, max_value, rythme):
    cycle = [i for i in range(max_value, 0, -rythme)] + [i for i in range(0, max_value, rythme)]
    print(cycle)

def main(course, id, top, position, temp, quali, deltatop):

    input_file = f"{source}/{course}"
    # files = list(map(lambda x: path.join(
    #     input_file, x), listdir(input_file)))
    with open("results/tiny/1.json") as f:
        modele = json.loads(f.read())
        if len(modele) == 1 :
            turtle_type = list(modele.keys())[0]
            params = modele[turtle_type][0]['params']
            predictFatigue(position, deltatop, params[1], params[2])



if __name__ == "__main__":
    course = 'tiny'
    id = 1
    top = 807356
    position = 127966586
    quali = 0.3100529516794682
    temp = 14.470235587748288
    deltatop=1

    main(course, id, top, position, temp, quali, deltatop)
