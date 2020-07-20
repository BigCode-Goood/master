import json
import numpy as np
import matplotlib.pyplot as plt


def dtw_distance(ts_a, ts_b, d=lambda x, y: abs(x - y), mww=10000):
    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))

    # Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
        cost[i, 0] = cost[i - 1, 0] + d(ts_a[i], ts_b[0])

    for j in range(1, N):
        cost[0, j] = cost[0, j - 1] + d(ts_a[0], ts_b[j])

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i - mww), min(N, i + mww)):
            choices = cost[i - 1, j - 1], cost[i, j - 1], cost[i - 1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])

    # Return DTW distance given window
    return cost[-1, -1]


def cutZero(array):
    i = 0
    while array[i] == 0 & i < len(array) - 1:
        i = i + 1
    j = len(array) - 1
    while array[j] == 0 & j >= 1:
        j = j - 1
    return array[i:j + 1]


result_dic = {}
with open('D:/大二下/数据科学基础/master/JSON/personal_progress_data.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)
    for item1 in json_data:  # 遍历比较
        similarity = float('inf')
        array1 = []
        for progress1 in item1["daily_progress"]:
            array1.append(progress1["completion"])
        array1 = cutZero(array1)
        for item2 in json_data:
            if item1 != item2:
                array2 = []
                for progress2 in item2["daily_progress"]:
                    array2.append(progress2["completion"])
                array2 = cutZero(array2)  # 去掉头尾的0
                simi = dtw_distance(array1, array2)
                if simi < similarity:
                    companion_id = item2["user_id"]
                    similarity = simi
        result_dic[item1["user_id"]] = {"BestCompanion": companion_id, "DTW_similarity": similarity}
with open('D:/大二下/数据科学基础/master/JSON/DTWsimilarity.json', 'a', encoding='utf8') as fp2:
    json.dump(result_dic, fp2, ensure_ascii=False)
for item in json_data:
    array_progress = []
    for progress in item["daily_progress"]:
        array_progress.append(progress["completion"])
    array_progress1 = []
    for temp in json_data:
        if temp["user_id"] == result_dic[item["user_id"]]["BestCompanion"]:
            for progress in temp["daily_progress"]:
                array_progress1.append(progress["completion"])
            break
    time1 = range(0, len(array_progress))
    time2 = range(0, len(array_progress1))
    plt.plot(time1, array_progress, label='原学生')
    plt.plot(time2, array_progress1, label='匹配学生')
    plt.xlabel("period", fontsize=12)
    plt.ylabel("completion", fontsize=12)
    plt.tick_params(axis='both', labelsize=10)
    plt.savefig('D:/大二下/数据科学基础/master/pics/DTW匹配图/' + item['user_id'] + '.png')