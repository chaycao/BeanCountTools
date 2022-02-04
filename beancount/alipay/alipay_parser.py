from beancount.common.constants.common_constant import ParseRetCode, SkipPartner
from beancount.common.parser import Parser


class AliPayParser(Parser):

    def special_parse(self, record):
        retcode = ParseRetCode.FAIL
        result = None
        # 余额宝-收入
        if self.is_yuebao_income(record):
            retcode, result = self.parse_yuebao(record)
        # 相互宝分摊
        elif self.is_mutual_treasure(record):
            retcode, result = self.parse_mutual_treasure(record)
        return retcode, result

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

    def is_mutual_treasure(self, r):
        return r.product_name.startswith('相互宝分摊')

    def parse_mutual_treasure(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Financial:Insurance; 金融保险-人身保险',
        )
        return ParseRetCode.SUCCESS, result
