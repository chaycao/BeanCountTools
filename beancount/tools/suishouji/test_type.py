from beancount.tools.suishouji.suishouji_constant import expenses_type_map, income_type_map, assets_map

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

s = """2018-01-01 open Assets:FamilySharedBalance CNY  ;家庭公用结余
2018-01-01 open Assets:Finance:Bound CNY  ;债券
2018-01-01 open Assets:Finance:Fund CNY  ;基金账户
2018-01-01 open Assets:Home:Balance CNY  ;结余
2018-01-01 open Assets:Home:FamilyShared CNY  ;家庭公用
2018-01-01 open Assets:Loan:Pay CNY  ;应付款项
2018-01-01 open Assets:Loan:Receive CNY  ;应收款项
2018-01-01 open Assets:Marry CNY  ;结婚用
2018-01-01 open Assets:Pension:Cao CNY  ;曹家养老金
2018-01-01 open Assets:Pension:Huang CNY  ;黄家养老金
2018-01-01 open Assets:Pocket:Husband CNY  ;老公钱包
2018-01-01 open Assets:Pocket:Wife CNY  ;老婆钱包
2018-01-01 open Assets:RelationShip:Gift CNY  ;份子钱"""
rows = s.split('\n')
for row in rows:
    items = row.split(' ')
    # print("{\n'account':'%s',\n'remark':'%s'\n}," % (items[2], items[5].strip(';')))
    print("'%s; %s'," % (items[2], items[5].strip(';')))