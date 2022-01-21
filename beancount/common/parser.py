from beancount.alipay.record import BeanRecordTransaction, BeanRecord, StandardExcelRecord
from beancount.common.constants.account_constant import SKIP_ACCOUNT
from beancount.common.constants.common_constant import PN


class Parser(object):
    def parse_to_excel_record(self, record):
        raise NotImplementedError

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
