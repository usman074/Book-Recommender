import numpy as np
import math
import csv
import os.path
import random

def unique_user():
    list=[]
    with open("ratings.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            list.append(row)
    data = np.array(list)
    print(data)
    unique_user = np.unique(data[1:,1:2])
    np.save("unique_user", unique_user)

def average_rating():
    unique_user=np.load("unique_user.npy")
    list=[]
    avg_rating={}
    with open("ratings.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            list.append(row)
    data = np.array(list)

    for user in unique_user:
        avg=0
        indexes = np.where(data[:,1:2]==user)
        for y in range(len(indexes[0])):
            rate=data[indexes[0][y]]
            avg=avg+float(rate[2])
        avg = avg/len(indexes[0])
        avg_rating[user]=avg
    print(avg_rating)
    avg_rating_numpy=np.array(avg_rating)
    print(avg_rating_numpy)
    np.save("user_avg_rating",avg_rating_numpy)

def find_correlation():
    list=[]
    unique_user=np.load("unique_user.npy")
    unique_user=unique_user[0:500]
    other_user_data=[]
    current_user_data=[]
    correlation_list=[[],[]]
    correlation_dict = {}
    avg_rating = np.load("user_avg_rating.npy",allow_pickle=True)

    with open("ratings.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            list.append(row)
    data = np.array(list)
    for ind in range(len(unique_user)):
        print("--------------------------------------------------------------")
        current_user_data=[]
        correlation_list=[[],[]]
        print(unique_user[ind])
        indexes = np.where(data[:,1:2]==unique_user[ind])
        for a in range(len(indexes[0])):
            current_user_data.append(data[indexes[0][a]])
        for other_user_ind in range(ind+1,len(unique_user)):
            other_user_data=[]
            if (not ind==other_user_ind):
                other_user_indexes = np.where(data[:,1:2]==unique_user[other_user_ind])
                for b in range (len(other_user_indexes[0])):
                    other_user_data.append(data[other_user_indexes[0][b]])
            value1_list=[]
            value2_list=[]
            for c in range(len(current_user_data)):
                for d in range(len(other_user_data)):
                    if(current_user_data[c][0] == other_user_data[d][0]):
                        print("match")
                        temp1=calculate_pearson_value1(current_user_data[c])
                        temp2=calculate_pearson_value2(other_user_data[d])
                        value1_list.append(temp1)
                        value2_list.append(temp2)
                        break
            if(value1_list):
                temp3=correlation(value1_list,value2_list)
                if(temp3 != "error"):
                    correlation_list[0].append(other_user_data[0][1])
                    correlation_list[1].append(temp3)
        correlation_dict[current_user_data[0][1]]=correlation_list
        print(correlation_dict)
        print("--------------------------------------------------------------")
    correlation_numpy=np.array(correlation_dict)
    np.save("user_correlation",correlation_numpy)

def calculate_pearson_value1(x):
    avg_rating = np.load("user_avg_rating.npy",allow_pickle=True)
    rating = avg_rating.item().get(x[1])
    rating_diff = float(x[2]) - float(rating)
    return rating_diff
def calculate_pearson_value2(x):
    avg_rating = np.load("user_avg_rating.npy",allow_pickle=True)
    rating = avg_rating.item().get(x[1])
    rating_diff = float(x[2]) - float(rating)
    return rating_diff
def correlation(x,y):
    numerator_values = []
    value1 = []
    value2 = []
    for i in range (len(x)):
        numerator_values.append(float(x[i])*float(y[i]))
    numerator=sum(numerator_values)
    for i in range (len(x)):
        value1.append(float(x[i])*float(x[i]))
        value2.append(float(y[i])*float(y[i]))
    value3=sum(value1)
    value4=sum(value2)
    value3=math.sqrt(value3)
    value4=math.sqrt(value4)
    denomenator=value3*value4
    if(denomenator == 0.0):
        return "error"
    final_value = numerator/denomenator
    return final_value

def recommendation():
    corr = np.load("user_correlation.npy",allow_pickle=True)
    unique = np.load("unique_user.npy",allow_pickle=True)
    avg_rating = np.load("user_avg_rating.npy",allow_pickle=True)
    user1=0
    user2=0
    user1_data=[]
    user2_data=[]
    updated_user2_data=[]
    recommended_book_list=[]
    books_list=[]
    list=[]

    while True:
        rand=random.randint(1,501)
        selected_user=corr.item().get(unique[rand])
        if(len(selected_user[0]) > 0):
            m=max(selected_user[1])
            if(m>0):
                ind=selected_user[1].index(m)
                corr_user = selected_user[0][ind]
                user1=unique[rand]
                user2=corr_user
                break
    with open("ratings.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            list.append(row)
    data = np.array(list)
    indexes = np.where(data[:,1:2]==user1)
    for a in range(len(indexes[0])):
        user1_data.append(data[indexes[0][a]])
    indexes = np.where(data[:,1:2]==user2)
    for a in range(len(indexes[0])):
        user2_data.append(data[indexes[0][a]])
    for x in range(len(user2_data)):
        book_read = True
        for y in range(len(user1_data)):
            if (user2_data[x][0] == user1_data[y][0]):
                book_read = False
                break
        if (book_read):
            updated_user2_data.append(user2_data[x])
    user1_rating = avg_rating.item().get(user1)
    user2_rating = avg_rating.item().get(user2)
    for z in range(len(updated_user2_data)):
        book_rating=user2_rating-float(updated_user2_data[z][2])
        book_rating=book_rating+user1_rating
        if (book_rating > 3.0):
            recommended_book_list.append(updated_user2_data[z][0])
    with open("books.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            books_list.append(row)
    books = np.array(books_list)
    print("user selected for recommendation is "+str(user1))
    print("Following are the books recommended to "+str(user1))
    for book_ind in range(len(recommended_book_list)):
        ind=int(recommended_book_list[book_ind])
        print(books[ind][9])

if(not os.path.exists("unique_user.npy")):
    unique_user();

if(not os.path.exists("user_avg_rating.npy")):
    average_rating();

if(not os.path.exists("user_correlation.npy")):
    find_correlation()

recommendation()