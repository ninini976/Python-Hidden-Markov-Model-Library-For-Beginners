import hmm
from io import StringIO
import numpy as np
import math
import sys

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.9,0.1],[0,1]])
hmm1.set_observation_matrix([[0.8,0.2],[0.3,0.7]])
hmm1.set_pi([0.85,0.15])

# #........The following part is the code for reading data form file "data"

# txt = []
# file = open('data')


# for line in file: # This for loop splite each line in the data file to 3 numbers and saved in the list "txt"
# 	txt.append(line.split())

# observations = []
# pt_observation = []
# for i in range (0,5692): # 5692 is the total number of records
# 	if i < 5691 and int(txt[i+1][0]) == 1:
# 		if int(txt[i][2]) <= 6:
# 			pt_observation.append("-")
# 		else:
# 			pt_observation.append("+")
# 		observations.append(pt_observation)
# 		pt_observation = []
# 	else: 
# 		if i < 5691 and int(txt[i+1][0]) != 1:
# 			if int(txt[i][2]) <= 6:
# 				pt_observation.append("-")
# 			else:
# 				pt_observation.append("+")
# 		else:
# 			if int(txt[i][2]) <= 6:
# 				pt_observation.append("-")
# 			else:
# 				pt_observation.append("+")
# 			observations.append(pt_observation)

# ps_array = []

# # This is a filter that only filter out those seqences with only one record
# observations = [elem for elem in observations if len(elem)>1]


# The following part read simulated data from a file "obs.txt"
file = open("obs1")

observations = []

for line in file:
	observations.append(line.split())
for ob in observations:
	print ob
print len(observations)


log = 0
for ob in observations:		
	log = log + math.log(hmm1.observation_possibility(ob))
print log	
# following part is em for a00(based on the ob sequences in the list observations)

# a00 = 0.6
# out = 0.6
# error_tolerence = 0.000001
# hmm1.set_transition_matrix([[a00,1-a00],[0,1]])
# while True:
# 	a00 = out
# 	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]])
# 	divisor = 0
# 	dividend = 0
# 	for ob in observations:
# 		xi_sum = 0
# 		gamma_sum = 0
# 		for t in range(len(ob)-1):
# 			xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
# 			gamma_sum = gamma_sum + hmm1.gamma(t,0,ob)
# 		dividend = dividend + xi_sum
# 		divisor = divisor + gamma_sum
# 	out = dividend/divisor
# 	print out
# 	if abs(out - a00) < error_tolerence:
# 		break
# print a00
# print out



# This is the grid search on maximizing the product of P for each sequence

# Max_p_log = -1000000000000000000000000000000000000
# Max = 0
# for i in range(1,101):
# 	a = float(i)/100
# 	log = 0
# 	for ob in observations:
# 		hmm1.set_transition_matrix([[a,1-a],[0,1]])
# 		log = log + math.log(hmm1.observation_possibility(ob))
# 	print log	
# 	if log > Max_p_log:
# 		Max = a
# 		Max_p_log = log
# print Max




# following part is EM algorithm for a00(based on the ob sequences in the list observations)
error_tolerence = 0.00001

# set the starting value
a00 = 0.90
out_a00 = a00
hmm1.set_transition_matrix([[a00,1-a00],[0,1]])

# b00 = 0.8
# out_b00 = b00
# hmm1.set_observation_matrix([[b00, 1-b00], [0.375,0.625]])

b11 = 0.90
out_b11 = b11
hmm1.set_observation_matrix([[0.8, 0.2], [1-b11,b11]])



# out2 = b11
# pi0 = 0.7488
# out3 = pi0
# hmm1.set_pi([pi0,1-pi0])


while True: # This is a loop of EM algorithm
	# a00 = out_a00
	# b00 = out_b00
	b11 = out_b11
	# pi0 = out3
	
	divisor_a00 = 0
	divisor_b00 = 0
	divisor_b11 = 0
	dividend_a00 = 0
	dividend_b11 = 0
	dividend_b00 = 0
	# out3 = 0 # out3 is for estimate of pi_0
	
	hmm1.set_observation_matrix([[0.8, 0.2], [1-b11,b11]])
	# hmm1.set_transition_matrix([[a00, 1-a00],[0,1]])
	# hmm1.set_pi([pi0, 1-pi0])
	
	for ob in observations:
		# xi_sum = 0 # element that will sum up to the dividend of a00
		# gamma_sum = 0 # element that will sum up to the divisor of a00
		# gamma_sum1 = 0 # element that will sum up to the dividend of b00
		# gamma_sum_p1 = 0 # element that will sum up to the divisor ot b00
		gamma_sum2 = 0 # element that will sum up to the dividend of b11
		gamma_sum_p2 = 0 # element that will sum up to the divisor ot b11
		for t in range(len(ob)-1):
			# this is for a00
			# xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
			# gamma_sum = gamma_sum + hmm1.gamma(t,0,ob)
			
			# this is for b00
			# gamma_sum1 = gamma_sum1 + hmm1.gamma(t,0,ob)
			# if ob[t] == "-":
			# 	gamma_sum_p1 = gamma_sum_p1 + hmm1.gamma(t,0,ob)

			#this is for b11
			gamma_sum2 = gamma_sum2 + hmm1.gamma(t,1,ob)
			if ob[t] == '+':
				gamma_sum_p2 = gamma_sum_p2 + hmm1.gamma(t,1,ob)	

		t = len(ob) - 1
		gamma_sum2 = gamma_sum2 + hmm1.gamma(t,1,ob)
		if ob[t] == '+':
			gamma_sum_p2 = gamma_sum_p2 + hmm1.gamma(t,1,ob)


		# divisor_a00 = divisor_a00 + gamma_sum
		# divisor_b00 = divisor_b00 + gamma_sum1
		divisor_b11 = divisor_b11+ gamma_sum2
		# dividend_a00 = dividend_a00 + xi_sum
		# dividend_b00 = dividend_b00 + gamma_sum_p1
		dividend_b11 = dividend_b11 + gamma_sum_p2
		
		# out3 = out3 + hmm1.gamma(0,0,ob)

	# out_a00 = dividend_a00 / divisor_a00
	# out_b00 = dividend_b00 / divisor_b00
	out_b11 = dividend_b11 / divisor_b11
	# out3 = out3/len(observations)
	# print out_a00
	print out_b11
	
	# hmm1.print_hmm()
	log = 0
	for ob in observations:
		log = log + math.log(hmm1.observation_possibility(ob))
	print log

	if (abs(out_b11 - b11) < error_tolerence): # and (abs(out_b11 - b11) < error_tolerence):
		break


print "result"
print "a"
print a00
print out_a00
print "b11"
print b11
print out_b11
# print "pi0"
# print pi0
# print out3

log = 0
for ob in observations:
	log = log + math.log(hmm1.observation_possibility(ob))
print "Total posibility:"
print log
