import json

import pandas as pd


if __name__ == '__main__':
    file = 'weekly-trunk-track-2019-ww23.xlsx'
    xlsx = pd.ExcelFile(file)   # 生成pandas专用excel到内存中（可以同一文件多次读取，提高性能）

    # guide = pd.read_excel(xlsx, sheet_name='Sheet1', header=0)
    # print(guide.head(3))  # 取头三行
    # print(guide.tail(3))  # 取尾三行
    # print(guide.loc[3:6])   # 取指定几行（切片，3到6行）

    # print(guide['configurations'].isin(['subcase']))
    # subcase_index = guide['configurations'].isin(['subcase'])
    # print(subcase_index)
    # print(type(subcase_index))

    reader = pd.read_excel(xlsx, sheet_name='Sheet1', header=47, index_col=0, usecols=[0, 1])
    # print(reader)
    data_json = reader.to_json()

    data = json.loads(data_json)
    # key = reader.
    # print(key)
    print(data_json)
    print(data)
    # print(type(data['glk_01']))
    # print(type(reader.to_json()))
    # sheet = reader['Sheet1']
    # data = sheet[46:63]['subcase']
    # print(data)
    # print(reader)
    # print(reader[])
    # json.dumps()