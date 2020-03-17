#!/usr/bin/python3
import os
import re
from sys import argv
import pandas as pd
from pandas import DataFrame
import time
import argparse


def dir_args(string):
    if not os.path.isdir(string):
        msg = "%s is not a directory path!" % string
        raise argparse.ArgumentTypeError(msg)
    return string


parser = argparse.ArgumentParser()
# parser.usage = help_msg
parser.add_argument('dir', type=dir_args, nargs=2, help='add jsc and dir')

args = parser.parse_args()
dir_list = args.dir
mode = 'all'


def extract_data(file):
    name_ls = []
    score_ls = []
    with open(file) as f:
        content = f.read()

    if file.endswith('txt'):
        cont_ls = re.findall(r'Running (.*?):(.*?)Score: *([0-9]*\.?[0-9]+)', content, re.S)
        total_score = re.findall(r"Total Score: *([0-9]*\.?[0-9]+)", content)

        name_ls.append('Score')
        score_ls.append(float(total_score[0]))

        if mode == 'simple':
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

        if mode == 'simple':
            for i in cont_ls:
                name_ls.append(i[2])
                score_ls.append(float(i[5]))
        else:
            for i in cont_ls:
                name_ls.append(i[2])
                score_ls.append(float(i[5]))
                date = re.findall(
                    r'<span id="(.*?)">([0-9]*\.?[0-9]+)</span><label>(\w*?)</label></span>',
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
                r'<span id="(.*?)">([0-9]*\.?[0-9]+)</span><label>(.*?)</label></span>', i[6],
                re.S)
            for j in date:
                name_case = '____' + j[2]
                name_ls.append(name_case)
                score_ls.append(float(j[1]))

    return name_ls, score_ls


def to_excel(src, file_list, df, mean1):
    i = 0
    files_num = len(file_list)
    for file in file_list:
        i += 1
        name_ls, score_ls = extract_data(src + file)
        if "subcases" not in df:
            df['subcases'] = name_ls
        df[file] = score_ls

    if df.shape[1] == files_num + 1:
        stdev = df.std(axis=1)
        mean = df.mean(axis=1)
        stdev_mean = stdev/mean
        df['stdev1'] = stdev
        df['average1'] = mean
        df['stdev/average_1'] = stdev_mean.apply(lambda x: float(x))
        return df, mean

    else:
        file2_start = df.shape[1] - files_num
        stdev= df.iloc[:, range(file2_start, file2_start + files_num)].std(axis=1)
        mean2 = df.iloc[:, range(file2_start, file2_start + files_num)].mean(axis=1)
        stdev_mean = stdev / mean2
        df['stdev2'] = stdev
        df['average2'] = mean2
        df['stdev/average_2'] = stdev_mean.apply(lambda x: float(x))
        gain = (mean2-mean1)/mean1
        df['gain'] = gain.apply(lambda x: float(x))

    return df, None


def main(dir_list):
    df = DataFrame()
    mean1 = DataFrame()
    for item in dir_list:
        file_list = os.popen('ls ' + item).read().split()
        if item.endswith('/'):
            result, mean = to_excel(item, file_list, df, mean1)
        else:
            result, mean = to_excel(item+'/', file_list, df, mean1)

        if type(mean) == pd.Series:
            mean1 = mean

    score = df.loc[0:0]
    df_column = df.shape[1] - 1  # index start with 1

    subcase_index = []
    for i in range(1, df.shape[0]):
        if not df.iloc[i]['subcases'].startswith('_'):
            subcase_index.append(i)

    total_list = []
    for i in range(len(subcase_index)):
        if i == len(subcase_index)-1:
            total_list.append([df.iat[subcase_index[i], df_column], df.loc[subcase_index[i]:subcase_index[i]+3]])
        else:
            total_list.append([df.iat[subcase_index[i], df_column], df.loc[subcase_index[i]:(subcase_index[i+1]-1)]])

    sorted_list = sorted(total_list, key=lambda x: x[0], reverse=True)

    df_list = []
    subcase_list = list(map(lambda x: x[1], sorted_list))
    df_list.append(score)
    df_list.extend(subcase_list)

    result_df = pd.concat(df_list)
    sheet_name = '{}'.format(time.strftime("%Y-%m-%d", time.localtime()))
    writer = pd.ExcelWriter("jetstream2-cli-pk-{}.xls".format(time.strftime("%Y%m%d-%H%M%S", time.localtime())))
    result_df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


if __name__ == '__main__':
    main(dir_list)
