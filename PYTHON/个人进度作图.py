import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit


def cal_error_val(y, yval):
    error_val = 0
    for i in range(len(y)):
        error_val += np.square(y[i] - yval[i])
    return np.sqrt(error_val)


# 高斯函数
def func1(x, a, b, c):
    return a * np.power(np.e, -np.square(x - b) / 2 * np.square(c))


def x_n(x, y, n):
    # 直接n次多项式拟合
    f1 = np.polyfit(x, y, n)
    # print('f1 is :\n', f1)

    p1 = np.poly1d(f1)
    # print('p1 is :\n', p1)

    yvals = p1(x)
    return {
        "yvals": yvals,
        "系数": f1
    }


if __name__ == '__main__':

    # 用于拟合的函数
    func_list = [func1]
    # 记录最小标准差选择拟合函数
    min_error_val = None
    # 最终确认的拟合曲线
    y_fit_val = []

    # 拟合曲线类型
    # 三次函数形状问题？找拐点
    fit_type = -1
    type_list = ["高斯函数", "U型二次函数", "n型二次函数", "a>0的三次函数", "a<0的三次函数"]

    f = open('personal_progress_data.json', encoding='utf-8')
    res = f.read()
    user_data = json.loads(res)

    period = []
    dataC = []

    # 测试的数据记录：
    # user[2]:标准高斯函数
    # user[30]：应该是指数函数 还没补上去，我去恰饭啦，耶
    # user[31 32]:a>0的三次函数，无拐点

    user = user_data[30]
    dailyP = user['daily_progress']
    set_period_length = 3  # 设置几天为一个period
    cnt = 0
    p = 1
    period_comp = 0
    # 注意：补全日期数据保证period数相同
    for item in dailyP:
        if cnt == set_period_length:
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

    x = np.array(period)
    y = np.array(dataC)

    type = 0
    # 记录拟合函数类型，先遍历拟合func_list，再遍历多项式次数

    # 非线性最小二乘法拟合

    for func in func_list:
        try:
            popt, pcov = curve_fit(func, x, y)

            # 获取popt里面是拟合系数
            # print(popt)
            yvals = func(x, *popt)  # 拟合y值
            # print('popt:', popt)
            er_val = cal_error_val(y, yvals)
            # 判断是否为最佳拟合
            if min_error_val is None or er_val < min_error_val:
                min_error_val = er_val
                fit_type = type
                y_fit_val = yvals
        except:pass
        type += 1

    # 遍历拟合多项式，n为多项式次数
    for n in [2, 3]:
        res = x_n(x, y, n)
        er_val = cal_error_val(y, res["yvals"])
        yvals = res["yvals"]
        # 判断是否为最佳拟合
        if min_error_val is None or er_val < min_error_val:
            min_error_val = er_val
            y_fit_val = yvals
            if yvals[0] > 0:
                fit_type = type
            else:
                fit_type = type + 1
        if n == 2:
            type += 2
        if n == 3:
            # todo:考虑拐点？
            pass

    # 2:u,n
    # 3:/\/ \/\

    # 绘图

    print("拟合函数：", type_list[fit_type])

    plt.plot(period, dataC)
    plt.plot(x, y_fit_val, 'r', label='polyfit values')

    plt.title("userId: " + user['user_id'], fontsize=20)
    plt.xlabel("period", fontsize=12)
    plt.ylabel("completion", fontsize=12)
    plt.tick_params(axis='both', labelsize=10)
    # plt.savefig(user['user_id'] + '.png') # 保存图片
    plt.show()
