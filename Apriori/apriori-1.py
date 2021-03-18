import pandas as pd
import numpy as np


def get_c1(data):
    c1 = []
    for x in data:
        for y in x:
            if [y] not in c1:
                c1.append([y])
    c1.sort()
    return c1

# def get_zhixindu(support, zhixin, minzhixin):
#     zhixin_num = {}
#     # 记录支持集合
#     zhixin_data = []
#     for keys in support:
#         print(keys)
#         print(keys[0:len(keys)-1])
#         print(support[keys])
#         print(zhixin[keys[0:len(keys)-1]])
#         ok = support[keys] / zhixin[keys[0:len(keys)-1]]
#         if ok >= minzhixin:
#             zhixin_num[tuple(keys)] = ok
#             zhixin_data.append(keys)
#     return zhixin_data, zhixin_num

def get_count(data, ck, minsupport):
    # 计算出现次数,
    # set() 函数创建一个无序不重复元素集，可进行关系测试
    # tuple() 函数将列表转换为元组
    temp_L = {}
    for x in ck:
        for y in data:
            if set(x).issubset(set(y)):
                if tuple(x) not in temp_L:
                    temp_L[tuple(x)] = 1
                else:
                    temp_L[tuple(x)] += 1
    # len:多维数组返回最外围的大小
    num_all = len(data)
    # 记录支持度
    support_num = {}
    # 记录支持集合
    support_data = []
    for keys in temp_L:
        ok = temp_L[keys]/num_all
        if ok >= minsupport:
            support_num[keys] = ok
            support_data.append(keys)
    return support_data, support_num


def get_candidate(LK, K):
    # 求第k次候选集
    ck = []    # 存放产生候选集
    # 求k阶频繁项度时，对于候选集Lk-1，若两项的前K-2项一致，则组合出来的极有可能为Lk里面的频繁项（根据k阶频繁项的k-1阶的组合都必须为k-1阶频繁项可得）
    for i in range(len(LK)):
        for j in range(i+1, len(LK)):
            L1 = list(LK[i])
            L2 = list(LK[j])      # 先排序，在进行组合
            L1.sort()
            L2.sort()
            if L1[:K-2] == L2[:K-2]:
                # new_item = set(LK[i]) | set(LK[j])
                # new_item = sorted(new_item)
                # if is_apriori(new_item, LK):
                #     ck.append(list(new_item))
                if K > 2:       # 第二次求候选集，不需要进行减枝，因为第一次候选集都是单元素，且已经减枝了，组合为双元素肯定不会出现不满足支持度的元素
                    new = list(set(LK[i]) ^ set(LK[j]))     # 集合运算 对称差集 ^ 含义，集合的元素在t或s中，但不会同时出现在二者中）
                else:
                    new = set()
                for x in LK:
                    if set(new).issubset(set(x)) and list(set(L1) | set(L2)) not in ck:
                        # Apriori定律1 如果一个集合是频繁项集，则它的所有超集都是频繁项集
                        # 减枝 new是 x 的子集，并且 还没有加入 ck 中
                        new_item = list(set(L1) | set(L2))
                        ck.append(new_item)
    return ck

# def is_apriori(Ck_item, Lk_sub_1):
#     # Apriori定律1 如果一个集合是频繁项集，则它的所有超集都是频繁项集
#     for item in Ck_item:
#         item1 = set([item])
#         sub_item = set(Ck_item) - item1
#         if tuple(sub_item) not in Lk_sub_1:
#             return False
#     return True
#
# def Generate_Rule(L, support_data, minconfidence):
#     # 参数：所有的频繁项目集，项目集-支持度dic，最小置信度
#     rule_list = []
#     sub_set_list = []
#     for i in range(len(L)-1):
#         for frequent_set1 in L[i+1]:
#             frequent_set = set(frequent_set1)
#             for sub_set1 in L[i]:
#                 sub_set = set(sub_set1)
#                 if sub_set.issubset(frequent_set):
#                     conf = support_data[tuple(frequent_set)] / support_data[tuple(sub_set)]
#                     # 将rule声明为tuple
#                     rule = (sub_set, frequent_set - sub_set, conf)
#                     if conf >= minconfidence and rule not in rule_list:
#                         rule_list.append(rule)
#             sub_set_list.append(frequent_set)
#     return rule_list


if __name__ == '__main__':
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

    c1 = get_c1(data)
    minsupport = 0.005
    minconfidence = 0.5
    L1, L1_num = get_count(data, c1, minsupport)
    L = [L1]
    support = L1_num
    K = 2  # 从第二个开始循环求解，先求候选集，在求频繁项集

    while (K < 4):  # k-2是因为F是从0开始数的     #前一个的频繁项集个数在2个或2个以上，才继续循环，否则退出
        print(K)
        ck = get_candidate(L[K - 2], K)  # 求第k次候选集
        fk, sup_k = get_count(data, ck, minsupport)  # 求第k次频繁项集
        print(len(fk), K)
        L.append(fk)  # 把新产生的候选集假如F
        support.update(sup_k)  # 字典更新，加入新得出的数据
        K += 1

    with open('L2_sup.csv', 'w') as f:
        for key in support:
            f.write('{},\t{}\n'.format(key, support[key]))
    # rule_list = Generate_Rule(L, support, minconfidence)
    # print(rule_list)
    # with open('confidence.csv', 'w') as f:
    #     for item in rule_list:
    #         f.write('{}\t{}\t{}\t{}\n'.format(item[0], "=>", item[1], item[2]))
    print('ok')