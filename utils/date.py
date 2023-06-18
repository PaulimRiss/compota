from datetime import datetime


def get_str_date():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d - %H:%M:%S")
    return dt_string
