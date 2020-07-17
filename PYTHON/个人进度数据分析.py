import json
import time

if __name__ == '__main__':
    f = open('code_length.json', encoding='utf-8')
    res = f.read()
    user_data = json.loads(res)

    f2 = open('题目难度.json', encoding='utf-8')
    res2 = f2.read()
    case_dfct = json.loads(res2)

    total_personal_progress = []  # 最终所有结果放这里
    for users in user_data:
        personal_progress = {}
        personal_progress['user_id'] = users['user_id']
        dailyData = []
        cases = users['casses']
        casesSortList = sorted(cases, key=lambda x: x['datetime'], reverse=False)
        today = ""
        dailyC = 0
        for case in casesSortList:
            ts = str(case['datetime'])[0:10]  # 获取13位时间戳
            caseDate = time.strftime("%m-%d", time.localtime(int(ts)))
            if caseDate == today:
                # 继续往dailyC上累加
                dailyC += (case['final_score'] * case_dfct[case['case_id']])
            else:
                if today!="":
                    dailyData_item = {}
                    dailyData_item['date'] = today
                    dailyData_item['completion'] = dailyC
                    dailyData.append(dailyData_item)
                # --------开始新的一天-------------
                dailyC = 0
                today = caseDate
                dailyC += (case['final_score'] * case_dfct[case['case_id']])

        dailyData_item = {}
        dailyData_item['date'] = today
        dailyData_item['completion'] = dailyC
        dailyData.append(dailyData_item)
        personal_progress['daily_progress'] = dailyData

        total_personal_progress.append(personal_progress)

    print(total_personal_progress)
    print(len(total_personal_progress))

    ppdJson=json.dumps(total_personal_progress, ensure_ascii=False)
    with open("personal_progress_data.json", "w") as fp:
        fp.write(ppdJson)

