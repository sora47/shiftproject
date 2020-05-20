from calendar import Calendar


# 指定した年月の月のカレンダー（日曜始まり）
def month_calendar(year, month):
    cl = Calendar(firstweekday=6)
    cllist = []
    for week in cl.monthdatescalendar(year, month):
        list = []
        for i in week:
            if (i.month == month):
                list.append(i.day)
            else:
                list.append('-')
        cllist.append(list)
    return cllist


# 登録されている募集日程
def shiftbase_list(cllist, model):
    modellist = []
    periodtimelist = []
    c = 0
    for i, data in enumerate(model):
        if i % 21 == 0:
            list = [cllist[c]]
            c += 1
        periodtimelist.append(data)
        if i % 7 == 6:
            list.append(periodtimelist)
            periodtimelist = []
        if i % 21 == 20:
            modellist.append(list)
    return modellist


# 現在の月と前月・次月の年月を含んだ辞書を返す
def prevnextmonth_dic(year, month):
    if month == 1:
        prevmonth = 12
        prevyear = year - 1
    else:
        prevmonth = month - 1
        prevyear = year
    if month == 12:
        nextmonth = 1
        nextyear = year + 1
    else:
        nextmonth = month + 1
        nextyear = year
    dic = {
        'month': month,
        'prevyear': prevyear,
        'prevmonth': prevmonth,
        'nextyear': nextyear,
        'nextmonth': nextmonth,
    }
    return dic
