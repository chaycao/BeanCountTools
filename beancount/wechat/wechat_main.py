import csv
import os
import sys

import openpyxl as openpyxl

from beancount.common.constants.common_constant import ParseRetCode
from beancount.common.file_utils import write_standard_excel_record, write_bean_record
from beancount.wechat.record import WeChatRecord
from beancount.wechat.wechat_parser import WeChatParser


def parse_to_excel(in_filename):
    out_filename = in_filename.split('.')[0] + '_standard.xlsx'
    # 如果文件已存在，返回报错，避免覆盖了已标记的fail数据
    if os.path.exists(out_filename):
        print('Fail!\n%s exits!' % out_filename)
        return
    csv_reader = csv.reader(open(in_filename))

    # skip header
    for i in range(17):
        next(csv_reader)

    success_records, fail_records, skip_records = [], [], []
    for line in csv_reader:
        if line[0].startswith('--------------'):
            break
        record = WeChatRecord(line)
        retcode, record = WeChatParser().parse_to_excel_record(record)
        if retcode == ParseRetCode.SUCCESS:
            success_records.append(record)
        elif retcode == ParseRetCode.FAIL:
            fail_records.append(record)
        elif retcode == ParseRetCode.SKIP:
            skip_records.append(record)

    # reverse records
    success_records.reverse()
    fail_records.reverse()
    skip_records.reverse()

    write_standard_excel_record(out_filename, success_records, fail_records, skip_records)
    print('Success parse!')


def parse_to_bean(in_filename):
    out_filename = in_filename.split('.')[0] + '.bean'

    workbook = openpyxl.load_workbook(in_filename)
    success_sheet = workbook['success']
    fail_sheet = workbook['fail']

    # 检查 sheet 里的记录是否都标记了Account
    check_ret = WeChatParser().check_sheet_account(success_sheet)
    if not check_ret:
        print('Success sheet account is empty! Please check!')
        return

    check_ret = WeChatParser().check_sheet_account(fail_sheet)
    if not check_ret:
        print('Fail sheet account is empty! Please check!')
        return

    # 把excel转成beancount格式
    bean_records = []
    bean_records.extend(WeChatParser().parse_to_bean_record(success_sheet))
    bean_records.extend(WeChatParser().parse_to_bean_record(fail_sheet))

    write_bean_record(out_filename, bean_records)
    print('Success parse!')


if __name__ == "__main__":
    """
    python wechat_main.py excel in_filename
    eg: python wechat_main.py excel doc/wechat-20210901-20210930.csv
    
    python wechat_main.py trans in_filename
    """
    cmd = sys.argv[1]
    if cmd == 'excel':
        in_filename = sys.argv[2]
        parse_to_excel(in_filename)
    if cmd == 'bean':
        in_filename = sys.argv[2]
        parse_to_bean(in_filename)
