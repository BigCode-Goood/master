import json
import numpy as np
import matplotlib.pyplot as plt

with open('D:/大二下/数据科学基础/master/JSON/不同类型得分排名.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)
type_array = ["字符串", "数字操作", "数组", "排序算法", "查找算法", "线性表", "图结构", "树结构"]
labels = np.array(type_array)
data_len = 8
for item in json_data:
    data = [item['1'], item['2'], item['3'], item['4'], item['5'], item['6'], item['7'], item['8']]
    data = np.array(data)
    angles = np.linspace(0, 2 * np.pi, data_len, endpoint=False)
    data = np.concatenate((data, [data[0]]))  # 闭合
    angles = np.concatenate((angles, [angles[0]]))  # 闭合
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)  # polar参数！！
    ax.plot(angles, data, 'bo-', linewidth=2)  # 画线
    ax.fill(angles, data, facecolor='r', alpha=0.25)  # 填充
    ax.set_thetagrids(angles * 180 / np.pi, labels, fontproperties="SimHei")
    ax.set_title("学生ID：" + str(item["id"]), va='bottom', fontproperties="SimHei")
    ax.set_rlim(0, 1)  # 设置雷达图的范围
    ax.grid(True)
    plt.savefig("D:/大二下/数据科学基础/master/pics/雷达图/" + str(item["id"]) + ".png", dpi=120)
