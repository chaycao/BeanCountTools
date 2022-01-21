from beancount.common.constants.common_constant import FinalRetCode, ParseRetCode
from beancount.common.parser import Parser
from beancount.wechat.constants import SkipPartner


class WeChatParser(Parser):

    def parse_to_excel_record(self, record):
        """
        :param record: alipay格式record
        :return: 标准格式record
        """
        # 解析 转账
        retcode, result = self._parse_transfer(record)
        if retcode in FinalRetCode:
            return retcode, result
        # todo chay.cao 解析其他类型

        # 解析失败转成未标记分类的excel格式
        result = self.parse_to_excel_record_without_classify(record)
        return retcode.FAIL, result

    def _parse_transfer(self, record):
        # 给黄梅的转账可以直接跳过，不计入（需要注意会不会有账户名同名情况的转账，目前没有）
        if record.partner in SkipPartner:
            return ParseRetCode.SKIP, self.parse_to_excel_record_without_classify(record)
        # todo 其他转账如何处理
        return ParseRetCode.FAIL, None

