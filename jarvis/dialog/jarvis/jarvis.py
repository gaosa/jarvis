from .grapher import Grapher
from .parser import Parser


class Jarvis:
    def __init__(self, df):
        self.grapher = Grapher(df)
        self.parser = Parser(self.__df_statistics(df))


    def __df_statistics(self, df):
        dic = {}
        d = dict(df.nunique())
        for k in d:
            dic[k] = (df[k].dtype, d[k])
        return dic


    def handle_next(self, command):
        ls = self.parser.parse(command)
        if not len(ls):
            return False, ['Sorry, but I cannot understand you...']
        success = False
        err_msgs = []
        for p in ls:
            try:
                self.grapher.update(p[0], p[1])
                success = True
            except Exception as e:
                err_msgs.append(str(e))
        return success, err_msgs


    def get(self):
        return self.grapher.get()
