class Mark:
    def __init__(self, opacity):
        self.params = {'config': { 'opacity': opacity }, 'val': 'circle'}
        self.opacity = opacity
    def update(self, k, v):
        if k == 'val':
            self.params['val'] = v
        elif k == 'opacity':
            if v in set(['increase', 'decrease']):
                factor = 0.2
                if v == 'decrease':
                    factor = -0.2
                self.opacity = self.opacity + factor
                self.opacity = max(0.0, min(1.0, self.opacity))
                v = self.opacity
            else:
                self.opacity = v
            self.params['config'][k] = v
        elif k in set(['opacity', 'color', 'interpolate', 'line', 'point', 'size']):
            self.params['config'][k] = v
        return self
    def get(self, graph):
        val = self.params['val']
        if val == 'area':
            return graph.mark_area(**self.params['config'])
        elif val == 'bar':
            return graph.mark_bar(**self.params['config'])
        elif val == 'circle':
            return graph.mark_circle(**self.params['config'])
        elif val == 'line':
            return graph.mark_line(**self.params['config'])
        elif val == 'point':
            return graph.mark_point(**self.params['config'])
        elif val == 'rect':
            return graph.mark_rect(**self.params['config'])
        elif val == 'square':
            return graph.mark_square(**self.params['config'])
        else:
            return graph