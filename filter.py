def format_datetime2(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)


def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    g_list = list(value)
    f_year = g_list[0:4]
    f_month = g_list[4:6]
    f_date = g_list[6:8]
    f_hour = g_list[8:10]
    f_minute = g_list[10:12]

    f_year = ''.join(f_year)
    f_month = ''.join(f_month)
    f_date = ''.join(f_date)
    f_hour = ''.join(f_hour)
    f_minute = ''.join(f_minute)

    return f_year + "년 " + f_month + "월 " + f_date + "일 " + f_hour + "시 " + f_minute + "분"
