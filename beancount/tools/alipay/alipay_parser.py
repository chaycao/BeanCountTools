from beancount.tools.alipay.record import BeanRecord, BeanRecordTransaction, StandardExcelRecord
from beancount.tools.common.constants.account_constant import SKIP_ACCOUNT
from beancount.tools.common.constants.common_constant import FinalRetCode, ParseRetCode, SkipPartner, PN
from beancount.tools.common.parser import Parser


class AliPayParser(Parser):

    def parse_to_excel_record(self, record):
        """
        :param record: alipay格式record
        :return: 标准格式record
        """
        # 解析 转账
        retcode, result = self._parse_transfer(record)
        if retcode in FinalRetCode:
            return retcode, result
        # 解析 余额宝
        retcode, result = self._parse_yuebao(record)
        if retcode in FinalRetCode:
            return retcode, result
        # todo chay.cao 解析其他类型

        # 解析失败转成未标记分类的excel格式
        result = self.parse_to_excel_record_without_classify(record)
        return retcode.FAIL, result

    def parse_to_excel_record_with_classify(self, record, out_account, in_account):
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

    def _parse_yuebao(self, record):
        if self._is_yuebao_income(record):
            return self._parse_yuebao_income(record)
        return ParseRetCode.FAIL, None

    def _parse_transfer(self, record):
        # 给黄梅的转账可以直接跳过，不计入（需要注意会不会有账户名同名情况的转账，目前没有）
        if record.partner in SkipPartner:
            return ParseRetCode.SKIP, None
        # todo 其他转账如何处理
        return ParseRetCode.FAIL, None

    def _parse_yuebao_income(self, record):
        result = self.parse_to_excel_record_with_classify(
            record,
            out_account='Income:Financial:YuEbao',
            in_account='Assets:Home:Balance',
        )
        return ParseRetCode.SUCCESS, result

    def _is_yuebao_income(self, record):
        return record.product_name.startswith('余额宝') and record.product_name.endswith('收益发放')

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

            date = row[3].value
            fee = row[4].value
            partner = row[8].value
            remark = row[10].value

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


'''
需要删除，供 StandardExcelRecord 转 BeanRecord 参考 
income_t = BeanRecordTransaction(
    'Income:Financial:YuEbao',
    record.fee,
    PN.N
)
assets_t = BeanRecordTransaction(
    'Assets:Home:Balance',
    record.fee,
    PN.P
)
transactions = [income_t, assets_t]
standard_record = BeanRecord(record.ctime, transactions, record.partner, record.remark)
return ParseRetCode.SUCCESS, standard_record
'''
