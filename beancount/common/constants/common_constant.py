from enum import Enum


class ParseRetCode(Enum):
    """
    将数据解析成标准格式方法的返回码
    """
    SUCCESS = 0  # 解析成功
    FAIL = 1  # 解析失败
    SKIP = 2  # 可跳过该记录，不做记录


class PN(Enum):
    """
    金额正负
    """
    P = 1  # 正
    N = 2  # 负


class Currency(Enum):
    CNY = 'CNY'


# 可结束解析的RetCode
FinalRetCode = [
    ParseRetCode.SUCCESS,
    ParseRetCode.SKIP,
]

# 可跳过记录的转账对象
SkipPartner = [
    '发给黄梅🥰',
    '黄梅🥰',
    '宇',
    '梅',
    '草捏子(曹宇)',
    '草捏子',
    '梅(黄梅)',
]

# 早中晚餐 Partner
FoodMealPartner = [
    '重庆小面',
    '黔派贵州米粉小吃',
    '楚先笙（大仟里店）',
    '志远光大',
    '桐坑牛肉粿条汤',
    '三津汤包深圳深大店',
    '深圳市八合里海记餐饮文化有限公司',
]

# 买菜 Partner
FoodGroceryPartner = [
    '姐球青菜',
    '🐂新鲜黄牛肉🐂',
    '农家豆腐',
    '小李蔬菜',
    '朴朴超市',
]

# 零食 Partner
FoodSnackPartner = [
    '面包新语',
    '贡茶（宝立方店）',

]

# 慈善捐助 Partner
RelationshipDonatePartner = [
    '水滴筹',
]

# 打车 Partner
TaxiPartner = [
    '曹操出行',
]

# 快递 Partner
ShoppingExpressPartner = [
    '中通快递',
]

# 公交 Partner
BusPartner = [
    '深圳通',
]