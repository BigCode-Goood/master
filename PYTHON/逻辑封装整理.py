import json
import matplotlib.pyplot as plt
import numpy as np

# 直接在这里改自己的文件位置
location = {
    "zjy": "D:/大二下/数据科学基础/master/JSON/",
    "wyq": "I:/BigCode2/aster/JSON/",
    "fbj": "D:/bigcode/master/JSON/"
}

my_location = location["zjy"]


# 数据解析器类
# 初始化时读取需要的所有文件并将解析后的json字符串存入
class DataPaser:
    code_length_data = []
    #    personal_progress_data = {}
    daily_completion_data = {}
    fit_func_data = {}
    user_average = {}
    couples0 = {}  # 求导差匹配
    couples1 = {}  # 余弦相似度匹配
    couples2 = {}  # DTW匹配
    couples3 = {}  # 雷达图匹配
    couples = []

    def __init__(self):
        f1 = open(my_location + 'code_length_2.0.json', encoding='utf-8')
        self.code_length_data = json.loads(f1.read())
        f2 = open(my_location + 'personal_progress_data.json', encoding='utf-8')
        self.personal_progress_data = json.loads(f2.read())
        f3 = open(my_location + '得分趋势拟合信息.json', encoding='utf-8')
        self.fit_func_data = json.loads(f3.read())

        f4_0 = open(my_location + '求导差相似度2.0.json', encoding='utf-8')
        self.couples0 = json.loads(f4_0.read())
        f4_1 = open(my_location + '余弦相似度匹配.json', encoding='utf-8')
        self.couples1 = json.loads(f4_1.read())
        f4_2 = open(my_location + 'DTWsimilarity.json', encoding='utf-8')
        self.couples2 = json.loads(f4_2.read())
        f4_3 = open(my_location + '雷达图匹配.json', encoding='utf-8')
        self.couples3 = json.loads(f4_3.read())

        f5 = open(my_location + 'daily_progress.json', encoding='utf-8')
        self.daily_completion_data = json.loads(f5.read())

        f6 = open(my_location + '个人均分.json', encoding='utf-8')
        self.user_average = json.loads(f6.read())

        self.couples.append(self.couples0)
        self.couples.append(self.couples1)
        self.couples.append(self.couples2)
        self.couples.append(self.couples3)

    # 根据user_id获取用户所有提交数据，由于当初存数据考虑不周，如今查询只能遍历QAQ
    # def getDetailedData(self, id):
    #     for item in self.code_length_data:
    #         if int(item["user_id"]) == id:
    #             return item

    # 根据user_id获取用户每日完成度数据
    def getPersonalProgressData(self, id):
        return self.daily_completion_data[str(id)]

    def getFitFuncData(self, id):
        return self.fit_func_data[str(id)]

    def getCouples(self, id, match_func):
        return self.couples[match_func][str(id)]["companions"]


# 趋势对比图作图类
# 预想中的方法：画单人趋势图√、画趋势对比图√、画雷达图
class PicDrawer:
    pp_data = {}
    dc_data = {}

    def __init__(self, daily_completion_data):
        f1 = open(my_location + 'personal_progress_data.json', encoding='utf-8')
        self.pp_data = json.loads(f1.read())
        # f2读取画雷达图需要的json文件
        self.dc_data = daily_completion_data

    # 单人趋势图
    def drawPersonalProgressPic(self, id):
        completion = self.dc_data[id]
        dp = self.pp_data[str(id)]["daily_progress"]
        days = [i for i in range(1, len(completion) + 1)]
        days[len(completion) - 1] = dp[len(completion) - 1]["date"]
        plt.plot(days, completion)
        plt.title("userId: " + str(id) + "  " + dp[0]["date"] + "~" + dp[len(completion) - 1]["date"], fontsize=15)
        plt.xlabel("days", fontsize=12)
        plt.ylabel("completion", fontsize=12)
        plt.show()

    # cp趋势对比图
    def drawCpPic(self, id1, id2):
        completion1 = self.dc_data[str(id1)]
        completion2 = self.dc_data[str(id2)]
        days1 = [i for i in range(1, len(completion1) + 1)]
        days2 = [i for i in range(1, len(completion2) + 1)]
        plt.plot(days1, completion1)
        plt.plot(days2, completion2)
        plt.title("user: " + str(id1) + "  cp: " + str(id2), fontsize=12)
        plt.xlabel("days", fontsize=12)
        plt.ylabel("completion", fontsize=12)
        plt.show()


