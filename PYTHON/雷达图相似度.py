import json

def compareSimilarity(dic1,dic2):
    total=0
    total=total+abs(dic1["1"]-dic2["1"])
    total=total+abs(dic1["2"]-dic2["2"])
    total=total+abs(dic1["3"]-dic2["3"])
    total=total+abs(dic1["4"]-dic2["4"])
    total=total+abs(dic1["5"]-dic2["5"])
    total=total+abs(dic1["6"]-dic2["6"])
    total=total+abs(dic1["7"]-dic2["7"])
    total=total+abs(dic1["8"]-dic2["8"])
    return total

if __name__ == '__main__':
    with open('D:/大二下/数据科学基础/master/JSON/不同类型得分排名.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    result_dic={}
    for item1 in json_data:
        result_dic[item1["id"]]=[]
        for item2 in json_data:
            if item2!=item1:
                result_dic[item1["id"]].append({"companion_id":item2["id"],"similarity":compareSimilarity(item1,item2)})
        list.sort(result_dic[item1["id"]],key=lambda x:x["similarity"])
    with open('D:/大二下/数据科学基础/master/JSON/雷达图匹配.json', 'a', encoding='utf8') as fp2:
        json.dump(result_dic, fp2, ensure_ascii=False)