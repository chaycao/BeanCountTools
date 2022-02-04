from beancount.common.constants.common_constant import ParseRetCode, SkipPartner, FoodMealPartner, \
    FoodGroceryPartner, TaxiPartner, ShoppingExpressPartner, BusPartner
from beancount.common.parser import Parser


class WeChatParser(Parser):

    def parse_to_excel_record(self, record):
        """
        :param record: wechat格式record
        :return: 标准格式record
        """
        retcode = ParseRetCode.FAIL
        result = None

        # 跳过"转账"
        if self.is_skip_transfer(record):
            retcode = ParseRetCode.SKIP
        # 跳过"全额退款"
        elif self.is_full_refund(record):
            retcode = ParseRetCode.SKIP
        # 早中晚餐
        elif self.is_food_meal(record):
            retcode, result = self.parse_food_meal(record)
        # 买菜
        elif self.is_food_grocery(record):
            retcode, result = self.parse_food_grocery(record)
        # 居家生活-药
        elif self.is_medical_drug(record):
            retcode, result = self.parse_medical_drug(record)
        # 快递
        elif self.is_shopping_express(record):
            retcode, result = self.parse_shopping_express(record)
        # 打车
        elif self.is_taxi(record):
            retcode, result = self.parse_caocao_taxi(record)
        # 公交
        elif self.is_bus(record):
            retcode, result = self.parse_bus(record)
        # 美团
        elif self.is_meituan(record):
            retcode, result = self.parse_meituan(record)


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

    def is_medical_drug(self, r):
        return r.partner == '叮当快药'

    def parse_medical_drug(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Medical:Drug; 居家生活-药',
        )
        return ParseRetCode.SUCCESS, result

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

    def is_shopping_express(self, r):
        return r.partner in ShoppingExpressPartner

    def parse_shopping_express(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:Express; 购物消费-快递',
        )
        return ParseRetCode.SUCCESS, result

    def is_taxi(self, r):
        return r.partner in TaxiPartner

    def parse_caocao_taxi(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Taxi; 行车交通-打车',
        )
        return ParseRetCode.SUCCESS, result

    def is_bus(self, r):
        return r.partner in BusPartner

    def parse_bus(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Bus; 行车交通-公交',
        )
        return ParseRetCode.SUCCESS, result

    def is_food_meal(self, r):
        return r.partner in FoodMealPartner

    def parse_food_meal(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Meal; 饮食-吃饭(早中晚餐)',
        )
        return ParseRetCode.SUCCESS, result

    def is_food_grocery(self, r):
        return r.partner in FoodGroceryPartner

    def parse_food_grocery(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Grocery; 饮食-买菜',
        )
        return ParseRetCode.SUCCESS, result
