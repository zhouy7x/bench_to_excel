#!/usr/bin/python3
import os
import re
import pandas as pd
import argparse
import  time

def file_args(str):
    if os.path.exists(str):
        return str
    else:
        msg = "%s does not  exist !" % str
        raise argparse.ArgumentError(msg)


parser = argparse.ArgumentParser()
parser.add_argument('file', type=file_args, nargs=2, help="add two excel file to contrast")
args = parser.parse_args()
files = args.file


def df1_index(x):
    if x == name:
        return x
    else:
        return str(x)+'_1'


def df2_index(x):
    if x == name:
        return x
    else:
        return str(x)+'_2'


name = str()
df1 = pd.read_excel(files[0])
name = df1.keys()[0]    # 获取第一个列索引值
df1 = df1.rename(columns=df1_index)
df2 = pd.read_excel(files[1])
df2 = df2.rename(columns=df2_index)
df_both_list = []
onside_only_list = []
result_list = []
data1 = df1.iloc[2][name]

score_df1 = df1.loc[0:0, :]
score_df2 = df2.loc[0:0, :]
score_df = pd.merge(score_df1, score_df2, on=name)
df2 = df2.drop(index=0)
df2 = df2.reset_index(drop=True)

# 拼接两个excel
if data1.startswith('_'):  # 有子分
    subcase1_index = []  #获取subcase index
    subcase2_index = []
    for i in range(1, df1.shape[0]):
        if not df1.iloc[i][name].startswith('_'):
            subcase1_index.append(i)

    for i in range(0, df2.shape[0]):
        if not df2.iloc[i][name].startswith('_'):
            subcase2_index.append(i)

    df2_list = []
    for i in range(len(subcase2_index)):
        if i == len(subcase2_index) - 1:
            df2_list.append([df2.iloc[subcase2_index[i]][name], df2.loc[subcase2_index[i]:df2.shape[0]-1]])
        else:
            df2_list.append([df2.iloc[subcase2_index[i]][name], df2.loc[subcase2_index[i]:(subcase2_index[i + 1] - 1)]])

    for i in range(len(subcase1_index)):
        subcase1 = df1.iloc[subcase1_index[i]][name]
        for j in df2_list:
            if subcase1 == j[0]:
                if i == len(subcase1_index) - 1:
                    temp_df1 = df1.loc[subcase1_index[i]:df1.shape[0]]
                else:
                    temp_df1 = df1.loc[subcase1_index[i]:subcase1_index[i+1]-1]
                temp_df = pd.merge(temp_df1, j[1], on=name)
                df_both_list.append(temp_df)
                df2_list.remove(j)
                break
        else:
            if i == len(subcase1_index) - 1:
                onside_only_list.append(df1.loc[subcase1_index[i]:df1.shape[0]])
            else:
                onside_only_list.append(df1.loc[subcase1_index[i]:subcase1_index[i+1]-1])
    if df2_list:
        for item in df2_list:
            onside_only_list.append(item[1])

else:   #无子分
    for i in range(1, df1.shape[0]):
        subcase1 = df1.iloc[i][name]
        for j in range(df2.shape[0]):
            subcase2 = df2.loc[j][name]
            if subcase1 == subcase2:
                temp_df1 = df1.loc[i:i, :]
                temp_df2 = df2.loc[j:j, :]
                temp_df = pd.merge(temp_df1, temp_df2, on=name)
                df_both_list.append(temp_df)
                df2 = df2.drop(index=j)
                df2 = df2.reset_index(drop=True)
                break
        else:
            onside_only_list.append(df1.loc[i:i, :])
    else:
        if not df2.empty:
             onside_only_list.append(df2)

result_list.append(score_df)
result_list.extend(df_both_list)
result_list.extend(onside_only_list)
result_df = pd.concat(result_list, sort=False)
result_df['gain'] = result_df.apply(lambda x: (x.average_2 - x.average_1)/x.average_1, axis=1)

# 排序
score = result_df[0:1]
gain = result_df.shape[1]-1
total_list = []
df_list = []
if result_df.iloc[2][name].startswith('_'):
    index = []
    for i in range(1, result_df.shape[0]):
        if not result_df.iloc[i][name].startswith('_'):
            index.append(i)
    for i in range(len(index)):
        if i == len(index)-1:
            total_list.append([result_df.iat[index[i], gain], result_df[index[i]:result_df.shape[0]]])
        else:
            total_list.append([result_df.iat[index[i], gain], result_df[index[i]:index[i+1]]])
else:
    for i in range(1, result_df.shape[0]):
        total_list.append([result_df.iat[i, gain], result_df[i:i+1]])

sorted_list = sorted(total_list, key=lambda x: x[0], reverse=True)
subcase_list = list(map(lambda x: x[1], sorted_list))
df_list.append(score)
df_list.extend(subcase_list)
result_df = pd.concat(df_list)

sheet_name = '{}'.format(time.strftime("%Y-%m-%d", time.localtime()))
writer = pd.ExcelWriter("sort-{}.xls".format(time.strftime("%Y%m%d-%H%M%S", time.localtime())))
result_df.to_excel(writer, sheet_name=sheet_name, index=False)
writer.save()
