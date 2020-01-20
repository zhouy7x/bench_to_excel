#!/usr/bin/python3
import os
import re
import pandas as pd
from pandas import DataFrame

import utils
import argparse

# unity3d
import pytesseract
from PIL import Image
import sys
import difflib

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

        if file.endswith('txt'):
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

        elif file.endswith('mhtml') or file.endswith('htm') or file.endswith('html'):
            content = content.replace("=\n", "").replace("=3D", "=")

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
                    data = re.findall(
                        r'<span id="(.*?)">([0-9]*\.?[0-9]+)</span><label>(.*?)</label></span>',
                        i[6], re.S)

                    for j in data:
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
                data = re.findall(
                    r'<span id="(.*?)">([0-9]*\.?[0-9]+)</span><label>(.*?)</label></span>', i[6],
                    re.S)
                for j in data:
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


class Unity3D(Base):
    def __init__(self, writer):
        Base.__init__(self, "unity3d", "unity3d", writer)

    def run(self):
        self.case_warehouse = ['Mandelbrot Script','Instantiate & Destroy','CryptoHash Script','Animation & Skinning','Asteroid Field','Particles','Physics Meshes','Physics Cubes','Physics Spheres','2D Physics Spheres','2D Physics Boxes','AI Agents']
        src_ls = os.popen("ls %s" % self.folder).readlines()
        src_ls = list(map(lambda x: x.replace('\n', ''), src_ls))
        i = 0
        for src in src_ls:
            i += 1
            file = self.folder + "/" + src
            # print(file)
            names, scores = self._run(file)
            if names == 5 or scores == 5:
                continue
            if 'name' not in self.df:
                self.df['name'] = names
            self.df[i] = scores

        self.df.to_excel(self.writer, index=False, sheet_name=self.name)

    def _run(self, file):
        name_ls = []
        score_ls = []
        # print(file)
        picture = file
        if picture:
            print(picture)
            image = Image.open(picture)
            text = pytesseract.image_to_string(image,lang="test")
            text_total = pytesseract.image_to_string(image,lang="test",config='-psm 1 number')
            result = self._Handle(text,text_total)
            if result not in [1,2,3,4]:
                name_ls = result[0]
                score_ls = result[1]
            else:
                return 5,5
        return name_ls, score_ls


    def _Handle(self,text,text_total):
        # print(text)
        name_ls_ex = []
        score_ls_ex = []
        name_ls_ex_finally =[]

        # Total score
        total_score = re.findall(r'(\d*)$', text_total, re.S)
        # print(total_score)
        try:
            total_score = total_score[0]
            int(total_score)

        except:
            print("Total score error")
            return 1

        if int(total_score) < 10000:
            print("The total score is too low and there may be anomalies")
            return 2


        text_ls = re.findall(r'(.*?)\n', text, re.S)
        score_ls = []
        message_useless = ["select","benchmarks","run","all","overall","score"]
        # print(text_ls)
        sigle_mode = 0
        # print(text_ls)
        for case in text_ls:

            sigle_useless = 0
            for useless in message_useless:
                if useless  in case.lower() or not case:
                    sigle_useless = 1

            if sigle_useless == 0:
                score_ls.append(case)

            try:
                int(case)
                sigle_mode = 1
            except:
                pass

        # print(sigle_mode)


        # print(score_ls)
        if sigle_mode == 0:
            for case in score_ls:
                num = re.findall(r"(.*?)(\d+\.?\d*)$", case,re.S)
                name_ls_ex.append(num[0][0])
                score_ls_ex.append(num[0][1])


        if sigle_mode == 1:
            for case in score_ls:
                try:
                    int(case)
                    score_ls_ex.append(case)
                except:
                    name_ls_ex.append(case)

        # print(name_ls_ex,score_ls_ex)
        if len(name_ls_ex) != len(score_ls_ex) or len(name_ls_ex) != len(self.case_warehouse):
            print("Case name does not match the number of points!")
            return 3

        i = 0
        for name in name_ls_ex:
            Similarity = self._string_similar(name.lower(),self.case_warehouse[i].lower())
            if Similarity < 0.6:
                print("%s：The similarity is too low, pause the extraction, please train the language library or manually extract"%(self.case_warehouse[i]))
                return 4
            else:
                name_ls_ex_finally.append(self.case_warehouse[i])
                i = i+1

        name_ls_ex_finally.insert(0,"overall")
        score_ls_ex.insert(0,total_score)

        return name_ls_ex_finally,score_ls_ex


    def _string_similar(self,s1, s2):
        return difflib.SequenceMatcher(lambda x: x==" ", s1, s2).quick_ratio()



if __name__ == '__main__':
    file_name = "scores.xls"
    choice = input('1.Jetstream2    2.Speedometer2    3.Ares    4.Webtooling    5.Unity3D\n' +
                   'Please input number or numbers split by ",":    ')
    if choice:
        choice_list = choice.split(',')
        for i in choice_list:
            if int(i) not in [1, 2, 3, 4, 5]:
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

                    elif int(i) == 5:
                        benchs.append(Unity3D(writer))


                for bench in benchs:
                    bench.run()
    else:
        print('The number is none, please run again!')
