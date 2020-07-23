import json
import matplotlib.pyplot as plt


# 数据解析器类
# 初始化时读取需要的所有文件并将解析后的json字符串存入
class DataPaser:
    code_length_data = []
    personal_progress_data = {}
    fit_func_data = {}
    couples = []

    def __init__(self):
        f1 = open('code_length_2.0.json', encoding='utf-8')
        self.code_length_data = json.loads(f1.read())
        f2 = open('personal_progress_data_pro000.json', encoding='utf-8')
        self.personal_progress_data = json.loads(f2.read())
        f3 = open('得分趋势拟合信息(plus coef).json', encoding='utf-8')
        self.fit_func_data = json.loads(f3.read())
        f4 = open('求导差相似度.json', encoding='utf-8')
        self.couples = json.loads(f4.read())

    # 根据user_id获取用户所有提交数据，由于当初存数据考虑不周，如今查询只能遍历QAQ
    def getDetailedData(self, id):
        for item in self.code_length_data:
            if int(item["user_id"]) == id:
                return item

    # 根据user_id获取用户每日完成度数据
    def getPersonalProgressData(self, id):
        return self.personal_progress_data[str(id)]["daily_progress"]

    def getFitFuncData(self, id):
        return self.fit_func_data[str(id)]

    def getCouples(self, id):
        for item in self.couples:
            if int(item["userid"]) == id:
                return item


# 趋势对比图作图类
# 预想中的方法：画单人趋势图√、画趋势对比图√、画雷达图
class PicDrawer:
    pp_data = {}

    def __init__(self):
        f1 = open('personal_progress_data_pro000.json', encoding='utf-8')
        self.pp_data = json.loads(f1.read())
        # f2读取画雷达图需要的json文件

    # 单人趋势图
    def drawPersonalProgressPic(self, id):
        completion = []
        dp = self.pp_data[str(id)]["daily_progress"]
        for item in dp:
            completion.append(item["completion"])
        days = [i for i in range(1, len(completion) + 1)]
        # days[0]=dp[0]["date"]
        # days[len(completion)-1]=dp[len(completion)-1]["date"]
        plt.plot(days, completion)
        plt.title("userId: " + str(id) + "  " + dp[0]["date"] + "~" + dp[len(completion) - 1]["date"], fontsize=15)
        plt.xlabel("days", fontsize=12)
        plt.ylabel("completion", fontsize=12)
        plt.show()

    def drawCpPic(self, id1, id2):
        completion1 = []
        completion2 = []
        dp1 = self.pp_data[str(id1)]["daily_progress"]
        dp2 = self.pp_data[str(id2)]["daily_progress"]
        for item in dp1:
            completion1.append(item["completion"])
        for item in dp2:
            completion2.append(item["completion"])
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
# 初始化同时创建一个DataPaser类对象
# 包含成员变量id、detailed_data、personal_progress、fit_func、dataPaser
# 包含成员方法：获取所有提交信息、获取个人进度数据、获取进度趋势拟合信息、获取
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
        self.picDrawer = PicDrawer()

    def getDetailedData(self):
        return self.dataPaser.getDetailedData(self.id)

    def getPersonalProgress(self):
        return self.dataPaser.getPersonalProgressData(self.id)

    def drawPersonalProgressPic(self):
        self.picDrawer.drawPersonalProgressPic(self.id)

    def getFitFunc(self):
        return self.dataPaser.getFitFuncData(self.id)

    # 获取用求导差匹配的相似度最高cp的前num位
    def getBestSimilarCPs_DelDeriv(self, num):
        res = self.dataPaser.getCouples(self.id)
        if num > len(res["companions"]):
            print("No enough targets!")
        else:
            return res["companions"][0: num: 1]

    def drawBestSimilarCPs_DelDeriv(self, num):
        res = self.dataPaser.getCouples(self.id)
        if num > len(res["companions"]):
            print("No enough targets!")
        else:
            cps = res["companions"][0: num: 1]
            for item in cps:
                self.picDrawer.drawCpPic(self.id, int(item["companion_id"]))

    # 获取用求导差匹配的相似度最低cp的前num位
    def getBestDissimilarCPs_DelDeriv(self, num):
        res = self.dataPaser.getCouples(self.id)
        if num > len(res["companions"]):
            print("No enough targets!")
        else:
            return sorted(res["companions"], key=lambda x: x['similarity'], reverse=True)[0: num: 1]

    def drawBestDissimilarCPs_DelDeriv(self, num):
        res = self.dataPaser.getCouples(self.id)
        if num > len(res["companions"]):
            print("No enough targets!")
        else:
            cps = sorted(res["companions"], key=lambda x: x['similarity'], reverse=True)[0: num: 1]
            for item in cps:
                self.picDrawer.drawCpPic(self.id, int(item["companion_id"]))


if __name__ == '__main__':
    user = User(48117)
    # print(user.getDetailedData())
    # print(user.getPersonalProgress())
    # print(user.getFitFunc())
    # print(user.getBestSimilarCPs_DelDeriv(5))
    # print(user.getBestDissimilarCPs_DelDeriv(2))
    # user.drawPersonalProgressPic()
    # user.drawBestSimilarCPs_DelDeriv(2)
    user.drawBestDissimilarCPs_DelDeriv(3)
