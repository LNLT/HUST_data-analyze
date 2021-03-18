import pandas as pd
import numpy as np

def data_set():
    data = pd.read_csv("Groceries.csv")
    # 读取列数据
    col_2 = data['items']
    data = np.array(col_2)
    # 将列数据转化为二维数组
    list_t1 = []
    for line in data:
        line = line.strip('{').strip('}').split(',')
        s = []
        for i in line:
            s.append(i)
        list_t1.append(s)
    data = list_t1
    print(data[:4])
    return data


def Create_C1(data):
    # 创建C1
    c1 = set()
    for items in data:
        for item in items:
            item_set = frozenset([item])
            # 使用frozenset函数以便于查找元素集，使用tuple不是特别方便
            c1.add(item_set)
    print(c1)
    return c1


def is_apriori(ck_item, Lk):
    # Apriori定律1 如果一个集合是频繁项集，则它的所有超集都是频繁项集
    for item in ck_item:
        sub_item = ck_item - frozenset([item])
        if sub_item not in Lk:
            return False
    return True


def Create_Ck(Lk, k):
    Ck = set()
    len_Lk = len(Lk)
    list_Lk = list(Lk)
    for i in range(len_Lk):
        for j in range(i + 1, len_Lk):
            l1 = list(list_Lk[i])[0:k - 2]
            l2 = list(list_Lk[j])[0:k - 2]
            l1.sort()
            l2.sort()
            # 求k阶频繁项度时，对于候选集Lk-1，若两项的前K-2项一致，则组合出来的极有可能为Lk里面的频繁项（根据k阶频繁项的k-1阶的组合都必须为k-1阶频繁项可得）
            # list[s:t]：截取s到t范围的元素生成一个新list
            if l1 == l2:
                Ck_item = list_Lk[i] | list_Lk[j]
                if is_apriori(Ck_item, Lk):
                    Ck.add(Ck_item)
    return Ck


def get_Lk(data_set, Ck, min_support, support_data):
    # 计算出现次数
    # len:多维数组返回最外围的大小
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    data_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / data_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / data_num
    return Lk

def get_Rule(L, support_data, minconfidence):
    # 参数：所有的频繁项目集，项目集-支持度dic，最小置信度
    rule_list = []
    sub_set_list = []
    for i in range(len(L)):
        for frequent_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(frequent_set):
                    conf = support_data[frequent_set] / support_data[sub_set]
                    # 将rule声明为tuple
                    rule = (sub_set, frequent_set - sub_set, conf)
                    if conf >= minconfidence and rule not in rule_list:
                        rule_list.append(rule)
            sub_set_list.append(frequent_set)
    return rule_list


if __name__ == "__main__":
    data = data_set()
    minsupport = 0.005
    minconfidence = 0.5
    support_data = {}
    C1 = Create_C1(data)
    L1 = get_Lk(data, C1, minsupport, support_data)
    print(len(L1), '1')
    Lk = L1.copy()
    L = []
    L.append(Lk)  # 末尾添加指定元素
    for k in range(2, 3 + 1):
        Ck = Create_Ck(Lk, k)
        Lk = get_Lk(data, Ck, minsupport, support_data)
        print(len(Lk), k)
        Lk = Lk.copy()
        L.append(Lk)
    rule_list = get_Rule(L, support_data, minconfidence)
    print(len(rule_list), "confidence")
    with open('L1.csv', 'w') as f:
        for Lk in L:
            for key in Lk:
                f.write('{},\t{}\n'.format(key, support_data[key]))
    with open('Z1.csv', 'w') as f:
        for item in rule_list:
            f.write('{}\t{}\t{}\t: {}\n'.format(item[0], "of", item[1], item[2]))
    print('ok')