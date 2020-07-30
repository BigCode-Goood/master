import json
import math
import numpy as np
from scipy.misc import derivative
from sympy import diff, symbols


def getDeriv(type, coef, i):
    x = symbols('x', real=True)
    # 高斯
    if type == 0:
        a = float(str(coef[0])[0:8])
        b = float(str(coef[1])[0:8])
        c = float(str(coef[2])[0:8])
        d = float(str(coef[3])[0:8])
        y = a * np.power(np.e, -np.square(x - b) / 2 * np.square(c)) + d
        return diff(y, x, 1).subs(x, i)
    # 正弦
    elif type == 1:
        a = float(str(coef[0])[0:8])
        b = float(str(coef[1])[0:8])
        c = float(str(coef[2])[0:8])
        d = float(str(coef[3])[0:8])
        return a*b*np.cos(b*i+c)
    # 指数
    elif type == 2 or type == 3:
        a = float(str(coef[0])[0:8])
        b = float(str(coef[1])[0:8])
        c = float(str(coef[2])[0:8])
        y = a * b ** x + c
        return diff(y, x, 1).subs(x, i)
    # 反比例
    elif type == 4:
        a = float(str(coef[0])[0:8])
        b = float(str(coef[1])[0:8])
        c = float(str(coef[2])[0:8])
        y = a / np.power(x, b) + c
        return diff(y, x, 1).subs(x, i)
    # 一次
    elif type == 5 or type == 6:
        a = float(str(coef[0])[0:8])
        b = float(str(coef[1])[0:8])
        return diff(a * x + b, x, 1).subs(x, i)
    # 二次
    elif type == 7 or type == 8:
        a = float(str(coef[0])[0:8])
        b = float(str(coef[1])[0:8])
        c = float(str(coef[2])[0:8])
        return diff(a * x ** 2 + b * x + c, x, 1).subs(x, i)


if __name__ == '__main__':
    f = open('得分趋势拟合信息(plus coef).json', encoding='utf-8')
    res = f.read()
    all = json.loads(res)

    fd=open('趋势分组.json', encoding='utf-8')
    r=fd.read()
    group=json.loads(r)

    g1=group["下降"]
    g2=group["上升"]+group["下降-上升"]
    g3=group["上升-下降"]
    g4=group["波动"]

    deriv1 = []
    deriv2 = []
    del_deriv = []
    x = []
    pairs = []
    n = 20  # 设置取点个数
    # 大致分类中每两个函数进行比较，取等距离点n个，求两函数在n个点上的导数差之和并取平均得到导数差，导数差越小相似度越高
    for item in all:
        pairs_item = {}
        pairs_item["userid"] = item
        pairs_item["companions"] = []
        for item2 in all:
            companion = {}
            deriv1 = []
            deriv2 = []
            del_deriv = []
            companion["companion_id"] = item2
            if item==item2 :
                continue
            if item != item2:
                end = all[item]["end"] if all[item]["end"] <= all[item2]["end"] else all[item2]["end"]
                x = np.linspace(0.5, end, n)
                for i in x:
                    deriv1.append(getDeriv(all[item]["拟合类型"], all[item]["coefficient"], i))
                    deriv2.append(getDeriv(all[item2]["拟合类型"], all[item2]["coefficient"], i))
                    del_deriv.append(
                        abs(getDeriv(all[item]["拟合类型"], all[item]["coefficient"], i) - getDeriv(all[item2]["拟合类型"], all[item2]["coefficient"], i))),
            companion["similarity"] = np.float(np.mean(del_deriv))
            pairs_item["companions"].append(companion)

        pairs_item["companions"]=sorted(pairs_item["companions"], key=lambda x: x['similarity'], reverse=False)
        pairs.append(pairs_item)
        pairsJson = json.dumps(pairs, ensure_ascii=False)
        print(pairs_item)
        print("finished:"+item)
    print(pairs)
    pairsJson = json.dumps(pairs, ensure_ascii=False)
    with open("求导差相似度.json", "w") as fp:
        fp.write(pairsJson)
