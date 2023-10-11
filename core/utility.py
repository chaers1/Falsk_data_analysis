import time
from datetime import datetime


class Utility:
    @classmethod
    def get_cur_time(cls):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


'''字符串转日期格式'''


def parse_date_string(date_str, format='%Y-%m-%d'):
    date_obj = datetime.strptime(date_str, format)
    return date_obj
