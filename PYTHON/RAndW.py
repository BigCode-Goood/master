# 读取json文件并且写入
import json

with open('D:/bigcode/master/JSON/personal_progress_data.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)
    dic_score={}
    for i in range(len(json_data)):
        sum=0
        user_data=json_data[i]
        user_id=user_data["user_id"]
        daily_progress=user_data["daily_progress"]
        for d in daily_progress:
            sum+=d["completion"]
        dic_score[user_id]=sum/200
print(dic_score)
with open('D:/bigcode/master/JSON/个人均分.json','a',encoding='utf8') as fp1:
    json.dump(dic_score,fp1,ensure_ascii=False)
