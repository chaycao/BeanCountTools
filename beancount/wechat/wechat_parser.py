from beancount.common.constants.common_constant import ParseRetCode
from beancount.common.parser import Parser


class WeChatParser(Parser):

    def special_parse(self, record):
        retcode = ParseRetCode.FAIL
        result = None
        if self.is_meituan(record):
            retcode, result = self.parse_meituan(record)
        # 红包收入
        elif self.is_income_hongbao(record):
            retcode, result = self.parse_income_hongbao(record)
        return retcode, result

    def is_meituan(self, r):
        return r.partner == '美团平台商户'

    def parse_meituan(self, r):
        # meituan 默认为吃饭，返回FAIL表示需要手动确认分类
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Meal; 饮食-吃饭(早中晚餐)',
        )
        return ParseRetCode.FAIL, result

    def is_income_hongbao(self, r):
        if r.pay_type == '收入' and r.type == '微信红包':
            return True
        return False

    def parse_income_hongbao(self, r):
        # 红包收入 默认收入到结余，返回FAIL表示需要手动确认分类
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Income:Relationship:Gift; 人情收礼-红包',
            in_account='Assets:Home:Balance; 结余',
        )
        return ParseRetCode.FAIL, result
