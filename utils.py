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
                return {
                    'cyclique': False
                }
            return {
                'cyclique': True,
                'cycle': cycle,
                'fenetre': len(cycle),
            }
    return {
        'cyclique': False
    }


def isRegulier(speeds=[]):
    if(len(speeds) > 1):
        first = speeds[0]
        for speed in speeds[1:2]:
            if speed == 0 or speed != first:
                return {
                    'regulier': False
                }
        return {
            'regulier': True,
            'vitesse': first,
        }
    return {
        'regulier': False
    }


def isFatiguee(speeds=[]):
    if(len(speeds) > 1):
        try:
            first_zero_index = speeds.index(0)
        except:
            return {
                'fatigue': False
            }
        try:
            second_zero_index = first_zero_index + \
                speeds[first_zero_index + 1:].index(0) + 1
        except:
            return {
                'fatigue': False
            }
        cycle = speeds[first_zero_index:second_zero_index + 1]
        max_speed = max(cycle)
        rythme = max_speed - cycle[cycle.index(max_speed) + 1]
        if rythme == 0:
            return {
                'fatigue': False
            }
        return {
            'fatigue': True,
            'vitesse_initiale': max_speed,
            'rythme': rythme,
        }

    return {
        'fatigue': False
    }
