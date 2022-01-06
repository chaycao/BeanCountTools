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

s = """2018-01-01 open Expenses:Baby:BabySupplies CNY  ;宝宝费用-宝宝用品
2018-01-01 open Expenses:Baby:Clothes CNY  ;宝宝费用-宝宝衣服
2018-01-01 open Expenses:Baby:Education CNY  ;宝宝费用-宝宝教育
2018-01-01 open Expenses:Baby:Food CNY  ;宝宝费用-宝宝食品
2018-01-01 open Expenses:Baby:Medical CNY  ;宝宝费用-医疗护理
2018-01-01 open Expenses:Baby:MotherSupplies CNY  ;宝宝费用-妈妈用品
2018-01-01 open Expenses:Baby:Other CNY  ;宝宝费用-宝宝其他
2018-01-01 open Expenses:Baby:Toy CNY  ;宝宝费用-宝宝玩具
2018-01-01 open Expenses:Education:SchoolFee CNY  ;教育-学费
2018-01-01 open Expenses:Entertainment CNY  ;休闲娱乐-K歌
2018-01-01 open Expenses:Financial:Insurance CNY  ;金融保险-人身保险
2018-01-01 open Expenses:Home:CommunityManagementFee CNY  ;居家物业-物业管理
2018-01-01 open Expenses:Home:Food CNY  ;居家生活-食物
2018-01-01 open Expenses:Home:Fruit CNY  ;居家生活-水果
2018-01-01 open Expenses:Home:Milk CNY  ;居家生活-牛奶
2018-01-01 open Expenses:Home:NetFee CNY  ;居家生活-网费
2018-01-01 open Expenses:Home:PhoneFee CNY  ;居家生活-话费
2018-01-01 open Expenses:Home:Rent CNY  ;居家生活-房租
2018-01-01 open Expenses:Home:Repair CNY  ;居家生活-维修
2018-01-01 open Expenses:Home:Snack CNY  ;居家生活-零食
2018-01-01 open Expenses:Home:WaterElectGas CNY  ;居家生活-水电煤气
2018-01-01 open Expenses:Home:Wine CNY  ;居家生活-酒
2018-01-01 open Expenses:Medical:Drug CNY  ;居家生活-药
2018-01-01 open Expenses:Medical:Hospital CNY  ;居家生活-医疗
2018-01-01 open Expenses:Other:AccidentallyLost CNY  ;其他-意外丢失
2018-01-01 open Expenses:Other:BadDebtLost CNY  ;其他-烂账损失
2018-01-01 open Expenses:Other:Other CNY  ;其他-其他
2018-01-01 open Expenses:Other:PartyMembershipDues CNY  ;其他-党费
2018-01-01 open Expenses:Relationship:Donate CNY  ;人情往来-慈善捐助
2018-01-01 open Expenses:Relationship:GiftAndTreat CNY  ;人情往来-送礼请客
2018-01-01 open Expenses:Relationship:Parent CNY  ;人情往来-孝敬家长
2018-01-01 open Expenses:Shopping:Bag CNY  ;衣服饰品-鞋帽包包
2018-01-01 open Expenses:Shopping:Bathroom CNY  ;购物消费-洗护用品
2018-01-01 open Expenses:Shopping:Book CNY  ;购物消费-书报杂志
2018-01-01 open Expenses:Shopping:Cleaning CNY  ;购物消费-清洁用品
2018-01-01 open Expenses:Shopping:Clothes CNY  ;购物消费-衣服裤子
2018-01-01 open Expenses:Shopping:Cosmetic CNY  ;购物消费-化妆饰品
2018-01-01 open Expenses:Shopping:DailySupplies CNY  ;购物消费-日常用品
2018-01-01 open Expenses:Shopping:Decoration CNY  ;购物消费-家居饰品
2018-01-01 open Expenses:Shopping:Electronic CNY  ;购物消费-电子数码
2018-01-01 open Expenses:Shopping:Express CNY  ;购物消费-快递
2018-01-01 open Expenses:Shopping:Furniture CNY  ;购物消费-家具家电
2018-01-01 open Expenses:Shopping:Jewelry CNY  ;购物消费-珠宝首饰
2018-01-01 open Expenses:Shopping:Kitchen CNY  ;购物消费-厨房用品
2018-01-01 open Expenses:Shopping:Office CNY  ;购物消费-办公用品
2018-01-01 open Expenses:Shopping:Sport CNY  ;购物消费-运动器械
2018-01-01 open Expenses:Study CNY  ;学习进修
2018-01-01 open Expenses:Traffic:Airplane CNY  ;行车交通-飞机
2018-01-01 open Expenses:Traffic:Bus CNY  ;行车交通-公交
2018-01-01 open Expenses:Traffic:Park CNY  ;行车交通-停车
2018-01-01 open Expenses:Traffic:RentCar CNY  ;行车交通-租车
2018-01-01 open Expenses:Traffic:Repair CNY  ;行车交通-维修
2018-01-01 open Expenses:Traffic:Taxi CNY  ;行车交通-打车
2018-01-01 open Expenses:Traffic:Train CNY  ;行车交通-火车
2018-01-01 open Expenses:Travel:Food CNY  ;出差旅游-餐饮费
2018-01-01 open Expenses:Travel:Hotel CNY  ;出差旅游-住宿费
2018-01-01 open Expenses:Travel:Transport CNY  ;出差旅游-交通费"""
rows = s.split('\n')
for row in rows:
    items = row.split(' ')
    print("{\n'account':'%s',\n'remark':'%s'\n}," % (items[2], items[5].strip(';')))