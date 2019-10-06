import re


# (NL key word/phrase, paramKey, value)
keyword_map = [
    ('scatterplot', {'type': 'point'}),
    ('scatter plot', {'type': 'point'}),
    ('point chart', {'type': 'point'}),
    ('circle chart', {'type': 'circle'}),
]


def _normalize(command):
    return ' '.join([w.strip() for w in command.strip().split()]).lower()


def _col_map(colNames):
    '''Generate keyword_map based on col names
    '''
    col_map = []
    for y in colNames:
        for x in colNames:
            col_map.append((y.lower() + ' by ' + x.lower(), {'y': y, 'x': x}))
    for x in colNames:
        col_map.append(('by ' + x.lower(), {'x': x}))
    for n in colNames:
        col_map.append((n.lower(), {'axis': n}))
    return col_map



def parse(colNames, command):
    command = _normalize(command)
    res = {}
    keyword_map_copy = [t for t in keyword_map]
    keyword_map_copy += _col_map(colNames)
    while True:
        flag = False
        for i in range(len(keyword_map_copy)):
            if command.find(keyword_map_copy[i][0]) == 0:
                flag = True
                dic = keyword_map_copy[i][1]
                for key in dic:
                    if key not in res:
                        res[key] = [dic[key]]
                    else:
                        res[key].append(dic[key])
                command = command[len(keyword_map_copy[i][0])+1:]
                break
        if not flag:
            i = command.find(' ')
            if i == -1:
                break
            command = command[i+1:]
    return res

