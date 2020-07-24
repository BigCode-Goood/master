import numpy as np
import json
import matplotlib.pyplot as plt


def bit_product_sum(x, y):
    return sum([item[0] * item[1] for item in zip(x, y)])


def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    # method 2
    # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

    # method 3
    # dot_product, square_sum_x, square_sum_y = 0, 0, 0
    # for i in range(len(x)):
    #     dot_product += x[i] * y[i]
    #     square_sum_x += x[i] * x[i]
    #     square_sum_y += y[i] * y[i]
    # cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内


if __name__ == '__main__':
    #
    # f = open('D:/bigcode/master/JSON/余弦相似度匹配.json', encoding='utf-8')
    # res = f.read()
    # cp = json.loads(res)
    #
    # f = open('D:/bigcode/master/JSON/趋势分组+每日得分.json', encoding='utf-8')
    # res = f.read()
    # progress = json.loads(res)
    #
    # all_progress = {}
    # for trend in progress:
    #     all_progress.update(progress[trend])
    # print(all_progress)
    #
    # for user in cp:
    #     print(user)
    #     print(cp[user])
    #     progress1 = all_progress[user]
    #     progress2 = all_progress[cp[user]["best_similar_cp"]]
    #     progress3 = all_progress[cp[user]["best_different_cp"]]
    #
    #     length = max(len(progress1), len(progress2), len(progress3))
    #
    #     while len(progress1) < length:
    #         progress1.append(0)
    #     while len(progress2) < length:
    #         progress2.append(0)
    #     while len(progress3) < length:
    #         progress3.append(0)
    #
    #     days = [i for i in range(1, length + 1)]
    #     plt.plot(days, progress1, 'blue', label='user')
    #     plt.plot(days, progress2, 'red', label='match_cp')
    #     #     plt.plot(days, progress3, 'green', label='different_cp')
    #
    #     plt.title("user: " + user + "  cp: " + cp[user]["best_similar_cp"] + "  similarity=" + str(
    #         cp[user]['b_s_similarity'])[0:6], fontsize=12)
    #  #   plt.savefig('D:/bigcode/master/pics/余弦相似度-相似匹配图/' + user+ '.png')  # 保存图片
    #     plt.show()
    #
    # # 获得趋势分组+每日得分json
    # #
    # # f = open('D:/bigcode/master/JSON/personal_progress_data.json', encoding='utf-8')
    # # res = f.read()
    # # score_data = json.loads(res)
    # #
    # # all_trends={}
    # #
    # # for trend in trend_data:
    # #     all_trends[trend] = {}
    # #     user_list=trend_data[trend]
    # #     all_users_scores = {}
    # #     for u in user_list:
    # #         user={}
    # #         for s in score_data:
    # #             if s["user_id"]==str(u):
    # #                 user=s
    # #                 break
    # #         id=user["user_id"]
    # #         completion_list = []
    # #         for score in user["daily_progress"]:
    # #             completion_list.append(score["completion"])
    # #         all_users_scores[id]=completion_list
    # #     all_trends[trend]=all_users_scores
    # #
    # # print (all_trends)
    # # with open('D:/bigcode/master/JSON/趋势分组+每日得分.json', 'a', encoding='utf8') as fp1:
    # #     json.dump(all_trends, fp1, ensure_ascii=False)
    #
    #
    #
    # # 获得匹配cp的json
    #
    # f = open('D:/bigcode/master/JSON/趋势分组+每日得分.json', encoding='utf-8')
    # res = f.read()
    # trend_data = json.loads(res)
    #
    # f = open('D:/bigcode/master/JSON/个人均分.json', encoding='utf-8')
    # res = f.read()
    # user_average = json.loads(res)
    #
    # undo1 = {}
    # undo2 = {}
    #
    # match = {}
    #
    # # 同trend找相似
    # for trend in trend_data:
    #     # print("trend",trend)
    #     if len(trend_data[trend]) < 2:
    #         undo1.update(trend_data[trend])
    #     else:
    #         lst = trend_data[trend]
    #         #  print("lst",lst)
    #         for user in lst:
    #             max_sim = 0
    #             min_sim = 1
    #             best_cp = 0
    #             best_diff_cp = 0
    #             # print("user",user)
    #             for ano_user in lst:
    #                 # print("another",ano_user)
    #                 if user == ano_user: continue
    #                 progress1 = trend_data[trend][user]
    #                 progress2 = trend_data[trend][ano_user]
    #                 # print(progress1)
    #                 while len(progress1) < len(progress2):
    #                     progress1.append(0)
    #                 while len(progress2) < len(progress1):
    #                     progress2.append(0)
    #                 sim = cosine_similarity(progress1, progress2)
    #                 if sim > max_sim and user_average[ano_user]>50:
    #                     max_sim = sim
    #                     best_cp = ano_user
    #             if max_sim < 0.7:
    #                 undo1.update({user: trend_data[trend][user]})
    #             match[user] = {
    #                 "best_similar_cp": best_cp,
    #                 "b_s_similarity": max_sim,
    #                 "best_different_cp":0,
    #                 "b_d_similarity":1
    #             }
    # #  print(undo)
    # for user in undo1:
    #     print("user", user)
    #     max_sim = 0
    #     best_cp = 0
    #     for ano_user in undo1:
    #         print("another", ano_user)
    #         if user == ano_user: continue
    #         progress1 = undo1[user]
    #         progress2 = undo1[ano_user]
    #         print(progress1)
    #         while len(progress1) < len(progress2):
    #             progress1.append(0)
    #         while len(progress2) < len(progress1):
    #             progress2.append(0)
    #         sim = cosine_similarity(progress1, progress2)
    #         if sim > max_sim and user_average[ano_user]>50:
    #             max_sim = sim
    #             best_cp = ano_user
    #     # if max_sim < 0.6:
    #     #     undo.append(user)
    #     #     continue
    #     if match.get(user) is None:
    #         match[user] = {
    #             "best_similar_cp": best_cp,
    #             "b_s_similarity": max_sim,
    #             "best_different_cp": 0,
    #             "b_d_similarity": 1
    #         }
    #     else:
    #         if max_sim > match[user]["b_s_similarity"]:
    #             match[user]["best_similar_cp"] = best_cp
    #             match[user]["b_s_similarity"] = max_sim
    #
    # # 相反trend找不同
    # opps = {
    #     "上升": "下降",
    #     "下降": "上升",
    #     "上升-下降": "下降-上升",
    #     "下降-上升": "上升-下降",
    #     "波动": "波动"
    # }
    # for trend1 in trend_data:
    #     trend2 = opps[trend1]
    #     if len(trend_data[trend2]) <= 5:
    #         undo2.update(trend_data[trend1])
    #     else:
    #         lst1 = trend_data[trend1]
    #         lst2 = trend_data[trend2]
    #         #  print("lst",lst)
    #         for user in lst1:
    #             max_sim = 0
    #             min_sim = 1
    #             best_cp = 0
    #             best_diff_cp = 0
    #             # print("user",user)
    #             for ano_user in lst2:
    #                 # print("another",ano_user)
    #                 progress1 = trend_data[trend1][user]
    #                 progress2 = trend_data[trend2][ano_user]
    #                 # print(progress1)
    #                 length = max(len(progress1), len(progress2))
    #                 while len(progress1) < length:
    #                     progress1.append(0)
    #                 while len(progress2) < length:
    #                     progress2.append(0)
    #                 sim = cosine_similarity(progress1, progress2)
    #                 if sim < min_sim and user_average[ano_user]>50:
    #                     min_sim = sim
    #                     best_diff_cp = ano_user
    #             print("min:", min_sim)
    #             if min_sim > 0.2:
    #                 undo2.update({user: trend_data[trend1][user]})
    #             match[user].update({
    #                 "best_different_cp": best_diff_cp,
    #                 "b_d_similarity": min_sim
    #             })
    # for user in undo2:
    #     print("user", user)
    #     min_sim = 1
    #     best_diff_cp = 0
    #     for ano_user in undo2:
    #         print("another", ano_user)
    #         if user == ano_user: continue
    #         progress1 = undo2[user]
    #         progress2 = undo2[ano_user]
    #         length = max(len(progress1), len(progress2))
    #         while len(progress1) < length:
    #             progress1.append(0)
    #         while len(progress2) < length:
    #             progress2.append(0)
    #         sim = cosine_similarity(progress1, progress2)
    #         if sim < min_sim and user_average[ano_user]>50:
    #             min_sim = sim
    #             best_diff_cp = ano_user
    #
    #         if match.get(user) is None:
    #             match[user] = {
    #                 "best_different_cp": best_diff_cp,
    #                 "b_d_similarity": min_sim,
    #             }
    #         else:
    #             if min_sim < match[user]["b_d_similarity"]:
    #                 match[user]["best_different_cp"] = best_diff_cp
    #                 match[user]["b_d_similarity"] = min_sim
    # print(match)
    # # with open('D:/bigcode/master/JSON/余弦相似度匹配.json', 'a', encoding='utf8') as fp1:
    # #     json.dump(match, fp1, ensure_ascii=False)
    f = open('D:/bigcode/master/JSON/daily_progress.json', encoding='utf-8')
    res = f.read()
    user_progress = json.loads(res)

    couples={}

    for user in user_progress:
        companions=[]
        for cp in user_progress:
            if user==cp:continue

            progress1=user_progress[user]
            progress2=user_progress[cp]
            length = max(len(progress1), len(progress2))

            while len(progress1) < length:
                progress1.append(0)
            while len(progress2) < length:
                progress2.append(0)

            sim=cosine_similarity(progress1,progress2)
            companions.append({
                "companion_id":cp,
                "similarity":sim
            })
        couples[user]={"companions":companions}

    with open('D:/bigcode/master/JSON/余弦相似度匹配.json', 'a', encoding='utf8') as fp1:
        json.dump(couples, fp1, ensure_ascii=False)


