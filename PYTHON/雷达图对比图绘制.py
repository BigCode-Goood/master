import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager


def plot_radar(data):
    N = 8  # 属性个数
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)  # 设置雷达图的角度，用于平分切开一个圆面
    angles = np.concatenate((angles, [angles[0]]))  # 为了使雷达图一圈封闭起来
    fig = plt.figure(figsize=(12, 12))  # 设置画布大小
    ax = fig.add_subplot(111, polar=True)  # 这里一定要设置为极坐标格式
    sam = ['r-', 'm-', 'g-', 'b-', 'y-', 'k-', 'w-', 'c-']  # 样式
    lab = []  # 图例标签名
    for i in range(len(data)):
        values = [float(data[i]["1"]), float(data[i]["2"]), float(data[i]["3"]), float(data[i]["4"]), float(data[i]["5"]), float(data[i]["6"]), float(data[i]["7"]),
                  float(data[i]["8"])]
        feature = ['字符串', '数字操作', '数组', '排序算法', '查找算法', '线性表', '图结构', '树结构']  # 设置各指标名称

        # 为了使雷达图一圈封闭起来，需要下面的步骤
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, sam[i], linewidth=2)  # 绘制折线图
        #        ax.fill(angles, values, alpha=0.5) # 填充颜色
        ax.set_thetagrids(angles * 180 / np.pi, feature, font_properties="SimHei")  # 添加每个特征的标签
        ax.set_ylim(auto=True)  # 设置雷达图的范围
        plt.title('雷达图对比图', font_properties="SimHei")  # 添加标题
        ax.grid(True)  # 添加网格线
        lab.append('邻域块' + str(i + 1))
    plt.savefig("D:/大二下/数据科学基础/master/pics/雷达图对比图/" + data[0]["id"] + "与" + data[1]["id"] + ".png", dpi=120)  # 保存图片到本地
    plt.show()  # 显示图形


if __name__ == '__main__':
    with open('D:/大二下/数据科学基础/master/JSON/不同类型得分排名.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    with open('D:/大二下/数据科学基础/master/JSON/雷达图匹配.json', 'r', encoding='utf8') as fp1:
        json_data1 = json.load(fp1)
    student_id = "48117"
    for i in json_data1[student_id]["companions"]:
        data = []
        companion_id = i["companion_id"]
        for item in json_data:
            if item["id"] == student_id or item["id"] == companion_id:
                data.append(item)
        plot_radar(data)
