import math
import numpy as np
import pandas as pd
from texttable import Texttable

def getMovies(file_name):
    data = pd.read_csv('movies.csv')
    col_1 = data['movieId']
    col_2 = data['title']
    col_3 = data['genres']
    movies = {}
    movies_title = {}
    i = 0
    for line in col_3:
        arr = line.split("|")
        movies[col_1[i]] = arr
        i += 1
    i = 0
    for line in col_2:
        arr = line
        movies_title[col_1[i]] = arr
        i += 1
    return movies, movies_title

def pearson(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    avg_x = 0.0
    avg_y = 0.0
    for key in user1:
        avg_x += key[1]
    avg_x = avg_x / len(user1)

    for key in user2:
        avg_y += key[1]
    avg_y = avg_y / len(user2)

    for key1 in user1:
        for key2 in user2:
            if key1[0] == key2[0]:
                sum_xy += (key1[1] - avg_x) * (key2[1] - avg_y)
                sum_y += (key2[1] - avg_y) * (key2[1] - avg_y)
        sum_x += (key1[1] - avg_x) * (key1[1] - avg_x)

    if sum_xy == 0.0:
        return 0
    sx_sy = math.sqrt(sum_x * sum_y)
    return sum_xy / sx_sy


def get_rating():
    f = open('train_set.csv')
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
    return user_rate, movie_user

# 计算与制定的邻居之间最为相近的邻居
# 输入：指定的用户ID，用户对电影的评分表，电影对应的用户表
# 输出：与制定用户最为相邻的邻居列表
# 用户字典：user_rate[用户id]=[(电影id,电影评分)...]
# 电影字典：movie_user[电影id]=[用户id1,用户id2...]
def nearuser_k(userid, user_rate, movie_user):
    neighbors = []
    for item in user_rate[userid]:
        # 在每一部电影与之相关的用户中查找邻居
        for neighbor in movie_user[item[0]]:
            if neighbor != userid and neighbor not in neighbors:
                neighbors.append(neighbor)
    # 计算相似度并输出
    neighbors_dist = []
    for neighbor in neighbors:
        dist = pearson(user_rate[userid], user_rate[neighbor])
        neighbors_dist.append([dist, neighbor])
    neighbors_dist.sort(reverse=True)
    return neighbors_dist


def recommendation(userid, k, movieid):
    r = get_rating()
    user_rate, movie_user = get_user(r)
    # 计算与userid最为相近的前k个用户，返回数组的格式为[[相似度，用户id]...]
    neighbors = nearuser_k(userid, user_rate, movie_user)[:k]
    # 计算邻居的每一部电影与被推荐用户之间的相似度大小
    recommend_dict = {}
    recommend_movie = {}
    for neighbor in neighbors:
        if neighbor[0] < 0:
            continue
        neighbor_user_id = neighbor[1]  # 邻居用户的ID
        movies = user_rate[neighbor_user_id]  # 邻居用户对电影的评分列表
        # 计算每一部电影对用户的推荐程度大小
        for movie in movies:
            if movie[0] not in recommend_dict:
                recommend_movie[movie[0]] = neighbor[0] * movie[1]
                recommend_dict[movie[0]] = neighbor[0]
            else:
                recommend_movie[movie[0]] += neighbor[0] * movie[1]
                recommend_dict[movie[0]] += neighbor[0]

    # 建立推荐的列表
    recommend_list = []
    for key in recommend_dict:
        recommend_dict[key] = recommend_movie[key]/recommend_dict[key]
    for key in recommend_dict:
        recommend_list.append([recommend_dict[key], key])  # 将字典转化为list，其中元素的第一项为推荐程度大小，第二项为电影的ID
    recommend_list.sort(reverse=True)  # 根据推荐的程度大小进行排序
    print(userid, movieid, recommend_dict[movieid])
    user_movies = [i[0] for i in user_rate[userid]]  # userid用户评分过的所有电影
    return [i[1] for i in recommend_list], recommend_list, user_rate, movie_user, neighbors, recommend_dict[movieid]


if __name__ == '__main__':
    movies, movies_title = getMovies('movies.csv')
    userid = 5
    movieid = 1
    k = 80
    n = 10
    recommend_list, recommend_list_all, user_movie, items_movie, neighbors, p_rating = recommendation(userid, k, movieid)
    # 输出前n个推荐项
    print(recommend_list_all[0:n])
    for movie_id in recommend_list[:n]:
        print("{0:10}\t{1:80}\t{2}".format(movie_id, movies_title[movie_id], movies[movie_id]))
    # data = pd.read_csv('test_set.csv')
    # userid = data['userId']
    # movieid = data['movieId']
    # rating = data['rating']
    # m = len(userid)
    # k = 670
    # sse = 0
    # for i in range(m):
    #     recommend_list, user_movie, items_movie, neighbors, p_rating = recommendation(userid[i], k, movieid[i])
    #     sse += (p_rating-rating[i])*(p_rating-rating[i])
    # print(sse)

