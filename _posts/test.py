# -*- coding: utf-8 -*-

import os
import re
import datetime


def rename_file(file_name, new_file_name):
    try:
        os.rename(file_name, new_file_name)
        print(f'{file_name} 已重命名为 {new_file_name}')
    except OSError as e:
        print(f'{file_name} 重命名失败，错误原因: {e}')

if __name__ == '__main__':
    # 获取当前时间，并格式化时间字符串
    now_time = datetime.datetime.now()
    formatted_time = now_time.strftime('%Y-%m-%d')

    # 获取当前目录下的全部文件
    current_dir = os.getcwd()
    all_files = os.listdir(current_dir)

    for file_name in all_files:
        # 若文件不存在，则跳过该文件名，继续循环
        if not os.path.exists(file_name):
            continue
        if file_name.endswith('.md') and not re.match(r'^\d{4}-\d{2}-\d{2}-', file_name):
            # 为源文件名前添加时间格式字符串
            new_file_name = f'{formatted_time}-{file_name}'
            rename_file(file_name, new_file_name)
            



