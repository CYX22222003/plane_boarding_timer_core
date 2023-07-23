import scipy as sci
import numpy as np
import matplotlib.pyplot as plt
time_set = []
nu = int(input('no of times:'))
max_luggage = int(input("max luggage:"))
disobedience_rate = float(input("Disobedience rate"))
av_luggage = int(input('average luggages:'))
boarding_method = input("intended boarding method")
for shu in range(nu):
	print(shu + 1) #check the progress
###########################################################################
####
####part 1: Initialize
#Define number of rows and columns
	n_rows=33
	n_cols=6
	#Calculate number of passengers
	n_pass=n_rows*n_cols
	#Create seat matrix
	seats=np.zeros((n_rows,n_cols))
	seats[:,:]=-1
	#Create aisle array
	aisle_q=np.zeros(n_rows)
	aisle_q[:]=-1
	#Create initial passenger number queue
	pass_q=[int(i) for i in range(n_pass)]
	pass_q=np.array(pass_q)
	#Create array for seat nos
	row_q_init=np.zeros(n_pass)
	col_q_init=np.zeros(n_pass)
	#Let's create moveto arrays
	moveto_loc=np.zeros(n_pass)
	moveto_time=np.zeros(n_pass)
	moveto_loc_dict={i:j for i in pass_q for j in moveto_loc}
	moveto_time_dict={i:j for i in pass_q for j in moveto_time}
	###########################################################################
	####
	###part 2
	def AssignSeats(rq,cq,assign_type,n_pass=n_pass,n_rows=n_rows):
		##method 1: random boarding
		if(assign_type=="Random"):
			#Initialize possible row positions
			av_rows=np.arange(0,n_rows,1)
			#Make as many copies of these positions as the number of columns
			av_rows=np.tile(av_rows,(n_cols,1))
			av_rows=av_rows.T.flatten()
			#Initialize possible column positions
			av_cols=np.arange(0,n_cols,1)
			#Make as many copies of these positions as the number of rows
			av_cols=np.tile(av_cols,(n_rows,1)).flatten()
			#Create list of all possible seat positions
			av_seats=np.zeros((n_pass,2))
			for i in range(n_pass):
			av_seats[i]=[av_rows[i],av_cols[i]]
			#Randomize seat positions
			sci.random.shuffle(av_seats)
			rq=av_seats[:,0]
			cq=av_seats[:,1]

		if(assign_type=="BBS"):
			#Initialize initial and final positions
			i=0
			f=n_rows
			#Define column seating positions
			c=[0,5,1,4,2,3]
			#Define iteration counter
			count=0
			#Assign queue
			while(f<=n_pass):
			cq[i:f]=[c[count]]*n_rows
			i+=n_rows
			f+=n_rows
			count+=1
			#Initialize possible row positions
			av_rows = np.arange(0,n_rows,1)
			np.random.shuffle(av_rows)
			#Make as many copies of these positions as the number of columns
			av_rows=np.tile(av_rows,(n_cols,1)).flatten()
			rq = av_rows

		if(assign_type=="BBA"):
			#Initialize possible row positions
			av_rows=np.arange(0,n_rows,1)
			#Make as many copies of these positions as the number of columns
			av_rows=np.tile(av_rows,(n_cols,1))
			av_rows=av_rows.T.flatten()
			av_rows = np.sort(av_rows)[::-1]
			#Initialize possible column positions
			av_cols=np.arange(0,n_cols,1)
			#Make as many copies of these positions as the number of rows
			av_cols=np.tile(av_cols,(n_rows,1)).flatten()
			#Create list of all possible seat positions
			av_seats=np.zeros((n_pass,2))
			for i in range(n_pass):
			av_seats[i]=[av_rows[i],av_cols[i]]
			#Randomize seat positions
			rq=av_seats[:,0]
			cq=av_seats[:,1]

		##method 4:boarding by columns
		if(assign_type=="SINP"):
		#Initialize initial and final positions
			i=0
			f=n_rows
			#Define column seating positions
			c=[0,5,1,4,2,3]
			#Define iteration counter
			count=0
			#Assign queue
			while(f<=n_pass):
			rq[i:f]=list(reversed(range(0,n_rows)))
			cq[i:f]=[c[count]]*n_rows
			i+=n_rows
			f+=n_rows
			count+=1

		##method 5 reverse pyramid method
		if(assign_type == 'Reverse_Pyramid'):
			cq,rq = np.loadtxt('sequence.csv',delimiter = ',', usecols = (0,1), unpack = True)
			return rq,cq
###########################################################################
#part 3: assign factors
	row_q,col_q=AssignSeats(row_q_init,col_q_init,boarding_method)
	def norm_distribute(a,b,c):
		import random
		lst = []
		i = 0
		while i < c:
			rannum = random.normalvariate(a,b)
			if rannum > 0 and rannum < 1.5:
				lst.append(rannum)
				i += 1
			else:
				continue
		return lst
	mean_velocity= 1.34
	stddev_velocity= 0.37
	velocity_q=norm_distribute(mean_velocity,stddev_velocity,n_pass)
	def weibull_dis(a, b, c):
		import random
		lst = []
		i = 0
		while i < c:
			rannum = random.weibullvariate(a,b)
			if rannum > 0 and rannum < max_luggage:
				lst.append(rannum)
				i += 1
			else:
				continue
		return lst
	time_l = weibull_dis(16,1.7, n_pass)
	time_q = np.array(time_l)
	pass_dict={}
	time_dict={}
	velocity_dict = {}
	seat_nos=np.column_stack((row_q,col_q))
	NL = []
	shu2 =0
	while shu2 <= n_pass:
		N = list(np.random.poisson(av_luggage,1))
		if N[0] < 10:
			NL += N
			shu2 +=1
		else:
			continue
	NL = np.array(NL)
	for i in range(n_pass):
		pass_dict[i]=seat_nos[i]
	for i in range(n_pass):
		time_dict[i]=time_q[i]
	for i in range(n_pass):
		velocity_dict[i] = velocity_q[i]*(1-NL[i]*0.1)
	#Create sum time array
	sum_time=np.zeros(n_pass)
	for i in range(n_pass):
		sum_time[i]=sum(time_q[:i+1])
