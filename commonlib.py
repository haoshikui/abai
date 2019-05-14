#!/usr/bin/python
# -*- coding: UTF-8 -*-


def date_convert(offset):
    # date函数用来将星上时转换为北京时 // REV4.1新增
    day_flag = 0; #偏移天数初始值为0，调试时刻设置为其他值
    DayInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # 月份天数库，默认为平年
    #定义初始时间
    year = 2009
    month = 1
    day = 1
    hour = 0
    minute = 0
    second = 0
    second = int(offset % 60)
    minute = int((offset % 3600) / 60)
    hour = int((offset / 3600) % 24)
    day_flag = int(offset / 3600 / 24)
    #星上时超过一天，进行年月日的计算
    while (day_flag > 0):
        #首先判断是否为闰年，根据判断修改月份天数库
        if ((year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)):
            DayInMonth[1] = 29
        else:
            DayInMonth[1] = 28
        #累加天数，得到日、月、年
        day +=1
        if (day > DayInMonth[(month - 1)]):
            day = 1
            month += 1
        if (month > 12):
            month = 1
            year += 1
        day_flag -=1
    if month<10:
        monthstr = '0'+ str(month)
    else:
        monthstr = str(month)

    if day<10:
        daystr = '0'+ str(day)
    else:
        daystr = str(day)

    if hour<10:
        hourstr = '0'+ str(hour)
    else:
        hourstr = str(hour)

    if minute<10:
        minutestr = '0'+ str(minute)
    else:
        minutestr = str(minute)

    if second<10:
        secondstr = '0'+ str(second)
    else:
        secondstr = str(second)

    time_str = str(year)+"-"+monthstr+"-"+daystr+" "+hourstr+":"+minutestr+":"+secondstr
    return time_str
