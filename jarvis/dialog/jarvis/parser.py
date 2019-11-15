import re
import numpy as np
from . import ml_parser as mlp


class Parser:
    
    def __init__(self, col_names):
        self.col_names = col_names
        colors = set([
            'black', 'blue', 'brown', 'dark blue', 'gray', 'grey', 'dark gray', 'dark grey',
            'green', 'dark green', 'orange', 'dark orange', 'red', 'dark red', 'pink', 'deep pink',
            'gold', 'light blue', 'light gray', 'light grey', 'light green', 'light pink',
            'yellow', 'light yellow', 'purple', 'silver', 'white'
        ])
        self.colors = set()
        self.keywords = {}
        kvs = {
            # Chart type values
            "area chart": "area",
            "area graph": "area",
            "bar chart": "bar",
            "bar graph": "bar",
            "barchart": "bar",
            "rectangle": "rect",
            "rectangles": "rect",
            "circle": "circle",
            "circles": "circle",
            "scatterplot": "circle",
            "scatter plot": "circle",
            "square chart": "square",
            "square graph": "square",
            "square": "square",
            "squares": "square",
            "line chart": "line",
            "line graph": "line",
            'histogram': 'bar',
            "line": "line",  # Can either be line chart or show line or not
            "lines": "line",  # Can either be line chart or show line or not 
            "point chart": "circle",
            "point graph": "circle",
            'color graph': 'rect',
            'color chart': 'rect',
            'color map': 'rect',
            '2d relationship': 'rect',
            "points": "circle",  # Can either be point chart or show point or not
            "point": "circle",  # Can either be point chart or show point or not
            "heatmap": "rect",
            "heat map": "rect",
            "area": "area",
            'bar': 'bar',
            # Chart type keywords
            # 'type': 'type',
            # Channel values (added based on column names)
            'count': 'count()',
            # Channel keys
            'x-axis': 'x',
            'y-axis': 'y',
            'x axis': 'x',
            'y axis': 'y',
            'x': 'x',
            'y': 'y',
            'size': 'size',
            'column': 'column',
            'group by': 'column',
            'row': 'row',
            'color': 'color',
            'colour': 'color',
            # Show point/line or not values
            #'with': 'True',
            #'show': 'True',
            'add': 'True',
            'without': 'False',
            'do not': 'False',
            'not': 'False',
            'don\'t': 'False',
            'remove': 'False',
            'natural': 'False',
            'none': 'False',
            # Mark opacity key
            'transparency': 'opacity-reverse',
            'transparent': 'opacity-reverse',
            'translucent': 'opacity-reverse',
            'opacity': 'opacity',
            'opaque': 'opacity',
            # Keywords to increase or reduce the opacity, marker size, height, width, size
            'increase': 'increase',
            'reduce': 'decrease',
            'smaller': 'decrease',
            'bigger': 'increase',
            'enlarge': 'increase',
            'shrink': 'decrease',
            'larger': 'increase',
            'decrease': 'decrease',
            'lighter': 'decrease',
            'darker': 'increase',
            'lower': 'decrease',
            'higher': 'increase',
            'more': 'increase',
            'less': 'decrease',
            'longer': 'increase',
            'shorter': 'decrease',
            'wider': 'increase',
            # Graph Size Keywords
            'height': 'height',
            'width': 'width',
            'interpolation': 'interpolate',
            'step after': 'step-after',
            'step-after': 'step-after',
            # Do not start from zero
            'start from zero': 'scale',
            'scale': 'scale',
            # Show axis or not
            'axis': 'axis',
            # Binned axis
            'binned': 'bin',
            'in bin': 'bin',
            'bins': 'bin',
            'bin': 'bin',
            # Axis transformation
            'median': 'median',
            'max': 'max',
            'maximum': 'max',
            'min': 'min',
            'minimum': 'min',
            'mean': 'mean',
            'average': 'mean',
            'sum': 'sum',
            # Axis align
            'center': 'center',
            'centre': 'center',
            # Set title
            'title': 'title',
            # Set tooltip
            'tooltip': 'tooltip',
            'tool tip': 'tooltip',
        }
        for n in col_names:
            self.keywords[n.lower()] = n
            self.keywords[n.lower() + 's'] = n
            self.keywords[' '.join(n.lower().split('_'))] = n
            self.keywords[' '.join(n.lower().split('_')) + 's'] = n
        for color in colors:
            v = ''.join(color.split())
            self.keywords[color] = v
            self.colors.add(v)
        for k in kvs:
            self.keywords[k] = kvs[k]
    
    
    def __find_num(self, command):
        p = command.find(' ')
        try:
            n = int(command[:p])
            return (n, command[p + 1:])
        except ValueError:
            return (None, command)
    
    
    def __find_next_match(self, command):
        while len(command):
            n, c = self.__find_num(command)
            if n:
                return (n, c)
            for k in self.keywords:
                k_ = k + ' '
                if command.find(k_) == 0:
                    return (self.keywords[k], command[len(k_):])
            command = command[command.find(' ') + 1:]
        return ('', '')
    
    
    def __update(self, match, parsed):
        if match in set(['area', 'bar', 'rect', 'circle', 'square', 'line ', 'point ']):
            parsed['val'] = match.strip()
            parsed['key'] = 'val'
            return True
        elif match == 'type':
            parsed['key'] = 'val'
        return False
            
        
    def __get_result(self, parsed):
        if parsed['channel']:
            return ([parsed['channel'], parsed['key']], parsed['val'])
        else:
            return (parsed['key'], parsed['val'])
    
    
    def __gen(self, matches, hasY=False):
        l = len(matches)
        i = 0
        res = []
        prev = ''
        while i < l:
            match = matches[i]
            i += 1
            if match in set(['area', 'bar', 'rect', 'circle', 'square', 'line ', 'point ']):
                res.append(('val', match.strip()))
                if i < l and matches[i] == 'type':
                    i += 1
            elif match in set(['line', 'point']):
                if i < l and matches[i] == 'type':
                    res.append(('val', match))
                    i += 1
                else:
                    res.append((match, True))
            elif match == 'type':
                if i < l and matches[i] in set(['area', 'bar', 'rect', 'circle', 'square', 'line ', 'point ', 'line', 'point']):
                    res.append(('val', matches[i].strip()))
                    i += 1
            elif match in self.col_names:
                if i < l and matches[i] in set(['x', 'y', 'size', 'column', 'row', 'color']):
                    res.append((matches[i], match))
                    i += 1
                    if prev == 'bin':
                        res.append(([matches[i - 1], 'bin'], True))
                    if i < l and matches[i] == 'bin':
                        res.append(([matches[i - 1], 'bin'], True))
                        i += 1
                elif hasY:
                    res.append(('x', match))
                    if prev == 'bin':
                        res.append((['x', 'bin'], True))
                    if i < l and matches[i] == 'bin':
                        res.append((['x', 'bin'], True))
                        i += 1
                else:
                    hasY = True
                    res.append(('y', match))
                    if prev == 'bin':
                        res.append((['y', 'bin'], True))
                    if i < l and matches[i] == 'bin':
                        res.append((['y', 'bin'], True))
                        i += 1
            elif match in set(['x', 'y', 'size', 'column', 'row', 'color']):
                if i < l and matches[i] == 'bin':
                    # x is binned
                    i += 1
                    res.append(([match, 'bin'], True))
                    if i < l and matches[i] in self.col_names:
                        # x is binned horsepower
                        res.append((match, matches[i]))
                        i += 1
                if i < l and matches[i] in self.col_names:
                    res.append((match, matches[i]))
                    i += 1
                    if i < l and matches[i] == 'bin':
                        # x is horsepower in bins
                        res.append(([match, 'bin'], True))
                        i += 1
                elif match == 'size' and i < l and matches[i] in set(['increase', 'decrease']):
                    # Graph size smaller
                    res.append(('height', matches[i]))
                    res.append(('width', matches[i]))
                    i += 1
                elif match == 'color' and i < l and matches[i] in self.colors:
                    res.append((['mark', 'color'], matches[i]))
                    i += 1
            elif match in set(['True', 'False']):
                if i >= l:
                    continue
                flag = True
                if match == 'False':
                    flag = False
                if matches[i] in set(['line', 'point']):
                    # remove points
                    res.append((matches[i], flag))
                    i += 1
                    continue
                if matches[i] in set(['bin', 'scale', 'axis']):
                    if i + 1 < l and matches[i + 1] in set(['x', 'y', 'size', 'column', 'row', 'color']):
                        # show binned x-axis
                        k = matches[i]
                        channel = matches[i + 1]
                        i += 2
                        res.append(([channel, k], flag))
                elif matches[i] in set(['x', 'y', 'size', 'column', 'row', 'color']):
                    if i + 1 < l and matches[i + 1] in set(['bin', 'scale', 'axis']):
                        # show x-axis in bins
                        k = matches[i + 1]
                        channel = matches[i]
                        i += 2
                        res.append(([channel, k], flag))
            elif match == 'opacity':
                # opacity smaller/bigger
                if i >= l or matches[i] not in set(['increase', 'decrease']):
                    continue
                res.append(('opacity', matches[i]))
                i += 1
            elif match in set(['decrease', 'increase']):
                # increase the size/opacity/height/width
                if i >= l or matches[i] not in set(['size', 'opacity', 'width', 'height']):
                    continue
                if matches[i] == 'size':
                    res.append(('width', match))
                    res.append(('height', match))
                else:
                    res.append((matches[i], match))
                i += 1
            elif match in self.colors:
                # Set red as the color
                # Draw ... with green
                if i < l and matches[i] != 'color':
                    continue
                res.append((['mark', 'color'], match))
                if i < l:
                    i += 1
            elif match == 'interpolate':
                if i >= l or matches[i] not in set(['step-after']):
                    continue
                res.append((match, matches[i]))
                i += 1
            elif match in set(['step-after']):
                if i < l and matches[i] == 'interpolate':
                    i += 1
                res.append(('interpolate', match))
            prev = match
        return res
    
    
    def __check_channel_key(self, matches, i, context):
        if i == len(matches):
            return i, False
        if matches[i] in set(['x', 'y', 'color', 'size', 'column', 'row']):
            if context['channel']:
                return i, True
            context['channel'] = matches[i]
            i += 1
        return i, False
    
    
    def __check_channel_val(self, matches, i, context):
        if i == len(matches):
            return i, False
        if matches[i] in self.col_names or matches[i] == 'count()':
            if context['val']:
                return i, True
            context['val'] = matches[i]
            i += 1
        return i, False
    
    
    def __check_channel_bool(self, checkword, matches, i, context):
        if i == len(matches):
            return i, False
        if matches[i] in set(['True', 'False']):
            if i + 1 == len(matches):
                return i, False
            if matches[i + 1] == checkword:
                if context[checkword]:
                    return i, True
                context[checkword] = matches[i] == 'True'
                return i + 2, False
            return i, False
        if matches[i] == checkword:
            if context[checkword]:
                return i, True
            if i + 1 == len(matches) or matches[i + 1] not in set(['True', 'False']):
                context[checkword] = True
                return i + 1, False
            context[checkword] = matches[i + 1] == 'True'
            return i + 2, False
        return i, False
    
    
    def __check_channel_title(self, matches, i, context):
        if i == len(matches):
            return i, False
        if matches[i] == 'title':
            s = self.cur_command[self.cur_command.find('title') + len('title') + 1:]
            preps = ['to be', 'to', 'as']
            for prep in preps:
                if s.find(prep) == 0:
                    s = s[len(prep) + 1:]
                    break
            context['title'] = s
            i = len(matches)
        return i, False
    
    
    def __check_channel_transform(self, matches, i, context):
        if i == len(matches):
            return i, False
        if matches[i] in set(['median', 'max', 'min', 'mean', 'sum']):
            if context['transform']:
                return i, True
            context['transform'] = matches[i]
            i += 1
        return i, False
    
    
    def __check_channel_align_center(self, matches, i, context):
        if i == len(matches):
            return i, False
        if matches[i] == 'center':
            if context['stack']:
                return i, True
            context['stack'] = 'center'
            i += 1
        return i, False
    
    
    def __decide_channel_type(self, context):
        if context['channel'] == 'y':
            return
        n = context['val']
        if n not in self.col_names:
            return
        stat = self.col_names[n]
        if (stat[0] == 'int64' or stat[0] == np.dtype('<M8[ns]')) and stat[1] <= 15:
            context['type'] = 'O'
    
    
    def __append_channel_info(self, context, res):
        self.__decide_channel_type(context)
        for key in context:
            if key == 'channel':
                continue
            if context[key]:
                res.append(([context['channel'], key], context[key]))
    
    
    def __check_channel(self, matches, parser_context):
        '''Channel property include a 1st level keyword: x, y
        color, size, column, row, among which x and y can be implicit,
        a 2nd level keyword: val (col names or count), bin, title, transformation,
        align (stack: center), and axis, and corresponding value.
        The 2nd level keyword for value for val, transformation, stack can be inferred.
        This check ends once the 1st or 2nd value finds replicates'''
        context = {
            'channel': None,
            'val': None,
            'bin': None,
            'title': None,
            'transform': None,
            'stack': None,
            'axis': None
        }
        i = parser_context['i']
        orig_i = i
        while i < len(matches):
            prev_i = i
            i, duplicate = self.__check_channel_key(matches, i, context)
            if duplicate:
                break
            i, duplicate = self.__check_channel_val(matches, i, context)
            if duplicate:
                break
            i, duplicate = self.__check_channel_bool('bin', matches, i, context)
            if duplicate:
                break
            i, duplicate = self.__check_channel_title(matches, i, context)
            if duplicate:
                break
            i, duplicate = self.__check_channel_transform(matches, i, context)
            if duplicate:
                break
            i, duplicate = self.__check_channel_align_center(matches, i, context)
            if duplicate:
                break
            i, duplicate = self.__check_channel_bool('axis', matches, i, context)
            if duplicate:
                break
            if prev_i == i:
                break
        parser_context['i'] = i
        if not context['channel']:
            if not context['val']:
                parser_context['i'] = orig_i
                return
            if parser_context['isY']:
                context['channel'] = 'y'
                parser_context['isY'] = False
            else:
                context['channel'] = 'x'
        self.__append_channel_info(context, parser_context['res']) 
        
    
    def __check_chart_type(self, matches, context):
        i = context['i']
        if i == len(matches):
            return
        match = matches[i]
        if match in set(['area', 'bar', 'rect', 'circle', 'square', 'line', 'point']):
            i += 1
            context['res'].append(('val', match))
            if match == 'rect':
                context['res'].append((['x', 'type'], 'O'))
                context['res'].append((['y', 'type'], 'O'))
        context['i'] = i

    
    def __check_opacity(self, matches, context):
        i = context['i']
        if i == len(matches):
            return
        match = matches[i]
        if match in ['increase', 'decrease'] and i + 1 < len(matches) and matches[i + 1] in ['opacity', 'opacity-reverse']:
            i += 2
            if matches[i - 1] == 'opacity':
                context['res'].append(('opacity', match))
            else:
                if match == 'increase':
                    context['res'].append(('opacity', 'decrease'))
                else:
                    context['res'].append(('opacity', 'increase'))
        elif match in ['opacity', 'opacity-reverse'] and i + 1 < len(matches) and matches[i + 1] in ['increase', 'decrease']:
            if match == 'opacity':
                context['res'].append(('opacity', matches[i + 1]))
            else:
                if matches[i + 1] == 'increase':
                    context['res'].append(('opacity', 'decrease'))
                else:
                    context['res'].append(('opacity', 'increase'))
            i += 2
        context['i'] = i
        
        
    def __check_color(self, matches, context):
        i = context['i']
        if i == len(matches):
            return
        match = matches[i]
        if match in self.colors:
            i += 1
            if i + 1 < len(matches) and matches[i + 1] == 'color':
                i += 1
            context['res'].append((['mark', 'color'], match))
        elif match == 'color' and i + 1 < len(matches) and matches[i + 1] in self.colors:
            context['res'].append((['mark', 'color'], matches[i + 1]))
            i += 2
        context['i'] = i
                
    
    def __check_tooltip(self, matches, context):
        i = context['i']
        if i == len(matches):
            return
        if matches[i] == 'tooltip':
            i += 1
            items = []
            while i < len(matches) and matches[i] in self.col_names:
                items.append(matches[i])
                i += 1
            context['res'].append(('tooltip', items))
        context['i'] = i
        
    
    def __check_graph_size(self, matches, context):
        i = context['i']
        if i == len(matches):
            return
        match = matches[i]
        if match in ['increase', 'decrease'] and i + 1 < len(matches) and matches[i + 1] in ['size', 'width', 'height']:
            if matches[i + 1] == 'size':
                context['res'].append(('height', match))
                context['res'].append(('width', match))
            else:
                context['res'].append((matches[i + 1], match))
            i += 2
        elif match in ['size', 'width', 'height'] and i + 1 < len(matches) and matches[i + 1] in ['increase', 'decrease']:
            if match == 'size':
                context['res'].append(('height', matches[i + 1]))
                context['res'].append(('width', matches[i + 1]))
            else:
                context['res'].append((match, matches[i + 1]))
            i += 2
        context['i'] = i
        
    
    def __check_graph_title(self, matches, context):
        i = context['i']
        if i == len(matches):
            return
        if matches[i] == 'title':
            s = self.cur_command[self.cur_command.find('title') + len('title') + 1:]
            preps = ['to be', 'to', 'as']
            for prep in preps:
                if s.find(prep) == 0:
                    s = s[len(prep) + 1:]
                    break
            context['res'].append(('title', s))
            i = len(matches)
        context['i'] = i
    
    
    def __gen1(self, matches):
        context = {
            'i': 0,
            'res': [],
            'isY': True
        }
        while context['i'] < len(matches):
            prev_i = context['i']
            self.__check_graph_size(matches, context)
            self.__check_chart_type(matches, context)
            self.__check_opacity(matches, context)
            self.__check_color(matches, context)
            self.__check_channel(matches, context)
            self.__check_tooltip(matches, context)
            self.__check_graph_title(matches, context)
            if prev_i == context['i']:
                context['i'] += 1
        return context['res']
    
    
    def parse(self, command):
        ml_type = mlp.get_type(command)
        command = command.lower()
        self.cur_command = command
        command = ' '.join(re.findall(r"[\w']+", command)) + ' '
        match, command = self.__find_next_match(command)
        matches = []
        while match != '':
            matches.append(match)
            match, command = self.__find_next_match(command)
        print('Matched keywords: ', matches)
        kvs = self.__gen1(matches)
        if ml_type:
            has_type = False
            for kv in kvs:
                if kv[0] == 'val':
                    has_type = True
                    break
            if not has_type:
                kvs.append(('val', ml_type))
        print('Commands: ', kvs)
        return kvs