###########################################################################
##part 4: function to move passengers into aircraft
	def MoveToAisle(t,aisle_q,pass_q,sum_time):
		if(t>sum_time[0]):
			if(aisle_q[0]==-1):
				aisle_q[0]=pass_q[0].copy()
				pass_q=np.delete(pass_q,0)
				sum_time=np.delete(sum_time,0)
		return aisle_q,pass_q,sum_time
###########################################################################
##part 5: simulation of boarding method
	time=0
	time_step= 0.4454/1.34 #speed = velocity_dict[passg] #distance of each step = 0.4454
	exit_sum=np.sum(pass_q)
	pass_sum=np.sum(seats)
	while(pass_sum!=exit_sum):
		if(pass_q.size!=0):
			aisle_q,pass_q,sum_time=MoveToAisle(time,aisle_q,pass_q,sum_time)
		for passg in aisle_q:
			if(passg!=-1):
				row=int(np.where(aisle_q==passg)[0]
					if(moveto_time_dict[passg]!=0):
						if(time>moveto_time_dict[passg]):
							if(moveto_loc_dict[passg]=="a"):
								#If move is in the aisle, check if position ahead is empty
								if aisle_q[row+1]==-1:
									aisle_q[row+1]=passg
									aisle_q[row]=-1
									#Set moves to 0 again
									moveto_loc_dict[passg]=0
									moveto_time_dict[passg]=0
								elif moveto_loc_dict[passg]=="s":
									#If move is to the seat,
									#Find seat row and column of passenger
									passg_row=int(pass_dict[passg][0])
									passg_col=int(pass_dict[passg][1])
									#Set seat matrix position to the passenger number
									seats[passg_row,passg_col]=passg
									#Free the aisle
									aisle_q[row]=-1
							elif(moveto_time_dict[passg]==0):
								#If move hasn't been assigned to passenger
								#Check passenger seat location
								passg_row=int(pass_dict[passg][0])
								passg_col=int(pass_dict[passg][1])
								if(passg_row==row):
									#If passenger at the row where his/her seat is,
									#Designate move type as seat
									moveto_loc_dict[passg]="s"
									#Check what type of seat: aisle, middle or window
									#Depending upon seat type, designate when it is time to move
									#tis=k*0.4454/0.75vm
									if(passg_col==0):
										if(seats[passg_row,1]!=-1 and seats[passg_row,2]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.25*velocity_dict[passg])
										elif(seats[passg_row,1]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.5*velocity_dict[passg])
										elif(seats[passg_row,2]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.5*velocity_dict[passg])
										else:
											moveto_time_dict[passg]=time+ time_dict[passg] +3*0.445/((0.75*velocity_dict[passg]))
									elif(passg_col==5):
										if(seats[passg_row,4]!=-1 and seats[passg_row,3]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.25*velocity_dict[passg])
										elif(seats[passg_row,4]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.5*velocity_dict[passg])
										elif(seats[passg_row,3]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.5*velocity_dict[passg])
										else:
											moveto_time_dict[passg]=time+ time_dict[passg] + 3*0.445/(0.75*velocity_dict[passg])
							
									elif(passg_col==1):
										if(seats[passg_row,2]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 2*0.445/((0.5*velocity_dict[passg]))
										else:
											moveto_time_dict[passg]=time+ time_dict[passg] +2*0.445/((0.75*velocity_dict[passg]))
									elif(passg_col==4):
										if(seats[passg_row,3]!=-1):
											moveto_time_dict[passg]=time+ time_dict[passg] + 2*0.445/((0.5*velocity_dict[passg]))
										else:
											moveto_time_dict[passg]=time+ time_dict[passg] +2*0.445/((0.75*velocity_dict[passg]))
									elif(passg_col==2 or passg_col==3):
										moveto_time_dict[passg]=time+ time_dict[passg] + 1*0.445/(0.75*velocity_dict[passg])

								elif(passg_row!=row):
									#If passenger is not at the row where his/her seat is,
									#Designate movement type as aisle
									moveto_loc_dict[passg]="a"
									#Designate time to move
									moveto_time_dict[passg]=time+time_dict[passg]
				###########################################################################
####
#part 6:calculate total time
#Iteration timekeeping
				time += time_step
				pass_sum=np.sum(seats)
			time = time*(1 + disobedience_rate)
			time_set.append(time)

###########################################################################
###
#part 7: output
time_array = np.array(time_set)
data = np.array([np.arange(nu), time_array])
#save data into the data_random file
np.savetxt("data.csv", data.T, fmt = '%d',delimiter = ',')