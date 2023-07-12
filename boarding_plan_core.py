import random
import numpy as np
import scipy as sci

N = 40#row number
k = 6#column number

#assign position to each passenger #random method
av_rows = np.arange(0,N,1)
av_rows = np.tile(av_rows,(k,1))
av_rows = av_rows.T.flatten()
av_cols = np.arange(0,k,1)
av_cols = np.tile(av_cols,(N,1)).flatten()
av_seats = np.zeros((N*k,2))
for i in range(N*k):
    av_seats[i]=[av_rows[i],av_cols[i]]
np.random.shuffle(av_seats)
seat_lst = [[int(list(ele)[0]),int(list(ele)[1]%3),(1 if list(ele)[1]>=3 else 0)] for ele in list(av_seats)]
print(seat_lst)
#define passenger class
class passenger(object):
    def __init__(self,current_pos,target_pos,column_dir = 1,column_pos = 0):#dir: 1 for left 2 for right / pos:0: aisle, 1:middle 2:window
        #record of column information
        self.column_dir = column_dir  #left hand or right hand
        self.column_pos = column_pos  #middle window or aisle
        #record of position in the queue
        self.current_pos = current_pos
        self.target_pos = target_pos
        self.status = False
        #timer
        self.luggage_time = 0
        self.isle_time = 0
        self.seat_shuffle_time = 1
        self.shuffle_multiplier = 2
        #luggage ammount
        #self.luggage = ....

#position list

position_lst = [None for i in range(N)]
column_status = [[[False,False,False],[False,False,False]] for i in range(N)]
position_lst2 = []
#note: way of assignment should be changed as the row number and column number change to avoid clustering 
print("current pos, target pos, column_pos, column_dir") 
for i in range(N*k):
    dirt = seat_lst[i][2]
    pos = seat_lst[i][1]
    target = seat_lst[i][0]
    ele = passenger(i+N,target,dirt,pos)
    position_lst.append(ele)
    print(ele.current_pos,ele.target_pos,ele.column_pos,ele.column_dir)

#check list
def check_lst(lst):
    for i in lst:
        if isinstance(i,passenger):
            if i.status == False:
                return True
    return False

def check_col(lst,p):
    for k in range(p):
        if lst[k]: #k is false if it is empty
            return True #true if it is occupied
    return False


#start iteration
time_lst = []
breakpt = False
while check_lst(position_lst):
    for i in range(len(position_lst)):
        if isinstance(position_lst[i],passenger):
            position_lst[i].isle_time += 1
            #case 1: move forward
            if position_lst[i].current_pos != position_lst[i].target_pos  and position_lst[i-1] == None:
                position_lst[i].current_pos -= 1 #it has not reach the position and there is a empty space ahead
                position_lst[i-1],position_lst[i] = position_lst[i],position_lst[i-1]
                continue

            #case2: reach position
            if position_lst[i].current_pos == position_lst[i].target_pos:
#               #case 2.1:account for seat_shuffling time, if statement to avoid over-counting
                if position_lst[i].luggage_time <= 0:
                    column_status[position_lst[i].current_pos][position_lst[i].column_dir][position_lst[i].column_pos] = True
                    if check_col( column_status[position_lst[i].current_pos][position_lst[i].column_dir],position_lst[i].column_pos):
                        position_lst[i].seat_shuffle_time *= position_lst[i].shuffle_multiplier

                #case 2.2: account for luggage stowing time
                position_lst[i].luggage_time += 1
                if position_lst[i].luggage_time > 3: #can be related to the number of carry-ons 
                    time_lst.append(position_lst[i].isle_time+position_lst[i].luggage_time+position_lst[i].seat_shuffle_time)
                    position_lst[i].status = True
                    position_lst[i] = None
           

#print the final time
print(time_lst,[(col[0],col[1]) for col in column_status])
 


    
