# pip install ipython-beautifulsoup

import requests
import re
from bs4 import BeautifulSoup

month_days = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def if_leap_year(ayear):
    if (ayear % 4) == 0:
        if (year % 100) == 0 and (ayear % 400) != 0:
            month_days[2] = 28
            return 0
        month_days[2] = 29
        return 1

    month_days[2] = 28
    return 0


# Получение исходного кода производственного календаря
calendar_url = "http://www.garant.ru/calendar/buhpravo/"
page = requests.get(calendar_url)
soup = BeautifulSoup(page.text)

# получить год календаря
meta_title = soup.find("meta", {"property": "og:title"})
year = int(re.findall(r'\d+', meta_title["content"])[0])
print("год %d\n" % year)

# проверка года на високосность
print("проверка года на високосность %d\n" % (if_leap_year(year)))

# Получение только необходимого куска кода
code_content = soup.find('div', {'class': 'page-content'})

# Получение всех тегов таблиц
code_table = code_content.findAll('table', {'class': 'tabCalendar'})
num_table = 0
num_tr = 0
num_td = 0
last_date = 0
arr = {}
month_num = 1
month_min = 1
month_num_count = 3
day_arr = 0

for table in code_table:

    if (num_table + 2) % 2 == 0:

        print("таблица %d\n" % num_table)
        code_tr = table.findAll('tr')

        for tr in code_tr:

            print("строка %d\n" % num_tr)

            if num_tr == 0:
                print("пропуск строки %d\n" % num_tr)
                num_tr += 1
                continue
            code_td = tr.findAll('td')

            for td in code_td:

                if_holiday = False

                td_text = td.text.strip()
                td_clean_text = td_text.replace("*", "").replace("'", "")

                if td_text != "":

                    day_arr = 0

                    if num_td == 0:
                        print("пропуск столбца %d / %s" % (num_td, td_text))
                        num_td += 1
                        continue

                    if "/" in td_clean_text:
                        day_arr = 1
                        daya = list(map(int, td_clean_text.split('/')))
                        day = daya[0]
                    else:
                        day = int(td_clean_text)

                    if day < last_date:
                        month_num += 1
                        if month_num > month_num_count:
                            month_num = month_min
                        print()

                    print("month_num %d" % month_num)
                    print("td.text.strip() %s" % td_text)

                    if len(arr) < month_num:
                        arr[month_num] = {}

                    if 'workday' not in arr[month_num].keys():
                        print("not workday in %d" % month_num)
                        arr[month_num]['workday'] = []

                    if 'deworkday' not in arr[month_num].keys():
                        print("not deworkday in %d" % month_num)
                        arr[month_num]['deworkday'] = []

                    if 'shortday' not in arr[month_num].keys():
                        print("not shortday in %d" % month_num)
                        arr[month_num]['shortday'] = []

                    if 'holiday' not in arr[month_num].keys():
                        print("not holiday in %d" % month_num)
                        arr[month_num]['holiday'] = []

                    # проверка даты на выходной день
                    if_holiday = td.find('span')

                    if td.has_attr('style'):
                        if "color: rgb(255, 0, 0)" in td['style']:
                            if_holiday = True

                    # Сортируем дни на выходные, праздничные, сокращенные и рабочие
                    if "'" in td_text:
                        print("deworkday %d" % day)

                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[month_num]['deworkday'].append(t)
                        else:
                            arr[month_num]['deworkday'].append(day)

                        arr[month_num]['deworkday'].sort()

                    elif "*" in td_text:
                        # print("is_short")
                        print("shortday %d" % day)
                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[month_num]['shortday'].append(t)
                        else:
                            arr[month_num]['shortday'].append(day)

                        arr[month_num]['shortday'].sort()

                    elif if_holiday:
                        # print("is_holiday")
                        # print(arr)
                        print("holiday %d" % day)
                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[month_num]['holiday'].append(t)
                        else:
                            arr[month_num]['holiday'].append(day)

                        arr[month_num]['holiday'].sort()

                    elif tr.has_attr('class'):
                        if tr['class'][0] == 'redDay':  # Notice that I put [0], as para['class'] is a list.
                            # print("is_holiday")
                            print("holiday %d" % day)
                            if day_arr == 1:
                                for t in range(len(daya)):
                                    arr[month_num]['holiday'].append(t)
                            else:
                                arr[month_num]['holiday'].append(day)

                            arr[month_num]['holiday'].sort()

                    else:
                        print("work day %d" % day)
                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[month_num]['workday'].append(t)
                        else:
                            arr[month_num]['workday'].append(day)

                        arr[month_num]['workday'].sort()

                    print(arr)

                    last_date = day
                    num_td += 1

            num_tr += 1
            num_td = 0

            # Здесь считать часы

            # quarter

            print("--- коней строки ---")
            print()

        num_tr = 0
        # break

        month_min = month_min + month_num_count
        month_num = month_min
        # month_min = 1
        # month_num_count = 3

    num_table += 1

for u in range(1, len(arr) + 1):
    print(u)
    arr[u]['calendar_days'] = month_days[u]
    arr[u]['work_40'] = round(len(arr[u]['workday']) * 8 + len(arr[u]['shortday']) * 7, 1)
    arr[u]['work_39'] = round(len(arr[u]['workday']) * 7.8 + len(arr[u]['shortday']) * 6.8, 1)
    arr[u]['work_36'] = round(len(arr[u]['workday']) * 7.2 + len(arr[u]['shortday']) * 6.2, 1)
    arr[u]['work_24'] = round(len(arr[u]['workday']) * 4.8 + len(arr[u]['shortday']) * 3.8, 1)

print(arr)
