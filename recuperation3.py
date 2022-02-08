from asyncio.log import logger
from datetime import datetime
import sys
import requests
from pathlib import Path
from datetime import datetime
import time
from pprint import pprint
import csv


def addQualiTemp(x, quali, temp, speed):
    x['qualite'] = quali
    x['temperature'] = temp
    x['vitesse'] = speed
    return x


data = {}

data_size = {"tiny": 10,
             "small": 100,
             "medium": 500,
             "large": 2000}


def getData(type='tiny', targetDir='./data', fileSize=1000):
    lastTop = 0
    data[type] = {}

    for i in range(data_size[type]):
        Path(f"./{targetDir}/{type}/{i}").mkdir(parents=True, exist_ok=True)

    while(True):
        time.sleep(2)
        try : 
            request = requests.get(
                f'http://tortues.ecoquery.os.univ-lyon1.fr/race/{type}')
        except requests.Timeout as err : 
            logger.error({"message : ": err.response})
            continue
        except requests.ConnectionError as err : 
            logger.error({"message : " : err.response})
            continue
        rawData = request.json()

        if(request.status_code != 200):
            print(f"REQUEST : {type}\t{request.status_code} ")
            continue
        if rawData['tortoises'][0]['top'] == lastTop:
            continue


        qualite = rawData['qualite']
        temperature = rawData['temperature']

        tortoises = list(map(lambda x: addQualiTemp(
            x, qualite, temperature, speed=x['position'] - data[type][x['id']][lastTop]['position'] if lastTop != 0 else 0), rawData['tortoises']))

        lastTop = tortoises[0]['top']
        for tortoise in tortoises:
            if(tortoise['id'] not in data[type]):
                data[type][tortoise['id']] = {tortoise['top']: tortoise}
            else:
                data[type][tortoise['id']][tortoise['top']] = tortoise

            if(len(data[type][tortoise['id']]) == fileSize + 1):
                items = list(data[type][tortoise['id']].items())
                Path(
                    f"{targetDir}/{type}/{tortoise['id']}/{items[0][0]}-{items[-1][0]}.csv").touch(exist_ok=True)
                with open(f"{targetDir}/{type}/{tortoise['id']}/{items[0][0]}-{items[-1][0]}.csv", 'w', newline='') as csvfile:
                    fieldnames = ['top', 'id', 'position', 'vitesse',
                                  'qualite', 'temperature']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for daton in data[type][tortoise['id']].items():
                        writer.writerow(daton[1])
                    # pprint(data[type][tortoise['id']])
                    data[type][tortoise['id']] = {tortoise['top']: tortoise}

        print(
            f"SIZE : {type}\t{len(data[type][0])} ")


getData(sys.argv[1], sys.argv[2], int(sys.argv[3]))
