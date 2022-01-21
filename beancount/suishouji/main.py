import csv

from beancount.suishouji.suishouji_constant import expenses_type_map, assets_map, income_type_map


def trans_expenses(record):
    header = '%s * "" "%s"' % (record.date, record.remark)
    expense = '  Expenses:%s  %s CNY' % (expenses_type_map[record.type], record.fee)
    assets = '  Assets:%s  -%s CNY' % (assets_map[record.account], record.fee)
    return '%s\n%s\n%s\n\n' % (header, expense, assets)

def trans_income(record):
    header = '%s * "" "%s"' % (record.date, record.remark)
    Income = '  Income:%s  -%s CNY' % (income_type_map[record.type], record.fee)
    assets = '  Assets:%s  %s CNY' % (assets_map[record.account], record.fee)
    return '%s\n%s\n%s\n\n' % (header, assets, Income)

def trans_trans(in_record, out_record):
    header = '%s * "" ""' % (in_record.date)
    in_trans = '  Assets:%s  %s CNY' % (assets_map[in_record.account], in_record.fee)
    out_trans = '  Assets:%s  -%s CNY' % (assets_map[out_record.account], out_record.fee)
    return '%s\n%s\n%s\n\n' % (header, in_trans, out_trans)

def trans_change(record):
    header = '%s * "" "%s"' % (record.date, record.remark)
    expense = '  Expenses:Other:BadDebtLost  %s CNY' % (record.fee[1:])
    assets = '  Assets:%s  %s CNY' % (assets_map[record.account], record.fee)
    return '%s\n%s\n%s\n\n' % (header, expense, assets)

def write_file(filename, content):
    with open(filename, 'a+') as file:
        file.write(content)

def clean_file(filename):
    with open(filename, 'w') as file:
        pass


class SuiShouJiRecord:
    def __init__(self, line):
        self.change_type = line[0]
        self.date = line[1][:10]
        self.type = line[2] + '-' + line[3]
        self.account = line[5]
        self.fee = line[7]
        self.remark = line[10]


if __name__ == "__main__":
    # read file
    read_file_name = 'doc/suishouji-20211207.csv'
    csv_reader = csv.reader(open(read_file_name))

    # skip header
    next(csv_reader)
    next(csv_reader)

    write_file_name = 'doc/test.beancount'
    clean_file(write_file_name)
    result = []
    for line in csv_reader:
        record = SuiShouJiRecord(line)
        content = ''
        if record.change_type == '支出':
            content = trans_expenses(record)
        elif record.change_type == '收入':
            content = trans_income(record)
        elif record.change_type == '转入':
            out_record = SuiShouJiRecord(next(csv_reader))
            content = trans_trans(record, out_record)
        elif record.change_type == '余额变更':
            content = trans_change(record)
        else:
            print(line)
        result.append(content)
    result.reverse()
    for item in result:
        write_file(write_file_name, item)