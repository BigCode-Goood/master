import json

if __name__ == '__main__':
    f = open('personal_progress_data.json', encoding='utf-8')
    res = f.read()
    pp_data = json.loads(res)

    item_i = 0
    for item in pp_data:
        daily_p_list = item["daily_progress"]
        pre_month = int(daily_p_list[0]["date"][0:2])
        pre_date = int(daily_p_list[0]["date"][3:])
        index = a = 0

        while index < len(daily_p_list):
            month = int(daily_p_list[index]["date"][0:2])
            date = int(daily_p_list[index]["date"][3:])
            if month == pre_month and date != (pre_date + 1):
                for i in range(pre_date + 1, date):
                    a += 1
                    d = ('0' + str(i)) if i < 10 else str(i)
                    insert_data = {"date": "0" + str(month) + "-" + d, "completion": 0}
                    pp_data[item_i]["daily_progress"].insert(index, insert_data)
                    index += 1
            elif month == (pre_month + 1) and pre_date == 29 and date != 1:
                for i in range(1, date):
                    a += 1
                    d = ('0' + str(i)) if i < 10 else str(i)
                    insert_data = {"date": "03-" + d, "completion": 0}
                    pp_data[item_i]["daily_progress"].insert(index, insert_data)
                    index += 1
            elif month == (pre_month + 1) and pre_date != 29 and date == 1:
                for i in range(pre_date + 1, 30):
                    a += 1
                    d = ('0' + str(i)) if i < 10 else str(i)
                    insert_data = {"date": "02-" + d, "completion": 0}
                    pp_data[item_i]["daily_progress"].insert(index, insert_data)
                    index += 1
            elif month == (pre_month + 1) and pre_date != 29 and date != 1:
                for i in range(pre_date + 1, 30):
                    a += 1
                    d = ('0' + str(i)) if i < 10 else str(i)
                    insert_data = {"date": "02-" + d, "completion": 0}
                    pp_data[item_i]["daily_progress"].insert(index, insert_data)
                    index += 1
                for i in range(1, date):
                    a += 1
                    d = ('0' + str(i)) if i < 10 else str(i)
                    insert_data = {"date": "03-" + d, "completion": 0}
                    pp_data[item_i]["daily_progress"].insert(index, insert_data)
                    index += 1
            index += 1
            pre_date = date
            pre_month = month
        item_i += 1
print(pp_data)
ppdJsonwith0 = json.dumps(pp_data, ensure_ascii=False)
with open("personal_progress_data000.json", "w") as fp:
    fp.write(ppdJsonwith0)
