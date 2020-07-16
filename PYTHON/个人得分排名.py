import json

score_0 = []
score_1 = []
score_2 = []
score_3 = []
score_4 = []
score_5 = []
score_6 = []
score_7 = []
dic_rate = []
with open('D:/大二下/数据科学基础/master/JSON/code_length_2.0.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)
    dic_score = []
    for item in json_data:
        person_id = item['user_id']
        dic_person = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, "id": person_id}
        for i in item['casses']:
            dic_person[i['case_type']] = dic_person[i['case_type']] + i['final_score']
        score_0.append(dic_person[1])
        score_1.append(dic_person[2])
        score_2.append(dic_person[3])
        score_3.append(dic_person[4])
        score_4.append(dic_person[5])
        score_5.append(dic_person[6])
        score_6.append(dic_person[7])
        score_7.append(dic_person[8])
        dic_score.append(dic_person)
score_0 = list(set(score_0))
score_0.sort()
score_1 = list(set(score_1))
score_1.sort()
score_2 = list(set(score_2))
score_2.sort()
score_3 = list(set(score_3))
score_3.sort()
score_4 = list(set(score_4))
score_4.sort()
score_5 = list(set(score_5))
score_5.sort()
score_6 = list(set(score_6))
score_6.sort()
score_7 = list(set(score_7))
score_7.sort()
for item in dic_score:
    dic_person_rate = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, "id": item["id"]}
    dic_person_rate[1] = float((score_0.index(item[1]) + 1) / len(score_0))
    dic_person_rate[2] = float((score_1.index(item[2]) + 1) / len(score_1))
    dic_person_rate[3] = float((score_2.index(item[3]) + 1) / len(score_2))
    dic_person_rate[4] = float((score_3.index(item[4]) + 1) / len(score_3))
    dic_person_rate[5] = float((score_4.index(item[5]) + 1) / len(score_4))
    dic_person_rate[6] = float((score_5.index(item[6]) + 1) / len(score_5))
    dic_person_rate[7] = float((score_6.index(item[7]) + 1) / len(score_6))
    dic_person_rate[8] = float((score_7.index(item[8]) + 1) / len(score_7))
    dic_rate.append(dic_person_rate)
with open('D:/大二下/数据科学基础/master/JSON/不同类型得分排名.json', 'a', encoding='utf8') as fp1:
    json.dump(dic_rate, fp1, ensure_ascii=False)
