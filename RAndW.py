#读取json文件并且写入
import json

with open('D:/大二下/数据科学基础/test_data.json','r',encoding='utf8') as fp:
    json_data=json.load(fp)
    dic_avg={}
    dic_type={}
    dic_type_temp={}
    for item in json_data.items():
        average=0
        for i in item[1]['cases']:
            average=average+i['final_score']
            if dic_type_temp.__contains__(i['case_type']):
                dic_type_temp[i['case_type']]['num']=dic_type_temp[i['case_type']]['num']+1
                dic_type_temp[i['case_type']]['total']=dic_type_temp[i['case_type']]['total']+i['final_score']
            else:
                dic_type_temp[i['case_type']]={}
                dic_type_temp[i['case_type']]['type']=i['case_type']
                dic_type_temp[i['case_type']]['num']=1
                dic_type_temp[i['case_type']]['total']=i['final_score']
        dic_avg[str(item[0])]=float(average/200)
    # with open('D:/大二下/数据科学基础/个人均分.json','a',encoding='utf8') as fp1:
    #     json.dump(dic_avg,fp1,ensure_ascii=False)
    for item in dic_type_temp:
        temp=dic_type_temp[item]
        dic_type[temp['type']]={'average':float(temp['total']/temp['num'])}
    # with open ('D:/大二下/数据科学基础/题型均分.json','a',encoding='utf8') as fp2:
    #     json.dump(dic_type,fp2,ensure_ascii=False)
