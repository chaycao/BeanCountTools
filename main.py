#!/usr/bin/python
# _*_ coding:utf-8 _*_
import sys
from beancount.alipay import alipay_main
from beancount.wechat import wechat_main

if __name__ == "__main__":
    """
    python model func in_filename
    
    python main.py alipay excel tmp/alipay/chaycao_alipay_record_202109.csv
    python main.py alipay bean tmp/alipay/chaycao_alipay_record_202109_standard.xlsx
    
    python main.py wechat excel tmp/wechat/chaycao_202109.csv
    python main.py wechat bean tmp/wechat/chaycao_202109_standard.xlsx
    
    python main.py alipay excel tmp/alipay/huang_alipay_record_202109.csv
    python main.py alipay bean tmp/alipay/huang_alipay_record_202109_standard.xlsx
    
    python main.py wechat excel tmp/wechat/huang_202109.csv
    python main.py wechat bean tmp/wechat/huang_202109_standard.xlsx
    
    """
    model = sys.argv[1]
    cmd = sys.argv[2]
    in_filename = sys.argv[3]

    main = None
    if model == 'alipay':
        main = alipay_main
    elif model == 'wechat':
        main = wechat_main

    if cmd == 'excel':
        main.parse_to_excel(in_filename)
    if cmd == 'bean':
        main.parse_to_bean(in_filename)

    # if model == 'alipay':
    #     if cmd == 'excel':
    #         in_filename = sys.argv[2]
    #         alipay_main.parse_to_excel(in_filename)
    #     if cmd == 'bean':
    #         in_filename = sys.argv[2]
    #         alipay_main.parse_to_bean(in_filename)
    # elif model == 'wechat':
    #     if cmd == 'excel':
    #         in_filename = sys.argv[2]
    #         wechat_main.parse_to_excel(in_filename)
    #     if cmd == 'bean':
    #         in_filename = sys.argv[2]
    #         wechat_main.parse_to_bean(in_filename)
