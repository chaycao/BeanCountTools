from beancount.alipay.record import BeanRecordTransaction, BeanRecord, StandardExcelRecord
from beancount.common.constants.account_constant import SKIP_ACCOUNT
from beancount.common.constants.common_constant import PN, FoodMealPartner, ParseRetCode, FoodGroceryPartner, \
    TrafficBusPartner, TrafficTaxiPartner, ShoppingExpressPartner, MedicalDrug, SkipStatus, SkipPartner, \
    SkipProductName, ShoppingElectronicPartner, FoodSnackPartner, TrafficCoachPartner, FoodFruitPartner, \
    RelationshipDonatePartner, SkipType


class Parser(object):
    def parse_to_excel_record(self, record):
        """
        :param record: wechat格式record
        :return: 标准格式record
        """
        retcode = ParseRetCode.FAIL
        result = None

        # 跳过
        if self.is_skip_partner(record):
            retcode = ParseRetCode.SKIP
        elif self.is_skip_status(record):
            retcode = ParseRetCode.SKIP
        elif self.is_skip_product_name(record):
            retcode = ParseRetCode.SKIP
        elif self.is_skip_type(record):
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
        elif self.is_traffic_taxi(record):
            retcode, result = self.parse_traffic_taxi(record)
        # 公交
        elif self.is_traffic_bus(record):
            retcode, result = self.parse_traffic_bus(record)
        # 电子数码
        elif self.is_shopping_electronic(record):
            retcode, result = self.parse_shopping_electronic(record)
        # 水电煤气
        elif self.is_water_elect_gas(record):
            retcode, result = self.parse_water_elect_gas(record)
        # 火车票
        elif self.is_traffic_train(record):
            retcode, result = self.parse_traffic_train(record)
        # 飞机票
        elif self.is_traffic_plane(record):
            retcode, result = self.parse_traffic_plane(record)
        # 运费险
        elif self.is_shopping_freight_insurance(record):
            retcode, result = self.parse_shopping_freight_insurance(record)
        # 话费
        elif self.is_home_phone_fee(record):
            retcode, result = self.parse_home_phone_fee(record)
        # 零食
        elif self.is_food_snack(record):
            retcode, result = self.parse_food_snack(record)
        # 大巴黑车
        elif self.is_traffic_coach(record):
            retcode, result = self.parse_traffic_coach(record)
        # 网费
        elif self.is_home_net_fee(record):
            retcode, result = self.parse_home_net_fee(record)
        # 水果
        elif self.is_food_fruit(record):
            retcode, result = self.parse_food_fruit(record)
        # 慈善捐助
        elif self.is_relationship_donate(record):
            retcode, result = self.parse_relationship_donate(record)
        else:
            retcode, result = self.special_parse(record)

        # 解析失败转成未标记分类的excel格式
        if retcode == ParseRetCode.SKIP:
            result = self.parse_to_skip_excel_record(record)
        elif retcode == ParseRetCode.FAIL and not result:
            result = self.parse_to_fail_excel_record(record)
        return retcode, result

    def special_parse(self, record):
        return ParseRetCode.FAIL, None

    def parse_to_fail_excel_record(self, record):
        return self.parse_to_excel_record_with_classify(record, out_account='Assets:Home:FamilyShared; 家庭公用')

    def parse_to_skip_excel_record(self, record):
        return self.parse_to_excel_record_with_classify(record)

    def parse_to_excel_record_with_classify(self, record, out_account='', in_account=''):
        kwargs = {
            'out_account': out_account,
            'in_account': in_account,
            'transaction_no': record.transaction_no,
            'date': record.ctime,
            'fee': record.fee,
            'status': record.status,
            'pay_type': record.pay_type,
            'type': record.type,
            'partner': record.partner,
            'product_name': record.product_name,
            'remark': record.remark,
        }
        return StandardExcelRecord(**kwargs)

    def parse_to_excel_record_without_classify(self, record):
        kwargs = {
            'transaction_no': record.transaction_no,
            'date': record.ctime,
            'fee': record.fee,
            'status': record.status,
            'pay_type': record.pay_type,
            'type': record.type,
            'partner': record.partner,
            'product_name': record.product_name,
            'remark': record.remark,
        }
        return StandardExcelRecord(**kwargs)

    def check_sheet_account(self, sheet):
        """
        检查每一行的前两列 out_account、in_account 是否为空
        """
        for row in sheet.rows:
            if not row[0].value or not row[1].value:
                return False
            out_account = row[0].value.strip()
            in_account = row[1].value.strip()
            if not out_account or not in_account:
                return False
        return True

    def parse_to_bean_record(self, sheet):
        """
        将sheet的记录转成beancount格式
        """
        bean_records = []
        for idx, row in enumerate(sheet.rows):
            # 跳过行首
            if idx == 0:
                continue

            out_account = row[0].value
            in_account = row[1].value

            # 如果为SKIP，需要跳过该记录
            if out_account == SKIP_ACCOUNT or in_account == SKIP_ACCOUNT:
                continue

            # 去除注释
            out_account = out_account.split(';')[0]
            in_account = in_account.split(';')[0]

            date = row[2].value
            fee = row[3].value
            partner = row[7].value
            remark = row[9].value or ''

            out_t = BeanRecordTransaction(
                out_account,
                fee,
                PN.N
            )
            in_t = BeanRecordTransaction(
                in_account,
                fee,
                PN.P
            )
            transactions = [out_t, in_t]
            bean_record = BeanRecord(date, transactions, partner, remark)
            bean_records.append(bean_record)

        return bean_records

    def is_skip_partner(self, record):
        return record.partner in SkipPartner

    def is_skip_status(self, r):
        return r.status in SkipStatus

    def is_skip_product_name(self, r):
        return r.product_name in SkipProductName

    def is_skip_type(self, r):
        return r.type in SkipType

    def is_food_meal(self, r):
        for p in FoodMealPartner:
            if p in r.partner:
                return True
        return False

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

    def is_traffic_bus(self, r):
        for p in TrafficBusPartner:
            if p in r.partner:
                return True
        return False

    def parse_traffic_bus(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Bus; 行车交通-公交',
        )
        return ParseRetCode.SUCCESS, result

    def is_traffic_taxi(self, r):
        return r.partner in TrafficTaxiPartner

    def parse_traffic_taxi(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Taxi; 行车交通-打车',
        )
        return ParseRetCode.SUCCESS, result

    def is_shopping_express(self, r):
        if r.partner in ShoppingExpressPartner:
            return True
        elif r.product_name.startswith('菜鸟裹裹-寄件费'):
            return True
        return False

    def parse_shopping_express(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:Express; 购物消费-快递',
        )
        return ParseRetCode.SUCCESS, result

    def is_medical_drug(self, r):
        for p in MedicalDrug:
            if p in r.partner:
                return True
        return False

    def parse_medical_drug(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Medical:Drug; 居家生活-药',
        )
        return ParseRetCode.SUCCESS, result

    def is_shopping_electronic(self, r):
        return r.partner in ShoppingElectronicPartner

    def parse_shopping_electronic(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:Electronic; 购物消费-电子数码',
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

    def is_traffic_train(self, r):
        return r.product_name == '火车票'

    def parse_traffic_train(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Train; 行车交通-火车',
        )
        return ParseRetCode.SUCCESS, result

    def is_traffic_plane(self, r):
        return r.product_name.startswith('机票订单付款')

    def parse_traffic_plane(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Airplane; 行车交通-飞机',
        )
        return ParseRetCode.SUCCESS, result

    def is_shopping_freight_insurance(self, r):
        return r.product_name.startswith('保险-买家版运费险')

    def parse_shopping_freight_insurance(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Shopping:FreightInsurance; 购物消费-运费险',
        )
        return ParseRetCode.SUCCESS, result

    def is_home_phone_fee(self, r):
        return r.product_name == '手机充值'

    def parse_home_phone_fee(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Home:PhoneFee; 居家生活-话费',
        )
        return ParseRetCode.SUCCESS, result

    def is_food_snack(self, r):
        for p in FoodSnackPartner:
            if p in r.partner:
                return True
        return False

    def parse_food_snack(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Snack; 饮食-零食',
        )
        return ParseRetCode.SUCCESS, result

    def is_traffic_coach(self, r):
        for p in TrafficCoachPartner:
            if p in r.partner:
                return True
        return False

    def parse_traffic_coach(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Traffic:Coach; 行车交通-大巴(黑车)',
        )
        return ParseRetCode.SUCCESS, result

    def is_home_net_fee(self, r):
        if r.product_name == '中国电信广东分公司充值':
            return True
        return False

    def parse_home_net_fee(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Home:NetFee; 居家生活-网费',
        )
        return ParseRetCode.SUCCESS, result

    def is_food_fruit(self, r):
        if r.partner in FoodFruitPartner:
            return True
        return False

    def parse_food_fruit(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Food:Fruit; 饮食-水果',
        )
        return ParseRetCode.SUCCESS, result

    def is_relationship_donate(self, r):
        if r.partner in RelationshipDonatePartner:
            return True
        return False

    def parse_relationship_donate(self, r):
        result = self.parse_to_excel_record_with_classify(
            r,
            out_account='Assets:Home:FamilyShared; 家庭公用',
            in_account='Expenses:Relationship:Donate; 人情往来-慈善捐助',
        )
        return ParseRetCode.SUCCESS, result
