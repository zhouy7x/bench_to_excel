import os
from sys import argv
from pandas import DataFrame

import jetstream2_d8_pk_2excel
import utils


def run(folder, name, df, writer):
    src_ls = os.listdir(folder)
    src_ls.sort()

    for src in src_ls:
        column = src.replace('.txt', '')
        file = folder + "/" + src
        print(file)
        names, scores = jetstream2_d8_pk_2excel.extract_data(file)
        if 'name' not in df:
            df['name'] = names
        df[column] = scores

    df.to_excel(writer, index=False, sheet_name=name)


if __name__ == '__main__':
    # src = argv[1]
    src = 'xuhao'
    name = 'jetstream2-d8'
    file_name = name+".xls"
    df = DataFrame()
    with utils.touch_excel(file_name) as writer:
        run(folder=src, name=name, df=df, writer=writer)
