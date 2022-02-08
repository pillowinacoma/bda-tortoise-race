from datetime import datetime
import logging
import requests
from pathlib import Path
from datetime import datetime
import time
from pprint import pprint
import csv
import threading


def addQualiTemp(x, quali, temp):
    x['qualite'] = quali
    x['temperature'] = temp
    return x


data = {}


def getData(type='tiny'):
    data[type] = {}
    while(True):
        request = requests.get( f'http://tortues.ecoquery.os.univ-lyon1.fr/race/{type}')
        rawData = request.json()

        if(request.status_code != 200): print(f"REQUEST : {type}\t{request.status_code} ")
        for i in range(len(rawData['tortoises'])):
            Path(f"./data/{type}/{i}").mkdir(parents=True, exist_ok=True)
        qualite = rawData['qualite']
        temperature = rawData['temperature']

        tortoises = list(map(lambda x: addQualiTemp(
            x, qualite, temperature), rawData['tortoises']))

        for tortoise in tortoises:
            if(tortoise['id'] not in data[type]):
                data[type][tortoise['id']] = {tortoise['top']: tortoise}
            else:
                data[type][tortoise['id']][tortoise['top']] = tortoise


            if(len(data[type][tortoise['id']]) == 100):
                items = list(data[type][tortoise['id']].items())
                Path(
                    f"./data/{type}/{tortoise['id']}/{items[0][0]}-{items[-1][0]}.csv").touch(exist_ok=True)
                with open(f"./data/{type}/{tortoise['id']}/{items[0][0]}-{items[-1][0]}.csv", 'w', newline='') as csvfile:
                    fieldnames = ['top', 'id', 'position',
                                  'qualite', 'temperature']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for daton in data[type][tortoise['id']].items():
                        writer.writerow(daton[1])
                    # pprint(data[type][tortoise['id']])
                    data[type][tortoise['id']] = {}

        print(f"SIZE : {type}\t{len( data[type][tortoise['id']]) * len(data[type])} ")
        time.sleep(2)


tinyThread = threading.Thread(target=getData, args=['tiny'])
smallThread = threading.Thread(target=getData, args=['small'])
mediumThread = threading.Thread(target=getData, args=['medium'])
largeThread = threading.Thread(target=getData, args=['large'])

tinyThread.start()
smallThread.start()
mediumThread.start()
largeThread.start()
