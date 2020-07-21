import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit


def cal_error_val(y, yval, size):
    sum_y = 0
    sum_yval = 0
    sum_y_mul_yval = 0
    sum_y2 = 0
    sum_yval2 = 0
    for i in range(size):
        sum_y += y[i]
        sum_yval += yval[i]
        sum_y_mul_yval += y[i] * yval[i]
        sum_y2 += np.square(y[i])
        sum_yval2 += np.square(yval[i])

    div = (sum_y2 - np.square(sum_y) / size) * (sum_yval2 - np.square(sum_yval) / size)
    # print("除数:",str(div))
    if div <= 0:
        r = 0
    else:
        r = (sum_y_mul_yval - sum_y * sum_yval / size) / np.sqrt(
            (sum_y2 - np.square(sum_y) / size) * (sum_yval2 - np.square(sum_yval) / size))
    return 1 - np.abs(r)


# 高斯函数
def func1(x, a, b, c, d):
    return a * np.power(np.e, -np.square(x - b) / 2 * np.square(c)) + d


# 幂函数 x
def func2(x, a, b, c):
    return a * np.power(x, b) + c


# 对数函数 x
def func3(x, a, b, c):
    return a * np.log(x, b) + c


# S型函数 x
def func4(x, a, b, c,d):
    return d / (a + b * np.power(np.e, -x)) + c


# sin
def func5(x, a, b, c, d):
    return a * np.sin(b * x + c) + d


# 指数函数
def func6(x, a, b, c):
    return a * b ** x + c


# a/x
def func7(x, a, b, c):
    return a / np.power(x, b) + c


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

    dic = {
    }

    # 用于拟合的函数
    func_list = [func1,func5, func6, func7]
    type_list = ["高斯函数", "正弦函数", "上升指数函数", "下降指数函数", "反比例函数", "一次增函数", "一次减函数", "U型二次函数",
                 "n型二次函数"]

    trend_type= {
        "高斯函数":"上升-下降",
        "正弦函数":"波动",
        "上升指数函数":"上升",
        "下降指数函数":"下降",
        "反比例函数":"下降",
        "一次增函数":"上升",
        "一次减函数":"下降",
        "U型二次函数":"下降-上升",
        "n型二次函数":"上升-下降"
    }

    f = open('personal_progress_data.json', encoding='utf-8')
    res = f.read()
    user_data = json.loads(res)



    for user_id in range(46):  # 输入要查看的userId

        # 选择拟合函数
        min_error_val = None
        # 最终确认的拟合曲线
        y_fit_val = []
        x_fit_val = []
        fit_dataC = []
        fit_popt = []

        # 拟合曲线类型
        # 三次函数形状问题？找拐点
        fit_type = -1

        fit_period_length = 0

        for set_period_length in [1, 2, 3]:  # 设置几天为一个period

            period = []
            dataC = []

            # 测试的数据记录：
            # user[2]:标准高斯函数
            # user[7]:高斯函数只有下降的一半
            # user[30]：应该是指数函数 还没补上去，我去恰饭啦，耶
            # user[31 32]:a>0的三次函数，无拐点
            # USER[25]:a>0的三次函数但是只有形如二次函数的前一半

            user = user_data[user_id]
            dailyP = user['daily_progress']

            cnt = 0
            p = 1
            period_comp = 0
            # 注意：补全日期数据保证period数相同
            for item in dailyP:
                if cnt == set_period_length:
                    period.append(p)
                    dataC.append(period_comp / 500)
                    period_comp = 0
                    cnt = 0
                    p += 1
                period_comp += item['completion']
                cnt += 1
            if cnt != 0:
                period.append(p)
                dataC.append(period_comp / 500)
                # 注意：为了判断周期把纵坐标缩短了

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
                    cf = func
                    # 获取popt里面是拟合系数
                    # print(popt)
                    yvals = func(x, *popt)  # 拟合y值
                    # print('popt:', popt)
                    er_val = cal_error_val(y, yvals, len(x))
                    # 判断是否为最佳拟合
                    if min_error_val is None or er_val < min_error_val:
                        if type == 0:  # 高斯函数期望要求
                            if popt[1] <= len(x)*0.25 or popt[1] >= len(x)*0.8:
                                type += 1
                                continue
                        if type == 1:  # sin周期要求
                            T = np.abs(2 * np.pi / popt[1])
                            if len(x) <= 2.5 * T:
                                type += 1
                                continue
                        min_error_val = er_val
                        fit_type = type
                        if type == 2:  # 指数函数趋势判断
                            if popt[1] < 1: fit_type += 1
                        y_fit_val = yvals
                        x_fit_val = x
                        fit_dataC = dataC
                        fit_popt = popt
                        fit_period_length = set_period_length
                except:
                    pass
                if type == 2:
                    type += 2
                else:
                    type += 1

            print(type)
            # 遍历拟合多项式，n为多项式次数
            for n in [1, 2]:
                res = x_n(x, y, n)
                er_val = cal_error_val(y, res["yvals"], len(x))
                yvals = res["yvals"]
                # 判断是否为最佳拟合
                if min_error_val is None or er_val < min_error_val:
                    if n == 2:
                        a = res["系数"][0]
                        b = res["系数"][1]
                        T = -b / (2 * a)  # 求出拐点，若拐点不在图像显示区间内则抛弃
                        if T <= 2 or len(x) * 0.8 <= T:
                            type += 2
                            continue
                    min_error_val = er_val
                    y_fit_val = yvals
                    x_fit_val = x
                    fit_dataC = dataC
                    fit_popt = res["系数"]
                    fit_period_length = set_period_length
                    if res["系数"][0] > 0:
                        fit_type = type
                    else:
                        fit_type = type + 1

                type += 2

            # 2:u,n
            # 3:/\/ \/\

        # 绘图
        print("R：", 1 - min_error_val)
        print("拟合函数：", type_list[fit_type])
        print("天数：", fit_period_length)

        plt.plot(x_fit_val, fit_dataC)
        plt.plot(x_fit_val, y_fit_val, 'r', label='polyfit values')

        plt.title("userId: " + user['user_id'] + "  R=" + str(1 - min_error_val)[0:6], fontsize=15)
        plt.xlabel("period", fontsize=12)
        plt.ylabel("completion", fontsize=12)
        plt.tick_params(axis='both', labelsize=10)
     #   plt.savefig('D:/bigcode/master/pics/最匹配拟合图/' + user['user_id'] + '.png')  # 保存图片
     #   plt.show()

        dic[user['user_id']] = {
            "拟合类型": fit_type,
            "拟合函数": type_list[fit_type],
            "趋势":trend_type[ type_list[fit_type]],
            "相关系数R": 1 - min_error_val
        }
        if 1-min_error_val<0.65:
            dic[user['user_id']]["趋势"]="波动"

    with open('D:/bigcode/master/JSON/得分趋势拟合信息.json', 'a', encoding='utf8') as fp1:
        json.dump(dic, fp1, ensure_ascii=False)
