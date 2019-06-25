#!/usr/bin/python3
import os
import re
from pandas import DataFrame

import utils


class Base(object):
    pass


class JetStream2(Base):
    def __init__(self, writer):
        super(JetStream2, self).__init__()
        self.name = "jetstream2"
        self.folder = "jetstream2"
        self.writer = writer
        self.df = DataFrame()

    def run(self):
        src_ls = os.popen("ls %s" % self.folder).readlines()
        src_ls = list(map(lambda x: x.replace('\n', ''), src_ls))
        # print(src_ls)

        i = 0
        for src in src_ls:
            i += 1
            file = self.folder + "/" + src
            print(file)
            names, scores = self._run(file)
            if 'name' not in self.df:
                self.df['name'] = names
            self.df[i] = scores

        self.df.to_excel(self.writer, index=False, sheet_name=self.name)

    def _run(self, file):
        name_ls = []
        score_ls = []
        with open(file) as f:
            content = f.read()
        cont = content.replace("=\n", "")
        score = re.search(r'<div class=3D"score">(\d+\.\d+)</div>', cont).group(1)
        name_ls.append('Score')
        score_ls.append(float(score))
        cont_ls = re.findall(r'<h3[\d\D]*?><[\d\D]*?>(.*?)</a></h3>[\d\D]*?<h4[\d\D]*?>(.*?)</h4>', cont, re.S)
        for i in cont_ls:
            name_ls.append(i[0])
            score_ls.append(float(i[1]))
        return name_ls, score_ls


if __name__ == '__main__':
    file_name = "scores.xls"
    with utils.touch_excel(file_name) as writer:
        benchs = list()
        benchs.append(JetStream2(writer))

        for bench in benchs:
            bench.run()
