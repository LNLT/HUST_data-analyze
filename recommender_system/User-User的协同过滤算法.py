import math
import numpy as np
import pandas as pd

def getMovies():
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
    movies = []
    for x in r:
        if x[1] not in movies:
            movies.append(x[1])
    m = len(movies)
    user_movie = np.zeros([671, m])
    for item in r:
        y = movies.index(item[1])
        user_movie[item[0]-1, y] = item[2]
    user_user = np.corrcoef(user_movie)
    return r, user_user


# 用户字典：user_rate[用户id]=[(电影id,电影评分)...]
# 电影字典：movie_user[电影id]=[用户id1,用户id2...]
def get_user(r):
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


# 计算与指定的邻居之间最为相近的邻居
# 输入：指定的用户ID，用户对电影的评分表，电影对应的用户表
# 输出：与指定用户最为相邻的邻居列表
# 用户字典：user_rate[用户id]=[(电影id,电影评分)...]
# 电影字典：movie_user[电影id]=[用户id1,用户id2...]
def nearuser_k(userid, user_rate, movie_user, user_user):
    neighbors = []
    neighbors_dist = []
    for item in user_rate[userid]:
        # 在每一部电影与之相关的用户中查找邻居
        for neighbor in movie_user[item[0]]:
            if neighbor != userid and neighbor not in neighbors:
                neighbors.append(neighbor)
                dist = user_user[userid - 1, neighbor - 1]
                neighbors_dist.append([dist, neighbor])
    neighbors_dist.sort(reverse=True)
    return neighbors_dist


def recommendation(userid, movieid, user_rate, movie_user, user_user, k):
    # 计算与userid最为相近的前k个用户，返回数组的格式为[[相似度，用户id]...]
    neighbors_dist = nearuser_k(userid, user_rate, movie_user, user_user)
    neighbors_dist = neighbors_dist[:k]
    # 计算邻居的每一部电影与被推荐用户之间的相似度大小
    recommend_dict = {}
    recommend_movie = {}
    sum = 0
    for movie in user_rate[userid]:
        sum += movie[1]
    user_acc = sum/len(user_rate[userid])
    for neighbor in neighbors_dist:
        if user_user[userid-1, neighbor[1]-1] < 0:
            continue
        movies = user_rate[neighbor[1]]  # 邻居用户对电影的评分列表
        sum = 0
        for movie in movies:
            sum += movie[1]
        neighbor_acc = sum / len(movies)

        # 计算每一部电影对用户的推荐程度大小
        for movie in movies:
            if movie[0] not in recommend_dict:
                recommend_movie[movie[0]] = neighbor[0] * (movie[1] - neighbor_acc)
                recommend_dict[movie[0]] = neighbor[0]
            else:
                recommend_movie[movie[0]] += neighbor[0] * (movie[1] - neighbor_acc)
                recommend_dict[movie[0]] += neighbor[0]

    # 建立推荐的列表
    recommend_list = []
    for key in recommend_dict:
        recommend_dict[key] = recommend_movie[key]/recommend_dict[key] + user_acc
        recommend_list.append([recommend_dict[key], key])  # 将字典转化为list，其中元素的第一项为推荐程度大小，第二项为电影的ID
    print(userid, movieid, recommend_dict[movieid])
    recommend_list.sort(reverse=True)  # 根据推荐的程度大小进行排序
    return [i[1] for i in recommend_list], recommend_dict[movieid], recommend_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    movies, movies_title = getMovies()
    r, user_user = get_rating()
    user_rate, movie_user = get_user(r)
    print('user_id:', end=' ')
    user_id = int(input())
    movie_id = 1
    print('k:', end=' ')
    k = int(input())
    print('n:', end=' ')
    n = int(input())
    recommend_list, p_rating, recommend_dict = recommendation(user_id, movie_id, user_rate, movie_user, user_user, k)
    # 输出前n个推荐项
    for movie in recommend_list[:n]:
        print("{0:6}\t{1:20}\t{2:80}\t{3}".format(movie, recommend_dict[movie], movies_title[movie], movies[movie]))

    data = pd.read_csv('test_set.csv')
    usersid = data['userId']
    moviesid = data['movieId']
    rating = data['rating']
    m = len(usersid)
    k = 95
    sse = 0
    for i in range(m):
        recommend_list, p_rating, recommend_dict = recommendation(usersid[i], moviesid[i], user_rate, movie_user, user_user, k)
        sse += (p_rating-rating[i])*(p_rating-rating[i])
    print(sse)