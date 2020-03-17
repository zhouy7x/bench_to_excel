#!/usr/bin/python3
import os
from sys import argv

import bench_to_excel
import utils

if __name__ == '__main__':
    output_dir = '.'
    if output_dir != '.' and output_dir != '..':
        if os.path.exists(output_dir):
            os.system('rm -rf '+output_dir)
        os.mkdir(output_dir)
    if argv[1:]:
        folder = argv[1]
        file_name = folder.replace('/', '-') + '.xls'
        # print(file_name)
        with utils.touch_excel(os.path.join(output_dir, file_name)) as writer:
            jt = bench_to_excel.JetStream2(writer)
            jt.folder = folder
            # jt.mode = 'all'
            jt.run()
    else:
        src = 'yanghe/disable'
        folders = os.popen('find %s -name jetstream2' % src).read().split()
        # print(folders)
        for folder in folders:
            # file_name = 'speedometer2-%s.xls' % utils.timezone()
            # print(file_name)
            file_name = folder.replace('/', '-') + '.xls'
            # print(file_name)
            with utils.touch_excel(os.path.join(output_dir, file_name)) as writer:
                jt = bench_to_excel.JetStream2(writer)
                jt.folder = folder
                jt.mode = 'all'
                jt.run()
