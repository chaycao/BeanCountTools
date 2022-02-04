from beancount.common.constants.common_constant import ParseRetCode, SkipPartner
from beancount.common.parser import Parser


class AliPayParser(Parser):

    def parse_to_excel_record(self, record):
        """
        :param record: alipay格式record
        :return: 标准格式record
        """
        retcode = ParseRetCode.FAIL
        result = None
        if self.is_skip_transfer(record):
            retcode = ParseRetCode.SKIP
        elif self.is_success_repay(record):
            # 还款成功
            retcode = ParseRetCode.SKIP
        elif self.is_close_trade(record):
            # 关闭交易
            retcode = ParseRetCode.SKIP
        elif self.is_fund_operation(record):
            # 基金操作
            retcode = ParseRetCode.SKIP
        elif self.is_yuebao_single_transfer(record):
            # 余额宝-单次转入
            retcode = ParseRetCode.SKIP
        elif self.is_huabei(record):
            # 花呗
            retcode = ParseRetCode.SKIP
        elif self.is_yuebao_to_card(record):
            # 余额宝-转出到银行卡
            retcode = ParseRetCode.SKIP
        elif self.is_quick_withdrawal(record):
            # 快速提现
            retcode = ParseRetCode.SKIP
        elif self.is_yuebao_auto_transfer(record):
            # 余额宝-自动转入
            retcode = ParseRetCode.SKIP
        elif self.is_success_refund(record):
            # 退款成功
            retcode = ParseRetCode.SKIP

        elif self.is_yuebao_income(record):
            # 余额宝收入
            retcode, result = self.parse_yuebao(record)
        elif self.is_didi_outcome(record):
            # 滴滴出行支出
            retcode, result = self.parse_didi_outcome(record)

        elif self.is_apple_app_store(record):
            # App Store & Apple Music
            retcode, result = self.parse_apple_app_store(record)
        elif self.is_mutual_treasure(record):
            # 相互宝分摊
            retcode, result = self.parse_mutual_treasure(record)

        elif self.is_freight_insurance(record):
            # 保险-买家版运费险
            retcode, result = self.parse_freight_insurance(record)
        elif self.is_water_elect_gas(record):
            # 水电煤气
            retcode, result = self.parse_water_elect_gas(record)
        elif self.is_train(record):
            # 火车票
            retcode, result = self.parse_train(record)
        elif self.is_plane(record):
            # 飞机票
            retcode, result = self.parse_plane(record)
        elif self.is_vpn(record):
            # VPN
            retcode, result = self.parse_vpn(record)

        # 解析失败转成未标记分类的excel格式
        if retcode == ParseRetCode.SKIP:
            result = self.parse_to_skip_excel_record(record)
        elif retcode == ParseRetCode.FAIL:
            result = self.parse_to_fail_excel_record(record)
        return retcode, result

    def is_skip_transfer(self, record):
        return record.partner in SkipPartner

    def is_yuebao_income(self, record):
        return record.product_name.startswith('余额宝') and record.product_name.endswith('收益发放')

    def parse_yuebao(self, record):
        if self.is_yuebao_income(record):
            return self.parse_yuebao_income(record)
        return ParseRetCode.FAIL, None

    def parse_yuebao_income(self, record):
        result = self.parse_to_excel_record_with_classify(
            record,
            out_account='Income:Financial:YuEbao; 金融-余额宝',
            in_account='Assets:Home:Balance; 结余',
        )
        return ParseRetCode.SUCCESS, result

    def is_didi_outcome(self, record):
        return record.partner == '滴滴出行'

    def parse_didi_outcome(self, record):
        result = self.parse_to_excel_record_with_classify(
            record,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Taxi; 行车交通-打车',
        )
        return ParseRetCode.SUCCESS, result

    def is_success_repay(self, record):
        return record.status == '还款成功'

    def is_close_trade(self, record):
        return record.status == '交易关闭'

    def is_apple_app_store(self, record):
        return record.partner == 'App Store & Apple Music'

    def parse_apple_app_store(self, record):
        result = self.parse_to_excel_record_with_classify(
            record,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:Electronic; 购物消费-电子数码',
        )
        return ParseRetCode.SUCCESS, result

    def is_quick_withdrawal(self, record):
        return record.product_name == '提现-快速提现'

    def is_yuebao_auto_transfer(self, record):
        return record.product_name == '余额宝-自动转入'

    def is_success_refund(self, r):
        return r.status == '退款成功'

    def is_mutual_treasure(self, r):
        return r.product_name.startswith('相互宝分摊')

    def parse_mutual_treasure(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Financial:Insurance; 金融保险-人身保险',
        )
        return ParseRetCode.SUCCESS, result

    def is_fund_operation(self, r):
        return r.partner == '蚂蚁财富-蚂蚁（杭州）基金销售有限公司'

    def is_yuebao_single_transfer(self, r):
        return r.product_name == '余额宝-单次转入'

    def is_huabei(self, r):
        return r.partner == '花呗'

    def is_yuebao_to_card(self, r):
        return r.product_name == '余额宝-转出到银行卡'

    def is_freight_insurance(self, r):
        return r.product_name.startswith('保险-买家版运费险')

    def parse_freight_insurance(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:FreightInsurance; 购物消费-运费险',
        )
        return ParseRetCode.SUCCESS, result

    def is_water_elect_gas(self, r):
        return r.product_name.startswith('电费') or r.product_name.startswith('水费')

    def parse_water_elect_gas(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Home:WaterElectGas; 居家生活-水电煤气',
        )
        return ParseRetCode.SUCCESS, result

    def is_train(self, r):
        return r.product_name == '火车票'

    def parse_train(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Train; 行车交通-火车',
        )
        return ParseRetCode.SUCCESS, result

    def is_plane(self, r):
        return r.product_name.startswith('机票订单付款')

    def parse_plane(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Airplane; 行车交通-飞机',
        )
        return ParseRetCode.SUCCESS, result

    def is_vpn(self, r):
        return r.partner == '上海市梦迪集团贸易'

    def parse_vpn(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Pocket:Husband; 老公钱包',
            in_account='Expenses:Shopping:Electronic; 购物消费-电子数码',
        )
        return ParseRetCode.SUCCESS, result
