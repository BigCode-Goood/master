import json

f = open('D:/bigcode/master/JSON/得分趋势拟合信息.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
up=[]
down=[]
up_down=[]
down_up=[]
wave=[]

if __name__ == '__main__':
    for user_id in data:
        trend=data[user_id]["趋势"]
        if trend=="上升":up.append(user_id)
        elif trend=="下降":down.append(user_id)
        elif trend=="上升-下降":up_down.append(user_id)
        elif trend=="下降-上升":down_up.append(user_id)
        elif trend=="波动":wave.append(user_id)
    print(wave)
    dic={
        "上升":up,
        "下降":down,
        "上升-下降":up_down,
        "下降-上升":down_up,
        "波动":wave
    }
    # with open('D:/bigcode/master/JSON/趋势分组.json', 'a', encoding='utf8') as fp1:
    #     json.dump(dic, fp1, ensure_ascii=False)
