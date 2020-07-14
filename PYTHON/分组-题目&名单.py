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
    student_list=[group1,group2,group3,group4]
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
        print(len(data))
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


if __name__ == '__main__':
    s = SelectGroup
    s.main_func(s)

    dic_group = {}

    for index in range(4):
        g = s.groups[index]
        name="分组"+(str)(index+1)
        dic_group[name]={
            "题目":g,
            "学生":s.student_list[index]
        }
    #     print("分组", index, ':', g, '\n')
    #
    # print("名单 1 :", s.group1, "\n人数", len(s.group1), '\n')
    # print("名单 2 :", s.group2, "\n人数", len(s.group2), '\n')
    # print("名单 3 :", s.group3, "\n人数", len(s.group3), '\n')
    # print("名单 4 :", s.group4, len(s.group4), '\n')

    print(dic_group)

    with open('分组.json', 'a', encoding='utf8') as file:
        json.dump(dic_group,file,ensure_ascii=False)
