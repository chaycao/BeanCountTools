from beancount.alipay.constants import SkipPartner
from beancount.common.constants.account_constant import SKIP_ACCOUNT
from beancount.common.constants.common_constant import FinalRetCode, ParseRetCode, PN
from beancount.common.parser import Parser


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

    def _parse_yuebao(self, record):
        if self._is_yuebao_income(record):
            return self._parse_yuebao_income(record)
        return ParseRetCode.FAIL, None

    def _parse_transfer(self, record):
        # 给黄梅的转账可以直接跳过，不计入（需要注意会不会有账户名同名情况的转账，目前没有）
        if record.partner in SkipPartner:
            return ParseRetCode.SKIP, self.parse_to_excel_record_without_classify(record)
        # todo 其他转账如何处理
        return ParseRetCode.FAIL, None

    def _parse_yuebao_income(self, record):
        result = self.parse_to_excel_record_with_classify(
            record,
            out_account='Income:Financial:YuEbao; 金融-余额宝',
            in_account='Assets:Home:Balance; 结余',
        )
        return ParseRetCode.SUCCESS, result

    def _is_yuebao_income(self, record):
        return record.product_name.startswith('余额宝') and record.product_name.endswith('收益发放')