# 用户类
# 初始化必需参数：id
# 初始化同时创建一个DataPaser类对象和PicDrawer类对象
# 包含成员变量id、detailed_data、personal_progress、fit_func、dataPaser
# 包含成员方法：获取所有提交信息、获取个人进度数据、获取进度趋势拟合信息、获取匹配cp、分差过大cp过滤
class User:
    id = 0
    detailed_data = {}
    personal_progress = []
    fit_func = {}
    dataPaser = None
    picDrawer = None

    def __init__(self, id):
        self.id = int(id)
        self.dataPaser = DataPaser()
        self.picDrawer = PicDrawer(self.dataPaser.daily_completion_data)

    # def getDetailedData(self):
    #     return self.dataPaser.getDetailedData(self.id)

    def getPersonalProgress(self):
        return self.dataPaser.getPersonalProgressData(self.id)

    def drawPersonalProgressPic(self):
        self.picDrawer.drawPersonalProgressPic(self.id)

    def getFitFunc(self):
        return self.dataPaser.getFitFuncData(self.id)

    def isMatch(self, id1, id2, lower, greater):
        scores = self.dataPaser.user_average
        s1 = scores[str(id1)]
        s2 = scores[str(id2)]
        return s1 + lower <= s2 <= s1 + greater

    def getCpList(self, num, similar, draw, lower, greater):
        # 求导差
        cp_list1 = self.dataPaser.getCouples(self.id, 0)
        # 余弦相似度
        cp_list2 = self.dataPaser.getCouples(self.id, 1)
        # DTW
        cp_list3 = self.dataPaser.getCouples(self.id, 2)
        # 雷达图
        cp_list4 = self.dataPaser.getCouples(self.id, 3)

        if similar:
            res1 = sorted(cp_list1, key=lambda x: x['similarity'], reverse=False)[0:num]
            res2 = sorted(cp_list2, key=lambda x: x['similarity'], reverse=True)[0:num]
            res3 = sorted(cp_list3, key=lambda x: x['similarity'], reverse=True)[0:num]
        else:
            res1 = sorted(cp_list1, key=lambda x: x['similarity'], reverse=True)[0:num]
            res2 = sorted(cp_list2, key=lambda x: x['similarity'], reverse=False)[0:num]
            res3 = []

        length=int(len(cp_list4)/2)
        res4 = cp_list4[0:length]
        res5 = sorted(cp_list4, key=lambda x: x['similarity'], reverse=True)[0:length]
        # 列表转存字典
        cp_list = {}
        res_list = [res1, res2, res3]
        method_list = ["求导差匹配", "余弦相似度匹配", "DTW匹配"]
        for cp in res1 + res2 + res3:
            print(cp)
            if self.isMatch(self.id, cp["companion_id"], lower, greater):
                cp_list[cp["companion_id"]] = None
        for i in range(3):
            res = res_list[i]
            method = method_list[i]
            for cp in res:
                if not self.isMatch(self.id, cp["companion_id"], lower, greater): continue
                if cp_list[cp["companion_id"]] is None:
                    print(cp)
                    str_type = ""
                    for i in res4:
                        if i["companion_id"]==cp["companion_id"]:
                            str_type="相似"
                            break
                    for i in res5:
                        if i["companion_id"]==cp["companion_id"]:
                            str_type="互补"
                            break
                    cp_list[cp["companion_id"]] = {
                        "method": [method],
                        "similarities": [cp['similarity']],
                        "matchType": [str_type]
                    }
                else:
                    cp_list[cp["companion_id"]]["method"].append(method)
                    cp_list[cp["companion_id"]]["similarities"].append(cp['similarity'])

        if draw:
            for cp in cp_list:
                self.picDrawer.drawCpPic(self.id, cp)

        return cp_list
    #
    # # 获取用求导差匹配的相似度最高cp的前num位
    # def getBestSimilarCPs_DelDeriv(self, num):
    #     res = self.dataPaser.getCouples(self.id)
    #     if num > len(res["companions"]):
    #         print("No enough targets!")
    #     else:
    #         return res["companions"][0: num: 1]
    #
    # def drawBestSimilarCPs_DelDeriv(self, num):
    #     res = self.dataPaser.getCouples(self.id)
    #     if num > len(res["companions"]):
    #         print("No enough targets!")
    #     else:
    #         cps = res["companions"][0: num: 1]
    #         for item in cps:
    #             self.picDrawer.drawCpPic(self.id, int(item["companion_id"]))
    #
    # # 获取用求导差匹配的相似度最低cp的前num位
    # def getBestDissimilarCPs_DelDeriv(self, num):
    #     res = self.dataPaser.getCouples(self.id)
    #     if num > len(res["companions"]):
    #         print("No enough targets!")
    #     else:
    #         return sorted(res["companions"], key=lambda x: x['similarity'], reverse=True)[0: num: 1]
    #
    # def drawBestDissimilarCPs_DelDeriv(self, num):
    #     res = self.dataPaser.getCouples(self.id)
    #     if num > len(res["companions"]):
    #         print("No enough targets!")
    #     else:
    #         cps = sorted(res["companions"], key=lambda x: x['similarity'], reverse=True)[0: num: 1]
    #         for item in cps:
    #             self.picDrawer.drawCpPic(self.id, int(item["companion_id"]))


if __name__ == '__main__':
    user = User(61406)
    score_range = (0, 10)  # 允许匹配cp的分数差距范围
    # 参数：
    # 每种方法匹配人数，
    # T-相似 F-相反，
    # 是否画图，
    # cp分数范围：[本人分数+score_range[0],本人分数+score_range[1]]
    cp_list = user.getCpList(5, True, False, score_range[0], score_range[1])
    print(len(cp_list))
    print(cp_list.keys())
    for item in cp_list:
        print(item, ":", cp_list[item])
