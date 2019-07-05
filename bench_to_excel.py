#!/usr/bin/python3
import os
import re
# import pandas
from pandas import DataFrame

import utils

# pandas.

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


class Speedometer2(Base):
    def __init__(self, writer):
        super(Speedometer2, self).__init__()
        self.name = "speedometer2"
        self.folder = "speedometer2"
        self.writer = writer
        self.df = DataFrame()

    def run(self):
        src_ls = os.popen("ls %s" % self.folder).readlines()
        src_ls = list(map(lambda x: x.replace('\n', ''), src_ls))

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
        score = re.search(r'<span id=3D"geomean-score">(\d+\.\d+)</span>', cont).group(1)
        name_ls.append('Score')
        score_ls.append(float(score))
        a = re.findall(r'<table class=3D"results-table">[\d\D]*?</table>', content)
        for i in a:
            if "Subcase" in i:
                i = i.replace("=\n", "")
                g = re.findall(r'<th>(.*?)</th>[\d\D]*?<td>(.*?)</td>[\d\D]*?<td>.*?</td>', i)
                item_list = g[1:]
                for item in item_list:
                    name_ls.append(item[0])
                    score_ls.append(float(item[1]))
        return name_ls, score_ls


class Ares(Base):
    def __init__(self, writer):
        super(Ares, self).__init__()
        self.name = "ares"
        self.folder = "ares"
        self.writer = writer
        self.df = DataFrame()

    def run(self):
        src_ls = os.popen("ls %s" % self.folder).readlines()
        src_ls = list(map(lambda x: x.replace('\n', ''), src_ls))

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
        cont = content.replace("=\n", "").replace("=\\n","").replace("=B1","")
        # 总分
        score= re.search(r'<span id=3D"Geomean"><span class=3D"value">([\d\D]*?)</span>', cont).group(1)
        name_ls.append('Score')
        score_ls.append(float(score))
        title_ls = ['air','basic','babylon','ML']
        for i in range(len(title_ls)):
            if i!=len(title_ls)-1:
                sub_ls = re.findall(r'<div class=3D"{} test">[\d\D]*?<div class=3D"{} test">'.format(title_ls[i],title_ls[i+1]), cont)
            # 最后一个子分
            else:
                sub_ls = re.findall(r'<div class=3D"{} test">[\d\D]*?</main>'.format(title_ls[i]), cont)

            sub_cont = re.findall(r'<div class=3D"score">[\d\D]*?</div>', str(sub_ls))

            for m in sub_cont:
                # 获取子项名称
                a = re.search(r'(.*)<label>(.*?)</label>(.*)', m)
                title = title_ls[i] + '-' + str(re.sub(' ', '', str(a.group(2)).lower()))
                name_ls.append(title)
                # 获取子分
                soc = re.search(r'(.*)<span class=3D"value">(.*?)</span>', m)
                score_ls.append(float(soc.group(2)))

        return name_ls,score_ls

class Webtooling(Base):
    def __init__(self, writer):
        super(Webtooling, self).__init__()
        self.name = "webtooling"
        self.folder = "webtooling"
        self.writer = writer
        self.df = DataFrame()

    def run(self):
        src_ls = os.popen("ls %s" % self.folder).readlines()
        src_ls = list(map(lambda x: x.replace('\n', ''), src_ls))

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

    def _run(self,file):
        name_ls = []
        score_ls = []
        with open(file) as f:
            content = f.read()

        content = content.replace("=\n", "").replace("=B1","").replace("=\\n","")
        b = re.findall(r'<span class=3D"score">(.*?)</span>', content)
        name_ls.append('Score')
        if b:
            score_ls.append(float(b[0]))
        else:
            score_ls.append(' ')
        a = re.findall(r'<td class=3D"result" id=3D"results-cell-(.*?)">(.*?)</td>', content)
        for i in a:
            name_ls.append(str(i[0]))
            score_ls.append(float(i[1]))
        return name_ls, score_ls


if __name__ == '__main__':
    file_name = "scores.xls"
    with utils.touch_excel(file_name) as writer:
        benchs = list()
        benchs.append(JetStream2(writer))
        # benchs.append(Speedometer2(writer))
        # benchs.append(Ares(writer))
        # benchs.append(Webtooling(writer))

        for bench in benchs:
            bench.run()
