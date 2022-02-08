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
    '黄梅'
    '宇',
    '梅',
    '草捏子(曹宇)',
    '草捏子',
    '梅(黄梅)',
    '蚂蚁财富-蚂蚁（杭州）基金销售有限公司',  # 基金操作不计入
    '花呗',
]

# 可跳过的订单状态
SkipStatus = [
    '已全额退款',
    '还款成功',
    '交易关闭',
    '退款成功',
    '充值完成',
]

# 可跳过的产品
SkipProductName = [
    '余额宝-单次转入',
    '余额宝-转出到银行卡',
    '提现-快速提现',
    '余额宝-自动转入',
    '余额宝-转出到余额',
]

# 可跳过的类别
SkipType = [
    '零钱提现'
]

# 早中晚餐 Partner
FoodMealPartner = [
    '达实智能大厦6F餐厅',
    '达实大厦餐厅',
    '重庆小面',
    '贵州米粉',
    '楚先笙',
    '志远光大',
    '粿条',
    '汤包',
    '八合里',
    '探鱼',
    '俏九州',
    '兰州拉面',
    '香满屋饺子馆',
]

# 零食 Partner
FoodSnackPartner = [
    '面包新语',
    '奈雪的茶',
    '贡茶',
    '煌上煌',
    '志远光大',
    '食尚麦点',
    '茶百道',
    '泉记牛杂',
    '拍立拿售货机',
    '丰e足食',
    '砵仔糕',
    '便利蜂',
    'luckin coffee',

]

# 买菜 Partner
FoodGroceryPartner = [
    '姐球青菜',
    '🐂新鲜黄牛肉🐂',
    '农家豆腐',
    '小李蔬菜',
    '朴朴超市',
    '元记水产',
    '每一鲜蔬菜铺',
    '客家纯手工',
    '鱼虾蟹店',
    '蔬菜百货店',
    '新发粮油百货',
    '福州朴朴电子商务有限公司',
    '业林',
    '猪肉档',
    '陈新英',
]

# 慈善捐助 Partner
RelationshipDonatePartner = [
    '水滴筹',
]

# 打车 Partner
TrafficTaxiPartner = [
    '曹操出行',
    '滴滴出行',
]

# 快递 Partner
ShoppingExpressPartner = [
    '中通快递',
    '顺丰速运',
]

# 公交 Partner
TrafficBusPartner = [
    '深圳通',
    '广州地铁',
]

# 药 Partner
MedicalDrug = [
    '叮当快药',
    '康之源医药',
]

# 电子数码 Partner
ShoppingElectronicPartner = [
    'App Store & Apple Music',
    '上海市梦迪集团贸易',
]

# 大巴（黑车） Partner
TrafficCoachPartner = [
    '贵州陆空联运汽车运输有限公司',
    '织金汽车客运总站',
]

# 水果
FoodFruitPartner = [
    '随缘（鲜果🍒）',
    '上果家精品水果店'
]
