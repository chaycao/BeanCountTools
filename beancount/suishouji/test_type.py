from beancount.suishouji.suishouji_constant import expenses_type_map, income_type_map, assets_map

# account_map = expenses_type_map
# account_map = income_type_map
account_map = assets_map

account_set = set()
for key in account_map:
    account_set.add(account_map[key])

account_set = list(account_set)
account_set = sorted(account_set)
# for key in account_set:
#     print("{\n'account':'Assets:%s',\n'remark':''\n}," % key)

s = """2018-01-01 open Income:Financial:Fund CNY  ;金融-基金
2018-01-01 open Income:Financial:Invest CNY  ;金融-投资
2018-01-01 open Income:Financial:YuEbao CNY  ;金融-余额宝
2018-01-01 open Income:Job:Bonus CNY  ;职业-奖金
2018-01-01 open Income:Job:PartTime CNY  ;职业-兼职
2018-01-01 open Income:Job:Salary CNY  ;职业-工资
2018-01-01 open Income:Other:Operate CNY  ;其他-经营
2018-01-01 open Income:Other:Win CNY  ;其他-中奖
2018-01-01 open Income:Other:WindfallBenefit CNY  ;其他-意外来钱
2018-01-01 open Income:Relationship:Birthday CNY  ;人情收礼-生日
2018-01-01 open Income:Relationship:Gift CNY  ;人情收礼-红包
2018-01-01 open Income:Relationship:Marry CNY  ;人情收礼-婚嫁收礼"""
rows = s.split('\n')
for row in rows:
    items = row.split(' ')
    # print("{\n'account':'%s',\n'remark':'%s'\n}," % (items[2], items[5].strip(';')))
    print("'%s; %s'," % (items[2], items[5].strip(';')))