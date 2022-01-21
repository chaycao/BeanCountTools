from beancount.alipay.record import BeanRecordTransaction, BeanRecord
from beancount.common.constants.common_constant import PN


def standard_excel_record_to_bean_record(standard_excel_record):
    out_t = BeanRecordTransaction(
        standard_excel_record.out_account,
        standard_excel_record.fee,
        PN.N
    )
    in_t = BeanRecordTransaction(
        standard_excel_record.in_account,
        standard_excel_record.fee,
        PN.P
    )
    bean_record = BeanRecord(
        standard_excel_record.ctime, [out_t, in_t],
        standard_excel_record.partner, standard_excel_record.remark)
    return bean_record