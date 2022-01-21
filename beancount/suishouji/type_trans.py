import csv

# read file
from beancount.suishouji.suishouji_constant import expenses_type_map, income_type_map, assets_map

file_name = 'doc/suishouji-20211207.csv'
csv_reader = csv.reader(open(file_name))

# skip header
next(csv_reader)
next(csv_reader)

expenses_type_set = set()
income_type_set = set()
account_set = set()
# for line in csv_reader:
#     type = line[2] + '-' + line[3]
#     if line[0] in ('支出'):
#         expenses_type_set.add(type)
#     elif line[0] in ('收入'):
#         income_type_set.add(type)
#     account_set.add(line[5])

list = []
for key in assets_map:
    value = assets_map[key]
    if value not in expenses_type_set:
        expenses_type_set.add(value)
        list.append('2018-01-01 open Assets:%s CNY  ;%s' % (value, key))

list = sorted(list)
for item in list:
    print(item)

'''
类别处理
'''
def trans_expenses_type(type):
    result = type
    if type.startswith('交流通讯'):
        return 'Communication'
    if type.startswith('人情'):
        if type.endswith('家长'):
            return 'Relationship:Parent'
        elif type.endswith('捐助'):
            return 'Relationship:Donate'
        else:
            return 'Relationship:GiftAndTreat'
    if type.startswith('休闲'):
        return 'Entertainment'
    if type.startswith('其他'):
        if type.endswith('党费'):
            return 'Other:PartyMembershipDues'
        if type.endswith('丢失'):
            return 'Other:AccidentallyLost'
        if type.endswith('损失'):
            return 'Other:BadDebtLost'
        else:
            return 'Other:Other'
    if type.startswith('出差旅游'):
        if type.endswith('交通费'):
            return 'Travel:Transport'
        if type.endswith('住宿费'):
            return 'Travel:Hotel'
        if type.endswith('餐饮费'):
            return 'Travel:Food'
    if type.startswith('医疗保健'):
        if type.endswith('药品费'):
            return 'Medical:Drug'
        else:
            return 'Medical:Hospital'
    if type.startswith('学习'):
        return 'Study'
    if type.startswith('宝宝'):
        if type.endswith('妈妈用品'):
            return 'Baby:MotherSupplies'
        if type.endswith('宝宝其他'):
            return 'Baby:Other'
        if type.endswith('教育'):
            return 'Baby:Education'
        if type.endswith('玩具'):
            return 'Baby:Toy'
        if type.endswith('宝宝用品'):
            return 'Baby:BabySupplies'
        if type.endswith('宝宝衣服'):
            return 'Baby:Clothes'
        if type.endswith('宝宝食品'):
            return 'Baby:Food'
        if type.endswith('医疗护理'):
            return 'Baby:Medical'
    if type.startswith('居家物业'):
        if type.__contains__('房租'):
            return 'Home:Rent'
        if type.endswith('日常用品'):
            return 'Shopping:DailySupplies'
        if type.endswith('煤气'):
            return 'Home:WaterElectGas'
        if type.endswith('管理'):
            return 'Home:CommunityManagementFee'
        if type.endswith('保养'):
            return 'Home:Repair'

    return result

def trans_income_type(type):
    result = type
    return result




#
# print('\n')
# print('账户：')
# account_set = sorted(account_set)
# for item in account_set:
#     # result = "'%s':'%s'" % (item, trans_income_type(item))
#     result = "%s" % (item)
#     print(result)
#
# print('支出类别：')
# expenses_type_set = sorted(expenses_type_set)
# for item in expenses_type_set:
#     # result = "'%s':'%s'" % (item, trans_expenses_type(item))
#     result = "%s" % (trans_expenses_type(item))
#     print(result)
#
# print('\n')
# print('收入类别：')
# income_type_set = sorted(income_type_set)
# for item in income_type_set:
#     # result = "'%s':'%s'" % (item, trans_income_type(item))
#     result = "%s" % (item)
#     print(result)