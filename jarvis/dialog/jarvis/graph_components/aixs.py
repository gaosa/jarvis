import altair as alt


class Axis:
    '''
    val = None
    type = None
    bin = None
    title = None
    transform = None
    stack = None
    axis = None
    scale = None
    # Not supported
    sort = None
    '''
    def __init__(self, channel):
        self.params = {'config': {}}
        self.channel = channel
    def __val(self):
        if 'val' not in self.params:
            return None
        val = self.params['val']
        if 'transform' in self.params:
            val = self.params['transform'] + '(' + val + ')'
        if 'type' in self.params:
            val += ':' + self.params['type']
        return val
    def get(self):
        val = self.__val()
        if not val:
            return None
        channel = self.channel
        if channel == 'x':
            return alt.X(val, **self.params['config'])
        elif channel == 'y':
            return alt.Y(val, **self.params['config'])
        elif channel == 'color':
            return alt.Color(val, **self.params['config'])
        elif channel == 'size':
            return alt.Size(val, **self.params['config'])
        elif channel == 'column':
            return alt.Column(val, **self.params['config'])
        elif channel == 'row':
            return alt.Row(val, **self.params['config'])
        elif channel == 'x2':
            return alt.X2(val, **self.params['config'])
        elif channel == 'y2':
            return alt.Y2(val, **self.params['config'])
        return None
    def update(self, k, v):
        if k in set(['val', 'type', 'transform']):
            # if k == 'val':
            #     if 'type' in self.params:
            #         del self.params['type']
            #     if 'transform' in self.params:
            #         del self.params['transform']
            self.params[k] = v
        elif k in set(['bin', 'title', 'stack', 'axis']):
            self.params['config'][k] = v
        elif k == 'scale':
            self.params['config']['scale'] = alt.Scale(zero=v)
        
        return self