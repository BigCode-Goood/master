import requests
import os
import zipfile
import json


class SelectGroup:
    g1 = []
    g2 = []
    g3 = []
    g4 = []
    groups = [g1, g2, g3, g4]
    # g1到g5为每一组的题目
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    # group1到group5为每一组学生名单

    unfinished_list = []

    # 暂时存储

    def append_user_to_group(self, index, id):
        g = self.group1
        if index == 0:
            g = self.group1
        elif index == 1:
            g = self.group2
        elif index == 2:
            g = self.group3
        elif index == 3:
            g = self.group4

        g.append(id)

    def main_func(self):
        f = open('test_data.json', encoding='utf-8')
        res = f.read()
        data = json.loads(res)
        for user_id in data:
            user_data = data[user_id]

            if len(user_data['cases']) == 200:

                cases = []
                for c in user_data['cases']:
                    cases.append(c['case_id'])

                for index in range(4):
                    if len(self.groups[index]) == 0:
                        cases.sort()
                        self.groups[index] = cases
                        self.append_user_to_group(self, index, user_id)
                        break
                    else:
                        if self.groups[index] == sorted(cases):
                            self.append_user_to_group(self, index, user_id)
                            break
                        else:
                            pass
            elif len(user_data['cases']) < 200:
                self.unfinished_list.append(user_id)

        for user_id in self.unfinished_list:
            user_data = data[user_id]
            cases = []
            for c in user_data['cases']:
                cases.append(c['case_id'])

            for index in range(4):
                g = self.groups[index]
                if set(cases) < set(g):
                    self.append_user_to_group(self, index, user_id)
                    break


def download(url):
    req = requests.get(url)
    filename = url.split('/')[-1]
    if req.status_code != 200:
        print('下载异常')
        return
    try:
        with open(filename, 'wb') as f:
            # req.content为获取html的内容
            f.write(req.content)
            print('下载成功')
            print(filename)

    except Exception as e:
        print(e)

    os.chdir('I:\\bigCode_py\\DataParsing')
    extracting = zipfile.ZipFile(filename)
    zip_list = extracting.namelist()
    extracting.extractall()
    extracting = zipfile.ZipFile(zip_list[0])
    nums = filename.split('_')[1]
    dir = "I:\\bigCode_data\\" + nums
    os.mkdir(dir)
    print(dir + "目录创建成功")
    extracting.extract('main.py', dir)
    extracting.close()
    filename = dir + "\\main.py"
    code_lines = []
    try:
        fp = open(filename, "r", encoding='utf-8')  #
        print("%s 文件打开成功" % filename)
        line = fp.readline()
        while line:
            code_lines.append(line)
            line = fp.readline()
        fp.close()
    except Exception as e:
        print(e)

    len = getValicLength(code_lines)
    return len


def getValicLength(code_lines):  # 去除cpp代码和面向用例代码
    if len(code_lines) == 0:
        return 0
    if "#include<" in code_lines[0]:
        return 0
    ifNum = 0
    elseNum = 0
    printNum = 0
    exNum = 0
    exBegin = exEnd = -1
    inEx = False
    for i in range(0, len(code_lines)):
        if "'''" in code_lines[i] and exBegin == -1:
            exBegin = i
            inEx = True
        elif "'''" in code_lines[i] and exBegin != -1 and exEnd == -1:
            exEnd = i
            inEx = False
            exNum = exNum + exEnd - exBegin + 1
        else:
            if inEx:
                continue
            if code_lines[i] == '\n':
                exNum += 1
            elif "#" in code_lines[i]:
                emp=0
                while code_lines[i][emp]==' ':
                    emp+=1
                if code_lines[i][emp]=="#":
                    exNum+=1
            else:
                if "if" in code_lines[i]:
                    ifNum += 1
                elif "else" in code_lines[i]:
                    elseNum += 1
                elif "print" in code_lines[i]:
                    printNum += 1

    if (len(code_lines) - exNum) == 0:
        return 0


    if (ifNum + elseNum + printNum) / (len(code_lines) - exNum) >= 0.6:
        return 0
    if printNum>4:
        return 0
    if printNum/len(code_lines)>=0.32:
        return 0
    return len(code_lines) - exNum


if __name__ == '__main__':
    # f = open('main.py', encoding='utf-8')
    # line = f.readline()
    # code_lines=[]
    # while line:
    #     code_lines.append(line)
    #     line = f.readline()
    # f.close()
    # len=getValicLength(code_lines)
    # print(len)

    # len=download("http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558143538.zip")
    # print(len)

    s = SelectGroup
    s.main_func(s)
    nameList = s.group1

    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    cnt = 0
    code_url = []

    for user_id in data:
        if str(user_id) in nameList:
            user_data = data[user_id]
            user_cases = user_data['cases']
            item = {}
            item['user_id'] = user_id
            item_cases = []
            for cases in user_cases:
                case = {}
                case['case_id'] = cases['case_id']
                if cases['case_type'] == "字符串":
                    case['case_type'] = 1
                elif cases['case_type'] == "数字操作":
                    case['case_type'] = 2
                elif cases['case_type'] == "数组":
                    case['case_type'] = 3
                elif cases['case_type'] == "排序算法":
                    case['case_type'] = 4
                elif cases['case_type'] == "查找算法":
                    case['case_type'] = 5
                elif cases['case_type'] == "线性表":
                    case['case_type'] = 6
                elif cases['case_type'] == "图结构":
                    case['case_type'] = 7
                elif cases['case_type'] == "树结构":
                    case['case_type'] = 8
                upload_records = cases['upload_records']
                index = len(upload_records)
                if index == 0:
                    continue
                else:
                    case['upload_count'] = index
                    case['case_url'] = upload_records[index - 1]['code_url']
                    case['datetime'] = upload_records[index - 1]['upload_time']
                    case['code_length'] = download(case['case_url'])
                    if case['code_length'] == 0:
                        case['final_score'] = 0.0
                    else:
                        case['final_score'] = cases['final_score']
                item_cases.append(case)
            item['casses'] = item_cases
            code_url.append(item)
    codeLengthJson = json.dumps(code_url, ensure_ascii=False)

    with open("code_length_2.0.json", "w") as fp:
        fp.write(codeLengthJson)
