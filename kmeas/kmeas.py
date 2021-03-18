import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import csv
def long_s(center, data):
    s = 0
    for i in range(1, 14):
        s += pow(center[i]-float(data[i]), 2)
    return s

def ssenum(data_min):
    # acc = 0
    # for i in range(m):
    #     acc += data_min[i, 1]
    sse_num = [0, 0, 0, 0]
    for i in range(m):
        sse_num[int(data_min[i, 0])] += data_min[i, 1]
    print('sse_single', sse_num)
    sse = sse_num[1] + sse_num[2] + sse_num[3]
    print('sse_all:', sse)
    return sse

def get_points(m, data, j, data_min):
    # 通过数据过滤来获得给定簇的所有
    point = []
    for i in range(m):
        if data_min[i, 0] == j + 1:
            point.append(data[i])
    return point

def get_accpoints(m, data, j):
    # 通过数据过滤来获得给定簇的所有
    point = []
    data = np.array(data)
    for i in range(m):
        if int(data[i, 0]) == j + 1:
            point.append(data[i])
    return point

def get_acc(m, data, k, data_min):
    num1 = data_min[0, 0]
    num3 = data_min[m-1, 0]
    num2 = max(3-num1, 3-num3, 6-(num1+num3))
    num = [num1, num2, num3]
    acc = 0
    for j in range(k):
        point = get_points(m, data, num[j]-1, data_min)
        accpoint = get_accpoints(m, data, j)
        temp_acc = min(len(point) / len(accpoint), len(accpoint) / len(point))
        if temp_acc-acc > 0 and temp_acc < 1:
            acc = temp_acc
    print('acc:', acc)

if __name__ == '__main__':
    with open('归一化数据.csv') as f:
        reader = csv.reader(f)
        data = []
        for j in reader:
            j = list(map(float, j))
            data.append(j)
    m = len(data)
    k = 3
    change = True
    data_min = np.mat(np.zeros((m, 2)))
    centers = []
    for i in range(k):
        c = []
        c.append(0)
        for j in range(13):
            c.append(rd.random())
        centers.append(c)

    while change:
        change = False
        for i in range(m):
            min_s = 10000000.0
            min_center = -1
            for j in range(k):
                distance = long_s(centers[j], data[i])
                if distance < min_s:
                    min_center = j + 1
                    min_s = distance
            if data_min[i, 0] != min_center or data_min[i, 1] != min_s:
                data_min[i, :] = min_center, min_s
                change = True
        for j in range(k):
            # 通过数据过滤来获得给定簇的所有
            point = get_points(m, data, j, data_min)
            # 计算所有点的均值,axis=0表示沿矩阵的列方向进行均值计算
            centers = np.array(centers)
            centers[j, :] = np.mean(point, axis=0)

    ssenum(data_min)
    get_acc(m, data, k, data_min)
    # 最终结果图示
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    # 不同的子集使用不同的颜色
    x = int(input())
    y = int(input())
    # x = 6
    # y = 7
    for j in range(k):
        point = get_points(m, data, j, data_min)
        point = np.array(point)
        plt.scatter(point[:, x], point[:, y], c=colors[j])
    plt.scatter(centers[:, x], centers[:, y], marker='*', s=200, c='black')
    plt.show()
    with open("result1.csv", 'w') as f:
        for i in range(m):
            f.write("{}\t,{}\n".format(data_min[i, 0], data_min[i, 1]))
    print('ok')
    # 1, 7