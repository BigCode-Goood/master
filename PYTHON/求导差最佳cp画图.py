import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    f = open('personal_progress_data000.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)

    user_data = {}
    for item in data:
        dp = item["daily_progress"]
        dpdata = []
        for i in dp:
            dpdata.append(i["completion"])
        user_data[item["user_id"]] = dpdata

    fd = open('求导差相似度.json', encoding='utf-8')
    r = fd.read()
    deriv_pair = json.loads(r)

    pairs = {}
    for item in deriv_pair:
        pairs[item["userid"]] = item["companions"][0]["companion_id"]
        dpdata1 = user_data[item["userid"]]
        dpdata2 = user_data[item["companions"][0]["companion_id"]]
        if len(dpdata1) > len(dpdata2):
            while len(dpdata2) < len(dpdata1):
                dpdata2.append(0)
        elif len(dpdata1) < len(dpdata2):
            while len(dpdata1) < len(dpdata2):
                dpdata1.append(0)

        days = [i for i in range(1, len(dpdata1) + 1)]
        plt.plot(days, dpdata1, 'blue', label='user')
        plt.plot(days, dpdata2, 'red', label='best_cp')
        plt.title("user: " + item["userid"] + "  cp: " + item["companions"][0]["companion_id"] + "  similarity=" + str(
            item["companions"][0]["similarity"])[0:6], fontsize=12)
        plt.savefig("I:/big_code_backup/求导差匹配图/" + item["userid"] + "-" + item["companions"][0]["companion_id"] + '.png')
        plt.show()
