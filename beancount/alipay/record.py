from datetime import datetime

from beancount.common.constants.common_constant import PN, Currency


class ParameterBaseObj(object):
    require_attributes = []
    common_attributes = []
    dict_attributes = {}

    def __init__(self, **kwargs):
        for k in self.require_attributes:
            if k not in kwargs:
                raise Exception("init param require not found error[%s]", self.require_attributes)
            setattr(self, k, kwargs[k])

        for k in self.common_attributes:
            if k in kwargs:
                setattr(self, k, kwargs[k])
            else:
                setattr(self, k, None)

        for k in self.dict_attributes:
            if k in kwargs:
                if isinstance(kwargs[k], list):
                    item_list = [self.dict_attributes[k](**item_info) for item_info in kwargs[k]]
                    setattr(self, k, item_list)
                else:
                    setattr(self, k, self.dict_attributes[k](**kwargs[k]))
            else:
                setattr(self, k, None)


class BeanRecord(object):
    def __init__(self, date, transactions, partner='', remark=''):
        """
        标准记录
        :param date: YYYY-MM-DD 格式
        :param transactions: 交易项
        :param partner: 交易方
        :param remark: 备注
        :return:
        """
        self.date = date
        self.transactions = transactions
        self.partner = partner
        self.remark = remark

    def __str__(self):
        header = '%s * "%s" "%s"' % (self.date, self.partner, self.remark)
        list = []
        for t in self.transactions:
            list.append(str(t))
        content = '\n'.join(list)
        return '%s\n%s\n\n' % (header, content)


class BeanRecordTransaction:
    def __init__(self, account, fee, pn, currency=Currency.CNY.value):
        """
        标准交易项
        :param account: 账户
        :param fee: 金额
        :param pn: 金额的正负
        :param currency: 货币
        :return:
        """
        self.account = account
        self.fee = fee
        self.pn = pn
        self.currency = currency

    def __str__(self):
        result = '  %s  ' % self.account
        if self.pn == PN.N:
            result += '-'
        result += '%s %s' % (self.fee, self.currency)
        return result


class StandardExcelRecord:
    def __init__(self, **kwargs):
        self.out_account = kwargs.get('out_account')
        self.in_account = kwargs.get('in_account')
        self.transaction_no = kwargs.get('transaction_no')
        self.date = kwargs['date']
        self.fee = kwargs['fee']
        self.status = kwargs.get('status')
        self.pay_type = kwargs.get('pay_type')
        self.type = kwargs.get('type')
        self.partner = kwargs.get('partner')
        self.product_name = kwargs.get('product_name')
        self.remark = kwargs.get('remark')


class AlipayRecord:
    def __init__(self, line):
        self.in_account = None
        self.out_account = None
        self.transaction_no = line[0].strip()  # 交易号
        self.order_no = line[1].strip()  # 商家订单号
        self.ctime = trans_ctime(line[2].strip())  # 创建时间
        self.pay_time = line[3].strip()  # 付款时间
        self.mtime = line[4].strip()  # 修改时间
        self.source = line[5].strip()  # 交易来源地
        self.type = line[6].strip()  # 类型
        self.partner = line[7].strip()  # 交易对方
        self.product_name = line[8].strip()  # 商品名称
        self.fee = line[9].strip()  # 金额(元)
        self.pay_type = line[10].strip()  # 收/支
        self.status = line[11].strip()  # 交易状态
        self.service_fee = line[12].strip()  # 服务费
        self.return_fee = line[13].strip()  # 退款
        self.remark = line[14].strip()  # 备注
        self.fund_status = line[15].strip()  # 资金状态


def trans_ctime(ctime):
    try:
        date = datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print('trans_time error, %s' % ctime)
        raise e
    return date.strftime('%Y-%m-%d')
