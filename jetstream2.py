#!/usr/bin/python3
import re
from sys import argv
import pandas as pd
from pandas import DataFrame

BENCHMARK = "jetstream2"
RUNS = int(argv[1]) if argv[1:] else 5


def fun1(file):
    name_ls = []
    score_ls = []
    with open(file) as f:
        pass
        content = f.read()

    cont = content.replace("=\n", "")

    cont_ls = re.findall(r'<h3[\d\D]*?><[\d\D]*?>(.*?)</a></h3>[\d\D]*?<h4[\d\D]*?>(.*?)</h4>', cont, re.S)
    # print(len(cont_ls))

    for i in cont_ls:
        name_ls.append(i[0])
        score_ls.append(i[1])

    return name_ls, score_ls


def main(runs):
    name_ls = []
    score_ls = []
    file_end = ".mhtml"
    for i in range(runs):
        file = BENCHMARK + '/' + str(i+1) + file_end
        if file:
            a = fun1(file)
            # print(a)
            name_ls.append(a[0])
            score_ls.append(a[1])
            name = name_ls[0]
    name_ls = name_ls[0]

    writer = pd.ExcelWriter("%s.xls" % BENCHMARK)

    # df = DataFrame({"name": name_ls})
    df = DataFrame()
    if 'name' not in df:
        # print('name')
        df['name'] = name_ls

    for i in range(runs):
        df[i+1] = score_ls[i]
    # print(df)

    df.to_excel(writer, index=False, sheet_name=BENCHMARK)
    writer.save()


if __name__ == "__main__":
    main(RUNS)
