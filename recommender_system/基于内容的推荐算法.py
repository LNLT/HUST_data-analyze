import numpy as np
import pandas as pd
from pandas import  *
from numpy import *
import math
from sklearn.metrics.pairwise import cosine_similarity

def get_rating():
    f = open('train_set.csv')
    ratings = f.readlines()
    f.close()
    # ratings = pd.read_csv('train_set.csv', usecols=['userId', 'movieId', 'rating'])
    r = []
    i = 0
    for line in ratings:
        if i < 1:
            i += 1
            continue
        rate = line.strip().split(',')
        r.append([int(rate[0]), int(rate[1]), float(rate[2])])
    return r

def get_user(r):
    # 用户字典：user_rate[用户id]=[(电影id,电影评分)...]
    # 电影字典：movie_user[电影id]=[用户id1,用户id2...]
    user_rate = {}
    movie_user = {}
    for i in r:
        user_rank = (i[1], i[2])
        if i[0] in user_rate:
            user_rate[i[0]].append(user_rank)
        else:
            user_rate[i[0]] = [user_rank]
        if i[1] in movie_user:
            movie_user[i[1]].append(i[0])
        else:
            movie_user[i[1]] = [i[0]]
    # print(user_rate[1])
    # print(movie_user)
    return user_rate, movie_user

def moviesID():
    movies_ID = []
    f = open('movies.csv')
    f.readline()
    ratings = f.readlines()
    for row in ratings:
        row = row.strip().split(",")
        movies_ID.append([int(row[0])])
    return movies_ID

def read_csv():
    movies = pd.io.parsers.read_csv('movies.csv')
    movies.head()
    data = movies['genres']
    moviesname = movies['title']
    final_list = list()
    for row in data:
        row = row.split('|')
        final_list.append(row)
    return final_list,moviesname

def createM(dataSet):
    C1 = []
    for data in dataSet:
        for i in data:
            if i not in C1:
                C1.append(i)
    print(C1)
    len_C1 = len(C1)
    len_da = len(dataSet)
    tidf = np.zeros([len_da,len_C1])
    idf_num = np.zeros([len_da,len_C1])
    M = np.zeros([len_da,len_C1])  #9526*20的矩阵
    a = 0
    for data in dataSet:
        for i in data:
            b = C1.index(i)
            M[a, b] = 1
            idf_num[a,b] = 1
        a = a+1
    for k in range(len_da):
        sum_of_col = sum(M[k,:])
        for j in range(len_C1):
            if M[k,j]:
                M[k, j] = M[k, j] / sum_of_col

    for j in range(len_C1):
        sum_of_col = sum(idf_num[:,j])
        for k in range(len_da):
            if idf_num[k,j]:
                idf_num[k,j] = math.log(len_da/(sum_of_col+1))

    for k in range(len_da):
        for j in range(len_C1):
            tidf[k,j] = idf_num[k,j]*M[k, j]

    return tidf,len_da

def test():
    f = open('test_set.csv')
    ratings = f.readlines()
    f.close()
    r = []
    i = 0
    for line in ratings:
        if i < 1:
            i += 1
            continue
        rate = line.strip().split(',')
        r.append([int(rate[0]), int(rate[1]), float(rate[2])])
    return r

def test_user(r):
    # 用户字典：user_test[用户id]=[(电影id,电影评分)...]
    user_test = {}
    for i in r:
        user_rank = (i[1], i[2])
        if i[0] in user_test:
            user_test[i[0]].append(user_rank)
        else:
            user_test[i[0]] = [user_rank]
    return user_test

if __name__ == "__main__":
    dataSet,moviesname = read_csv()
    movies_ID = moviesID()
    matrixa,len_da = createM(dataSet)
    matrix = cosine_similarity(matrixa)
    r = get_rating()
    user_rate, movie_user = get_user(r)
    #print(user_rate)
    r = test()
    user_test = test_user(r)
    print(user_test)

    pre_grade = list()
    # 用户字典：[用户id]=[(电影id,电影评分)...]
    rint_rate = 0
    pre_grade = {}
    for i,j in user_test.items(): #预测每个用户打分
        row = user_rate[i]  #查找用户已打过的分数
        len_row = len(row)
        for q in range(len(j)):  #预测该用户每个想看的电影的打分
            sum_a = 0
            sum_b = 0
            sum_c = 0
            test_name = j[q]
            movname = test_name[0]  # 电影的id
            cola = movies_ID.index([movname])  # 得到电影的序号
            for k in range(len_row):
                key_v = row[k]
                key_name = key_v[0]
                colb = movies_ID.index([key_name])
                if(matrix[cola,colb]>0):
                    sum_a +=key_v[1]*matrix[cola,colb]
                    sum_b +=matrix[cola,colb]
                    sum_c +=key_v[1]
                else:
                    continue
            if sum_b ==0 :
                pre_score = sum_c / len_row
            else :
                pre_score = sum_a / sum_b
            rint_rate+= (pre_score-test_name[1])**2
            user_rank = (movname,pre_score)
            if int(i) in pre_grade:
                pre_grade[int(i)].append(user_rank)
            else:
                pre_grade[int(i)] = [user_rank]
    print(pre_grade)
    print(rint_rate)
    while(1):
        # 用户字典：[用户id]=[(电影id,电影评分)...]
        a = int(input("UserId:"))
        b = int(input("k:"))
        row_u = user_rate[a]
        len_urow = len(row_u)
        recom = {}
        for j in range(len_da):
            den_a = 0
            den_b = 0
            den_c = 0
            for row in row_u:
                cola = movies_ID.index([row[0]])
                if matrix[cola, j] > 0:
                    if movies_ID[j] in row_u:
                        continue
                    else:
                        den_a += matrix[cola, j] * row[1]
                        den_b += matrix[cola, j]
                        den_c += row[1]
                else:
                    continue
            if den_b == 0:
                pre_s = den_c / len_urow
            else:
                pre_s = den_a / den_b
            str = moviesname[j]
            recom[str] = pre_s
        recom_mov = sorted(recom.items(), key=lambda x: x[1], reverse=True)
        for k in range(b):
            print(recom_mov[k])














