#!/usr/bin/python3
import os
import re
import pandas as pd
from pandas import DataFrame

import utils
import argparse

parser = argparse.ArgumentParser()
# parser.usage = help_msg
parser.add_argument('-m', '--mode', type=str, choices=['simple', 'all'], default="simple",
                    help="return only scores or all outputs of subcases")
args = parser.parse_args()
mode = args.mode

class Base(object):
    def __init__(self, name, folder, writer, mode="simple"):
        self.name = name
        self.folder = folder
        self.writer = writer
        self.df = DataFrame()
        self.mode = mode


class JetStream2(Base):
    def __init__(self, writer):
        Base.__init__(self, 'jetstream2', 'jetstream2', writer, mode)

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

        stdev = self.df.std(axis=1)
        mean = self.df.mean(axis=1)
        stdev_mean = stdev / mean
        self.df['stdev'] = stdev
        self.df['average'] = mean
        self.df['stdev/average'] = stdev_mean.apply(lambda x: float(x))
        self.df.to_excel(self.writer, index=False, sheet_name=self.name)

    def _run(self, file):
        name_ls = []
        score_ls = []
        with open(file) as f:
            content = f.read()

        if file.endswith('mhtml'):
            cont = content.replace("=\n", "")
            score = re.search(r'<div class=3D"score">(\d+\.\d+)</div>', cont).group(1)
            name_ls.append('Score')
            score_ls.append(float(score))
            cont_ls = re.findall(r'<h3[\d\D]*?><[\d\D]*?>(.*?)</a></h3>[\d\D]*?<h4[\d\D]*?>(.*?)</h4>', cont, re.S)
            for i in cont_ls:
                name_ls.append(i[0])
                score_ls.append(float(i[1]))
        elif file.endswith('txt'):
            cont_ls = re.findall(r'Running (.*?):(.*?)Score: *([0-9]*\.?[0-9]+)', content, re.S)
            total_score = re.findall(r"Total Score: *([0-9]*\.?[0-9]+)", content)

            name_ls.append('Score')
            score_ls.append(float(total_score[0]))

            if self.mode == 'simple':
                for i in cont_ls:
                    name_ls.append(i[0])
                    score_ls.append(float(i[2]))
            else:
                name_ls, score_ls = [], []
                for i in cont_ls:
                    name_ls.append(i[0])
                    score_ls.append(float(i[2]))
                    others = i[1].replace("\n", "")
                    others = re.findall(r" *(.*?): *([0-9]*\.?[0-9]+)", others, re.S)
                    for j in others:
                        name_ls.append("____" + j[0])
                        score_ls.append(float(j[1]))

        elif file.endswith('htm') or file.endswith('html'):
            cont_ls = re.findall(r'<div class="benchmark benchmark-done"(.*?)<h3 class="benchmark-name">(.*?)">(.*?)'
                                 r'</a></h3>(.*?)<h4 class="score"(.*?)">([0-9]*\.?[0-9]+)</h4><p><span class="result"'
                                 r'>(.*?)</div>', content, re.S)

            name_ls.append('total_socre')

            cont_total = re.search(r'<div id="result-summary" class="done"><div class="score">([0-9]*\.?[0-9]+)</div>'
                                   r'<label>Score</label></div>', content, re.S).group(1)
            score_ls.append(float(cont_total))

            if self.mode == 'simple':
                for i in cont_ls:
                    name_ls.append(i[2])
                    score_ls.append(float(i[5]))
            else:
                for i in cont_ls:

                    name_ls.append(i[2])
                    score_ls.append(float(i[5]))
                    date = re.findall(
                        r'<span class="result"><span id="(.*?)">([0-9]*\.?[0-9]+)</span><label>(.*?)</label></span>',
                        i[6], re.S)

                    for j in date:
                        name_case = '____' + j[2]
                        name_ls.append(name_case)
                        score_ls.append(float(j[1]))

        elif file.endswith('webarchive'):
            name_ls.append('total_socre')
            cont_total = re.search(r'<div id="result-summary" class="done"><div class="score">([0-9]*\.?[0-9]+)</div>'
                                   r'<label>Score</label></div>', content, re.S).group(1)
            score_ls.append(float(cont_total))
            cont_ls = re.findall(r'<div class="benchmark benchmark-done"(.*?)<h3 class="benchmark-name">(.*?)">(.*?)'
                                 r'</a></h3>(.*?)<h4 class="score"(.*?)">([0-9]*\.?[0-9]+)</h4><p>(.*?)</p></div>',
                                 content, re.S)
            for i in cont_ls:
                name_ls.append(i[2])
                score_ls.append(float(i[5]))
                date = re.findall(
                    r'<span class="result"><span id="(.*?)">([0-9]*\.?[0-9]+)</span><label>(.*?)</label></span>', i[6],
                    re.S)
                for j in date:
                    name_case = '____' + j[2]
                    name_ls.append(name_case)
                    score_ls.append(float(j[1]))

        return name_ls, score_ls


class Speedometer2(Base):

    def __init__(self, writer):
        Base.__init__(self, "speedometer2", "speedometer2", writer)

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
        if file.endswith('mhtml'):
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
        elif file.endswith('html'):
            a = re.findall(r'<table class="results-table">(.*?)</table>', content)
            b = a[1]
            b = b.replace("<tr><th>Subcase</th><td>Score (runs/min)</td><td>Time (ms)</td></tr>", '')
            cont_ls = re.findall(r'<tr><th>(.*?)</th><td>([0-9]*\.?[0-9]+)</td><td>([0-9]*\.?[0-9]+)</td></tr>', b)

            name_ls.append('total_socre')

            cont_total = re.search(r'<div id="result-number">([0-9]*\.?[0-9]+)</div>', content, re.S).group(1)
            score_ls.append(float(cont_total))

            for i in cont_ls:
                name_ls.append(i[0])
                score_ls.append(float(i[1]))

        return name_ls, score_ls


class Ares(Base):
    def __init__(self, writer):
        Base.__init__(self, "ares", "ares", writer)

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
        title_ls = ['air', 'basic','babylon','ML']
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

        return name_ls, score_ls

class Webtooling(Base):
    def __init__(self, writer):
        Base.__init__(self, "webtooling", "webtooling", writer)

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
    choice = input('1.Jetstream2    2.Speedometer2    3.Ares    4.Webtooling\n' +
                   'Please input number or numbers split by ",":    ')
    if choice:
        choice_list = choice.split(',')
        for i in choice_list:
            if int(i) not in [1, 2, 3, 4]:
                print("The number is wrong, please run again!")
                break
        else:
            with utils.touch_excel(file_name) as writer:
                benchs = list()
                for i in choice_list:
                    if int(i) == 1:
                        benchs.append(JetStream2(writer))
                    elif int(i) == 2:
                        benchs.append(Speedometer2(writer))
                    elif int(i) == 3:
                        benchs.append(Ares(writer))
                    elif int(i) == 4:
                        benchs.append(Webtooling(writer))

                for bench in benchs:
                    bench.run()
    else:
        print('The number is none, please run again!')
