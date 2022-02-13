from functools import reduce


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
    lc2 = cycle2.index(fc1)
    tc2 = cycle2[lc2:] + cycle2[:lc2]
    return cycle1 == tc2


def test(speeds):
    temp = 0.0
    quali = 0.0
    regulier = isRegulier(speeds)
    cyclique = isCyclique(speeds)
    fatigue = isFatiguee(speeds)

    res = (temp, quali, {'isGood': False})

    if regulier['regulier']:
        return (temp, quali, {'result': regulier, 'isGood': True})
    if cyclique['cyclique']:
        return (temp, quali, {'result': cyclique, 'isGood': True})
    if fatigue['fatigue']:
        return (temp, quali, {'result': fatigue, 'isGood': True})
    return (temp, quali, {'isGood': False})


if __name__ == "__main__":
    print(test([3, 2, 1, 0, 1, 2, 3, 2, 1, 0]))
