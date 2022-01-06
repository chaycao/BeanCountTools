import xlsxwriter as xlsxwriter

from beancount.tools.common.constants.account_constant import ALL_ACCOUNT


def write_standard_excel_record(filename, success_records, fail_records, skip_records):
    workbook = xlsxwriter.Workbook(filename)
    success_sheet = workbook.add_worksheet('success')
    fail_sheet = workbook.add_worksheet('fail')
    skip_sheet = workbook.add_worksheet('skip')
    meta_sheet = workbook.add_worksheet('meta')

    write_standard_excel_record_in_sheet(success_sheet, success_records)
    write_standard_excel_record_in_sheet(fail_sheet, fail_records)
    write_standard_excel_record_in_sheet(skip_sheet, skip_records)

    write_standard_excel_meta_data(meta_sheet)

    set_account_validation(success_sheet, success_records)
    set_account_validation(fail_sheet, fail_records)
    set_account_validation(skip_sheet, skip_records)

    workbook.close()


def set_column_width(column_num, column_width, sheet):
    for i in range(0, column_num):
        if column_width[i] < 40:
            sheet.set_column(i, i, (column_width[i] * 1.25))
        else:
            sheet.set_column(i, i, 40)
    sheet.set_column(0, 0, 30)
    sheet.set_column(1, 1, 30)


def set_account_validation(sheet, records):
    row_num = len(records)
    for i in range(1, row_num + 1):
        validate = {'validate': 'list', 'source': '=meta!$A$1:$A$' + str(len(ALL_ACCOUNT))}
        sheet.data_validation('A' + str(i + 1), validate)
        sheet.data_validation('B' + str(i + 1), validate)


def write_standard_excel_record_in_sheet(sheet, records):
    if not records:
        return
    row_num = len(records)
    keys = list(records[0].__dict__.keys())
    column_num = len(keys)
    column_width = []
    for i in range(0, row_num + 1):
        for j in range(0, column_num):
            if i == 0:
                # header
                sheet.write(i, j, keys[j])
                column_width.append(10)
                continue
            key = keys[j]
            index = i - 1
            content = getattr(records[index], key)
            if not content:
                continue
            column_width[j] = max([column_width[j], len(content)])
            sheet.write(i, j, content)
    set_column_width(column_num, column_width, sheet)


def write_standard_excel_meta_data(sheet):
    for i in range(0, len(ALL_ACCOUNT)):
        sheet.write(i, 0, ALL_ACCOUNT[i])


def write_bean_record(filename, bean_records):
    with open(filename, 'w') as file:
        for bean_record in bean_records:
            file.write(str(bean_record))
