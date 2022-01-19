from datetime import datetime


class WeChatRecord:
    def __init__(self, line):
        self.in_account = None
        self.out_account = None
        self.ctime = trans_ctime(line[0].strip())  # 交易时间
        self.type = line[1].strip()  # 交易类型
        self.partner = line[2].strip()  # 交易对方
        self.product_name = line[3].strip()  # 商品名称
        self.pay_type = line[4].strip()  # 收/支
        self.fee = line[5].strip()  # 金额(元)
        self.pay_method = line[6].strip()  # 支付方式
        self.status = line[7].strip()  # 当前状态
        self.transaction_no = line[8].strip()  # 交易单号
        self.order_no = line[9].strip()  # 商户单号
        self.remark = line[10].strip()  # 备注


def trans_ctime(ctime):
    try:
        date = datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print('trans_time error, %s' % ctime)
        raise e
    return date.strftime('%Y-%m-%d')
