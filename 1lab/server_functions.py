import os
import json
import pandas as pd
import csv
from io import StringIO


def init():
    os.makedirs("CSV_FOLDER", exist_ok=True)


def json_handler():
    d = dict()
    for i in os.listdir("CSV_FOLDER"):
        d.update({i[:-4]: list(pd.read_csv("CSV_FOLDER/" + i).columns)})
    return json.dumps(d, indent=4, sort_keys=True)


# return (успех/провал, файл csv)

# прислали строку s где нет select:
def select_handler(s):

    # разделим на select clause и from clause
    ind = max(s.find("from"), s.find("FROM"))
    ind2 = max(s.find("where"), s.find("WHERE"))
    if ind == -1:
        return ("From clause is missing.", None)
    s1 = s[:ind].replace("\n", " ").split(",")
    s2 = s[ind:ind2].split()
    # теперь обозначим название таблицы из from:
    try:
        table_name = s2[-1]
        file_name = s2[1]
    except:
        return ("From clause is missing.", None)
    # название получено, загружаем представление таблицы в p
    try:
        p = pd.read_csv("CSV_FOLDER/" + file_name + ".csv")
    except:
        return ("File doesn't exist.", None)

    # from обработан, переходим к where
    crit = lambda a: a
    if ind2 > -1:
        # обработаем тело where
        s3 = s[ind2:][5:].replace(" ", "")
        if (s3.find("!=") == -1) and (s3.find(">=") == -1) and (s3.find("<=") == -1):
            s3.replace("=", "==")
        statement = s3
        # преобразуем p под критерий where
        print(statement)
        try:
            p = p.query(statement)
        except:
            return ("Incorrect where statement.", None)

    # теперь обработаем select clause:
    if s1[0][0] == "*":
        return ("Success.", p.to_csv())
    columns = []
    for i in s1:
        columns.append(i.split()[0])
    return ("Success.", p[columns].to_csv())


# Название|Файл
# delimiter = ','
def csv_handler(s):
    name, body = s.split("|")
    pd.read_csv(StringIO(body)).to_csv("CSV_FOLDER/" + name + ".csv")


# s - полная строчка запроса.
def client_handler(s):
    # print(s)
    # есть всего 3 ситуации:
    # s = JSON_IT <=> JSON_IT - вывод json файла с названиям таблиц и их столбцами
    # s = SELECT ... <=> select-запрос
    # s = Название|Файл <=> запись csv файла
    if len(s) >= 6:
        check = max(s.find("select"), s.find("SELECT"))
        if check > -1:
            return select_handler(s[check + 6 :])
    if len(s) >= 7 and s[:7] == "JSON_IT":
        return ("Success.", json_handler())
    else:
        csv_handler(s)
        return ("Success.", None)
