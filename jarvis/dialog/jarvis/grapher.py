from .graph_components.aixs import Axis
from .graph_components.mark import Mark
import altair as alt


class Grapher:
    def __init__(self, df):
        self.mark = Mark(0.9)
        self.chart = self.mark.get(alt.Chart(df))
        self.encode = {}
        self.tooltip = []
        self.properties = {}
        self.width = 400
        self.height = 300


    def __update_mark(self, ks, v):
        if len(ks) != 0:
            self.chart = self.mark.update(ks[0], v).get(self.chart)


    def __update_encode(self, ks, v):
        if len(ks) == 0:
            return
        if ks[0] in set(['x', 'y', 'color', 'size', 'column', 'row', 'x2', 'y2']):
            self.__update_axis(ks, v)
        elif ks[0] == 'tooltip':
            self.__update_tooltip(v)


    def __update_axis(self, ks, v):
        channel = ks[0]
        if channel not in self.encode:
            self.encode[channel] = Axis(channel)
        key = 'val'
        if len(ks) > 1:
            key = ks[1]
        channel = self.encode[channel].update(key, v).get()
        if channel:
            self.chart = self.chart.encode(channel)


    def __update_tooltip(self, v):
        if len(v) == 0:
            raise Exception('Sorry, but once the tooltip is set, it cannot be empty again...')
        self.tooltip = v
        self.chart = self.chart.encode(tooltip=v)


    def __update_properties(self, ks, v):
        if len(ks) == 0:
            return

        if v in set(['increase', 'decrease']):
            factor = 1.2
            if v == 'decrease':
                factor = 0.8
            if ks[0] == 'width':
                self.width = self.width * factor
                v = self.width
            elif ks[0] == 'height':
                self.height = self.height * factor
                v = self.height
        
        self.properties[ks[0]] = v
        self.chart = self.chart.properties(**self.properties)


    def __expand_keys(self, ks, v):
        if type(ks) == str:
            ks = [ks]

        if len(ks):
            if ks[0] == 'size':
                if type(v) == str:
                    return ['encode'] + ks
                return ['mark'] + ks
            if ks[0] in set(['val', 'opacity', 'interpolate', 'line', 'point']):
                return ['mark'] + ks
            if ks[0] in set(['x', 'y', 'color', 'size', 'column', 'row', 'tooltip', 'x2', 'y2']):
                return ['encode'] + ks
            if ks[0] in set(['height', 'width', 'title']):
                return ['properties'] + ks
        return ks


    def update(self, ks, v):
        ks = self.__expand_keys(ks, v)
        if len(ks) == 0:
            return self
        if ks[0] == 'mark':
            self.__update_mark(ks[1:], v)
        elif ks[0] == 'encode':
            self.__update_encode(ks[1:], v)
        elif ks[0] == 'properties':
            self.__update_properties(ks[1:], v)
        return self


    def get(self):
        return self.chart

    
    # def from_list(self, kvs):
    #     for (ks, v) in kvs:
    #         self.update(ks, v)
    #     return self