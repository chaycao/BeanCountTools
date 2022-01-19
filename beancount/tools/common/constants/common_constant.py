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
