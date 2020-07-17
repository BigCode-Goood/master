import json
import math
import matplotlib.pyplot as plt

user_msg = open('D:/数据科学/master/JSON/code_length_2.0.json', encoding='utf-8')
res1 = user_msg.read()
data_user_msg = json.loads(res1)

scores = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

case_msg = {}
group_msg = open('D:/数据科学/master/JSON/分组.json', encoding="utf-8")
res2 = group_msg.read()
data_group_msg = json.loads(res2)

studentNum = len(data_group_msg["分组1"]["学生"])


# 获取题目信息
def get_case_message():
    zeroNum = {}
    dic_difficulty = {}
    for caseId in data_group_msg["分组1"]["题目"]:
        zeroNum[caseId]=0
        dic_difficulty[caseId] = {
            "类型": 0,
            "分数": 0,
            "代码行数": 0,
            "提交次数": 0
        }
    all_lines=[]
    for d_u_m in data_user_msg:
        for case in d_u_m["casses"]:
            caseId = case["case_id"]
            if case["final_score"] >= 50:
                zeroNum [caseId]+=1
            dic_difficulty[caseId]["类型"] = case["case_type"]
            dic_difficulty[caseId]["分数"] += case["final_score"]
            dic_difficulty[caseId]["代码行数"] += case["code_length"]
            # print("代码行数",case["code_length"])
            if case["final_score"] >= 50:
                dic_difficulty[caseId]["提交次数"] += case["upload_count"]
    for dicId in dic_difficulty:
        dic = dic_difficulty[dicId]
        # print(dic)
        # print((studentNum-zeroNum[dicId]))
        dic["分数"] = int(dic["分数"]) / studentNum
        dic["代码行数"] = int(dic["代码行数"]) / (studentNum-zeroNum[dicId])
        all_lines.append(dic["代码行数"])
        dic["提交次数"] = int(dic["提交次数"]) / (studentNum-zeroNum[dicId])
        print(zeroNum[dicId])
    print(dic_difficulty,zeroNum)
    # with open('D:/数据科学/master/JSON/题目信息.json', 'a', encoding='utf8') as file:
    #     json.dump(dic_difficulty, file, ensure_ascii=False)
    all_lines.sort()
    print(all_lines)

# 计算类型均分
def type_average():
    for d_u_m in data_user_msg:
        for case in d_u_m["casses"]:
            score = case["final_score"]
            index = int(case["case_type"]) - 1
            scores[index][0] += score
            scores[index][1] += 1
    for i in range(8):
        scores[i][0] /= scores[i][1]
    print(scores)

    dic_average = {}
    for case_type in range(1, 9):
        dic_average[case_type] = scores[case_type - 1][0]
    # with open('D:/数据科学/master/JSON/题型均分.json', 'a', encoding='utf8') as file:
    #     json.dump(dic_average, file, ensure_ascii=False)


# 画图
def draw(x,y):
    plt.plot(x,y)
    plt.title("case_difficulty")
#    plt.savefig("题目难度" + '.png') # 保存图片
    plt.show()


# 计算题目难度公式
def calculation(case_score, type_score, lines, upload):
    if upload < 1:
        upload = 1
    # if case_score >= 85: case_score = 100
    dif = math.pow(100 / case_score, 0.8) * math.pow(100 / type_score, 0.7) * (1 + 0.3*math.log(lines, 150)) * (
            1 + 0.2*math.log(upload, 10))
    print((1 + math.log(lines, 100)),"代码长度")
    print( 1 + math.log(upload, 10),"提交次数")
    return 0.92+dif/20


# 计算题目难度
def cal_difficulty():
    dic_difficulty = {}

    cases_msg = open('D:/数据科学/master/JSON/题目信息.json', encoding='utf-8')
    res1 = cases_msg.read()
    data_cases_msg = json.loads(res1)

    type_msg = open('D:/数据科学/master/JSON/题型均分.json', encoding='utf-8')
    res2 = type_msg.read()
    data_type_msg = json.loads(res2)

    name_list = []
    num_list = []

    for caseId in data_cases_msg:
        name_list.append(caseId)

        dic_difficulty[caseId] = 0
        case_score = data_cases_msg[caseId]["分数"]
        case_type = data_cases_msg[caseId]["类型"]
        type_score = data_type_msg[str(case_type)]
        lines = data_cases_msg[caseId]["代码行数"]
        uploads = data_cases_msg[caseId]["提交次数"]

        dic_difficulty[caseId] = calculation(case_score, type_score, lines, uploads)
        num_list.append(dic_difficulty[caseId])
    print(dic_difficulty)
    num_list.sort()
    draw([i for i in range(1,201)],num_list)

    # #
    # with open('D:/数据科学/master/JSON/题目难度.json', 'a', encoding='utf8') as file:
    #     json.dump(dic_difficulty, file, ensure_ascii=False)

# #
# get_case_message()
# # #
# type_average()
#
if __name__ == '__main__':
    cal_difficulty()
