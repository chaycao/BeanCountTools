from beancount.common.constants.common_constant import FinalRetCode, ParseRetCode
from beancount.common.parser import Parser
from beancount.wechat.constants import SkipPartner


class WeChatParser(Parser):

    def parse_to_excel_record(self, record):
        """
        :param record: wechat格式record
        :return: 标准格式record
        """
        retcode = ParseRetCode.FAIL
        result = None
        if self.is_skip_transfer(record):
            retcode = ParseRetCode.SKIP
        elif self.is_full_refund(record):
            retcode = ParseRetCode.SKIP
        elif self.is_dashi(record):
            retcode, result = self.parse_dashi(record)
        elif self.is_dingdang_drug(record):
            retcode, result = self.parse_dingdang_drug(record)
        elif self.is_meituan(record):
            retcode, result = self.parse_meituan(record)
        elif self.is_zhongtong(record):
            retcode, result = self.parse_zhongtong(record)
        elif self.is_caocao_taxi(record):
            retcode, result = self.parse_caocao_taxi(record)


        # 解析失败转成未标记分类的excel格式
        if retcode == ParseRetCode.SKIP:
            result = self.parse_to_skip_excel_record(record)
        elif retcode == ParseRetCode.FAIL and not result:
            result = self.parse_to_fail_excel_record(record)
        return retcode, result

    def is_skip_transfer(self, record):
        return record.partner in SkipPartner

    def is_full_refund(self, r):
        return r.status == '已全额退款'

    def is_dashi(self, r):
        return r.partner.startswith('达实')

    def parse_dashi(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Meal; 饮食-吃饭(早中晚餐)',
        )
        return ParseRetCode.SUCCESS, result

    def is_dingdang_drug(self, r):
        return r.partner == '叮当快药'

    def parse_dingdang_drug(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Medical:Drug; 居家生活-药',
        )
        return ParseRetCode.SUCCESS, result

    def is_meituan(self, r):
        return r.partner == '美团平台商户'

    def parse_meituan(self, r):
        # meituan 默认为吃饭
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Meal; 饮食-吃饭(早中晚餐)',
        )
        return ParseRetCode.FAIL, result

    def is_zhongtong(self, r):
        return r.partner == '中通快递'

    def parse_zhongtong(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:Express; 购物消费-快递',
        )
        return ParseRetCode.SUCCESS, result

    def is_caocao_taxi(self, r):
        return r.partner == '曹操出行'

    def parse_caocao_taxi(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Taxi; 行车交通-打车',
        )
        return ParseRetCode.SUCCESS, result
