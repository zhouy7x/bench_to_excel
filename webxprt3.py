#!/usr/bin/python3
import os
import re

import xlwt
from sys import argv


style = xlwt.XFStyle()   #总分样式
style2 = xlwt.XFStyle()  #子分名称样式
style3 = xlwt.XFStyle()  #子分样式

borders = xlwt.Borders()
borders.left= 1
borders.right= 1
borders.top= 1
borders.bottom= 1

font = xlwt.Font()
font.name = 'Calibri'
font.height = 20*11

font2 = xlwt.Font()
font2.name = 'Arial'
font2.height = 20*10

alignment = xlwt.Alignment()
alignment.horz = 0x02

alignment2 = xlwt.Alignment()
alignment2.horz = 0x01


style.borders = borders
style.font = font
style.alignment = alignment

style2.borders = borders
style2.font = font2
style2.alignment = alignment2


style3.borders = borders
style3.font = font2
style3.alignment = alignment


def getList(folder):
    txt_list = []
    a = os.listdir(folder)
    for name in a:
        if 'txt' in name:
            txt_list.append(name)
    txt_list.sort()

    return txt_list


def transform(folder, file):
    file_path = os.path.join(folder,file)
    name_ls = []
    score_ls = []
    Variance_ls = []
    with open(file_path) as f:
        content_0 = f.read()

    content_1 = re.findall(r'Variance(.*?)Capability', content_0, re.S)
    content_2 = re.findall(r'(.*?)\n', content_1[0], re.S)

    for i in content_2:
        if not i:
            continue
        content_3 = re.findall(r'^(.*?),(.*?),(.*?)$', i, re.S)
        res_ls = content_3[0]
        name_ls.append(res_ls[0])
        score_ls.append(float(res_ls[1]))
        if 'Overall' in res_ls[0]:
            Variance_ls.append('')
        else:
            Variance_ls.append(res_ls[2])

    return name_ls, score_ls,Variance_ls


def collect(folder, output_dir='.'):
    score_ls = []
    name_ls = []
    Variance_ls = []

    file_list = getList(folder)

    for file in file_list:
        if file:
            a = transform(folder, file)
            score_ls.append(a[1])
            name_ls.append(a[0])
            Variance_ls.append(a[2])

    if name_ls and score_ls and Variance_ls:
        name_ls = name_ls[0]

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')

    start = 1
    num_1 = 0
    for score_num in score_ls:
        i_a = 0
        num_2 = 0
        Variance_ls_case = Variance_ls[num_1]
        for score in score_num:
            worksheet.write(2+i_a,start,score,style3)
            worksheet.write(2+i_a,start+1,Variance_ls_case[num_2],style3)
            i_a = i_a + 1
            num_2 = num_2 +1
        worksheet.write(1,start,'Test Item',style)
        worksheet.write(1,start+1,'Variance',style)
        name = file_list[num_1].split('.')[0]
        worksheet.write_merge(0,0,start,start+1,name,style)
        num_1 = num_1 + 1
        start = start+2

    worksheet.write_merge(0,1,0,0,"name",style)

    i = 0
    for case in name_ls:
        worksheet.write(2+i,0,case,style2)
        i = i+1

    xls_name = folder.replace('/', '-') + '.xls'
    print(xls_name)
    workbook.save(os.path.join(output_dir, xls_name))


if __name__ == '__main__':
    output_dir = '.'
    if output_dir != '.' and output_dir != '..':
        if os.path.exists(output_dir):
            os.system('rm -rf '+output_dir)
        os.mkdir(output_dir)
    if argv[1:]:
        folder = argv[1]
        collect(folder)
    else:
        src = 'yanghe/disable'
        folders = os.popen('find %s -name webxprt3' % src).read().split()
        # print(folders)
        for folder in folders:
            # file_name = 'speedometer2-%s.xls' % utils.timezone()
            # print(file_name)
            collect(folder, output_dir)
