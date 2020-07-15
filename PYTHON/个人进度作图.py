import matplotlib.pyplot as plt
import json

if __name__ == '__main__':
    f = open('personal_progress_data.json', encoding='utf-8')
    res = f.read()
    user_data = json.loads(res)

    period = []
    dataC = []

    user = user_data[2]
    dailyP = user['daily_progress']
    cnt = 0  # 几天为一个period
    p = 1
    period_comp = 0
    for item in dailyP:
        if cnt == 1:
            period.append(p)
            dataC.append(period_comp)
            period_comp = 0
            cnt = 0
            p += 1
        period_comp += item['completion']
        cnt += 1
    if cnt != 0:
        period.append(p)
        dataC.append(period_comp)

    print(period)
    print(dataC)

    plt.plot(period, dataC)
    plt.title("userId: " + user['user_id'], fontsize=20)
    plt.xlabel("period", fontsize=12)
    plt.ylabel("completion", fontsize=12)
    plt.tick_params(axis='both', labelsize=10)
    # plt.savefig(user['user_id'] + '.png') # 保存图片
    plt.show()
